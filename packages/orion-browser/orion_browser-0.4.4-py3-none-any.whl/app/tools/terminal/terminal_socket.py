import asyncio
import json
from fastapi import WebSocket, WebSocketDisconnect
from pydantic import ValidationError
from app.logger import logger
from app.tools.terminal.terminal_manager import terminal_manager
from app.types.messages import TerminalInputMessage, TerminalOutputMessage, TerminalStatus

class TerminalSocket:
    """
    WebSocket server for handling terminal connections.
    This class manages bidirectional communication with terminals through WebSockets.
    """
    
    async def handle_connection(self, ws: WebSocket):
        """
        Handle a new WebSocket connection for terminal interaction.
        
        Args:
            ws: The WebSocket connection
        """
        await ws.accept()
        logger.info("New terminal WebSocket connection established")
        
        tasks = {}
        def stop_all_tasks():
            for task in tasks.values():
                task.cancel()
        
        async def get_socket_message():
            try:
                msg_data = await ws.receive_json()
                msg = TerminalInputMessage.model_validate(msg_data)
                task = asyncio.create_task(self.handle_msg(ws, msg))
                tasks[msg.action_id] = task
                task.add_done_callback(lambda _: tasks.pop(msg.action_id))
            except ValidationError as e:
                logger.error(f"Invalid message: {msg_data}, {e}")
                await self.send_resp(ws, TerminalOutputMessage(
                    action_id="",
                    type="error",
                    result=f"Invalid message: {e}",
                    output=[],
                    terminal_status="unknown",
                    terminal=""
                ))
            except json.JSONDecodeError as e:
                logger.error(f"JSONDecodeError: {e}")
                await self.send_resp(ws, TerminalOutputMessage(
                    action_id="",
                    type="error",
                    result=f"Invalid message: {e}",
                    output=[],
                    terminal_status="unknown",
                    terminal=""
                ))
            except Exception as e:
                logger.error(f"Error handling message: {e}")
                raise
        
        try:
            while True:
                await get_socket_message()
        except WebSocketDisconnect:
            logger.info("Websocket disconnected")
        except Exception as e:
            logger.error(e)
            logger.error(f"Error: {e}")
            logger.info("Closing websocket")
            await ws.close()
        
        stop_all_tasks()
    
    async def send_resp(self, ws: WebSocket, resp: TerminalOutputMessage):
        """
        Send a response to the client over the WebSocket connection.
        
        Args:
            ws: The WebSocket connection
            resp: The response data to send
        """
        logger.info(f"Sending resp {resp}")
        
        try:
            await ws.send_json(resp.model_dump())
        except RuntimeError as e:
            logger.error(f"Error sending resp: {e}")
    
    async def handle_msg(self, ws: WebSocket, msg: TerminalInputMessage):
        """
        Process a validated terminal input message.
        
        Args:
            msg: The validated terminal input message
            ws: The WebSocket connection
        """
        logger.info(f"Handle terminal socket msg#{msg.action_id} {msg}")
        
        terminal_id = msg.terminal
        terminal = await terminal_manager.get_terminal(terminal_id)
        
        if msg.type == "reset":
            await terminal.reset()
            response = msg.create_response(
                type="action_finish",
                result="terminal reset success",
                output=[],
                terminal_status="idle"
            )
            await self.send_resp(ws, response)
        
        elif msg.type == "reset_all":
            for term in terminal_manager.terminals.values():
                await term.reset()
            response = msg.create_response(
                type="action_finish",
                result="all terminals reset success",
                output=[],
                terminal_status="idle"
            )
            await self.send_resp(ws, response)
        
        elif msg.type == "view":
            terminal_status: TerminalStatus = "running" if terminal.is_running else "idle"
            response = msg.create_response(
                type="history",
                result=None,
                output=terminal.get_history(True, True),
                terminal_status=terminal_status
            )
            await self.send_resp(ws, response)
        
        elif msg.type == "view_last":
            terminal_status: TerminalStatus = "running" if terminal.is_running else "idle"
            response = msg.create_response(
                type="history",
                result=None,
                output=terminal.get_history(True, False),
                terminal_status=terminal_status
            )
            await self.send_resp(ws, response)
        
        elif msg.type == "kill":
            await terminal.kill_process()
            response = msg.create_response(
                type="action_finish",
                result="process killed",
                output=terminal.get_history(True, False),
                terminal_status="idle"
            )
            await self.send_resp(ws, response)
        
        elif msg.type == "command":
            if not msg.command:
                response = msg.create_response(
                    type="error",
                    result="must provide command",
                    output=[],
                    terminal_status="idle"
                )
                await self.send_resp(ws, response)
                return
            
            if msg.exec_dir:
                if not await terminal.set_working_directory(msg.exec_dir):
                    response = msg.create_response(
                        type="error",
                        result=f"Failed to change directory to {msg.exec_dir}",
                        output=[],
                        terminal_status="idle"
                    )
                    await self.send_resp(ws, response)
                    return
            
            if not msg.mode:
                msg.mode = "run"
            
            if msg.mode == "send_key":
                await terminal.send_key(msg)
                terminal_status: TerminalStatus = "idle" if not terminal.is_running else "running"
                response = msg.create_response(
                    type="action_finish",
                    result=f"Key sent: {msg.command}",
                    output=terminal.get_history(True, False),
                    terminal_status=terminal_status
                )
                await self.send_resp(ws, response)
            
            elif msg.mode == "send_line":
                await terminal.send_line(msg)
                terminal_status: TerminalStatus = "idle" if not terminal.is_running else "running"
                response = msg.create_response(
                    type="action_finish",
                    result=f"Line sent: {msg.command}",
                    output=terminal.get_history(True, False),
                    terminal_status=terminal_status
                )
                await self.send_resp(ws, response)
            
            elif msg.mode == "send_control":
                await terminal.send_control(msg)
                terminal_status: TerminalStatus = "idle" if not terminal.is_running else "running"
                response = msg.create_response(
                    type="action_finish",
                    result=f"Control character sent: {msg.command}",
                    output=terminal.get_history(True, False),
                    terminal_status=terminal_status
                )
                await self.send_resp(ws, response)
            
            elif msg.mode == "run":
                async for result in terminal.execute_command(msg):
                    await self.send_resp(ws, result)
            
            else:
                response = msg.create_response(
                    type="error",
                    result=f"Invalid mode: {msg.mode}",
                    output=[],
                    terminal_status="idle"
                )
                await self.send_resp(ws, response)
        
        else:
            logger.error(f"Invalid message type: {msg.type}")
            response = msg.create_response(
                type="error",
                result=f"Invalid message type: {msg.type}",
                output=[],
                terminal_status="idle"
            )
            await self.send_resp(ws, response)
        
        logger.info(f"Finished handling msg#{msg.action_id}")

terminal_socket = TerminalSocket()