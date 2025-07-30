import os
import subprocess
import time
import platform
from pathlib import Path
from app.logger import logger

FCITX5_PROFILE_CONTENT = """[Groups/0]
# Group Name
Name=Default
# Layout
Default Layout=us
# Default Input Method
DefaultIM=pinyin

[Groups/0/Items/0]
# Name
Name=keyboard-us
# Layout
Layout=

[Groups/0/Items/1]
# Name
Name=pinyin
# Layout
Layout=

[GroupOrder]
0=Default

"""

class SystemVncManager:
    def __init__(self):
        self.processes = []
        self.is_linux = platform.system().lower() == "linux"
        self.display = os.getenv("DISPLAY", ":199")
        self.vnc_password = os.getenv("VNC_PD", "orion")
        self.dbus_session_bus_address = None

    def setup_vnc_password(self):
        """Setup VNC password"""
        if not self.is_linux:
            return
            
        vnc_dir = Path.home() / ".vnc"
        vnc_dir.mkdir(parents=True, exist_ok=True)
        try:
            subprocess.run(["x11vnc", "-storepasswd", self.vnc_password, str(vnc_dir / "passwd")], 
                         check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to configure VNC password: {e}")

    def start_dbus(self):
        """Start dbus session bus and set environment variables"""
        if not self.is_linux:
            return

        # Create dbus session
        dbus_cmd = ["dbus-launch", "--sh-syntax"]
        try:
            result = subprocess.run(dbus_cmd, capture_output=True, text=True, check=True)
            # Parse dbus-launch output and set environment variables
            for line in result.stdout.splitlines():
                if line.startswith("DBUS_SESSION_BUS_"):
                    if "=" in line:
                        key, value = line.split("=", 1)
                        value = value.rstrip(";").strip("'").split(",")[0]
                        os.environ[key] = value
                        if key == "DBUS_SESSION_BUS_ADDRESS":
                            self.dbus_session_bus_address = value
            
            # Start dbus-daemon
            if self.dbus_session_bus_address:
                dbus_daemon_cmd = ["dbus-daemon", "--session", "--address=" + self.dbus_session_bus_address]
                process = subprocess.Popen(dbus_daemon_cmd)
                self.processes.append(process)
                time.sleep(1)  # Wait for dbus to start
                
                logger.info("Dbus session started successfully with address: " + self.dbus_session_bus_address)
            else:
                raise Exception("Failed to get DBUS_SESSION_BUS_ADDRESS")
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to start dbus: {e}")
            raise

    def start_xvfb(self):
        """Start Xvfb virtual display server"""
        cmd = ["Xvfb", self.display, "-screen", "0", "1280x1024x16", "-ac", "-noreset"]
        process = subprocess.Popen(cmd)
        self.processes.append(process)
        time.sleep(2)

    def start_x11vnc(self):
        """Start x11vnc server"""
        self.setup_vnc_password()
        cmd = [
            "x11vnc",
            "-display", self.display,
            "-geometry", "1280x1024",
            "-forever",
            "-shared",
            "-noxrecord",
            "-noxfixes",
            "-noxkb",
            "-noxdamage",
            "-rfbport", "5900",
            "-rfbauth", str(Path.home() / ".vnc" / "passwd")
        ]
        process = subprocess.Popen(cmd)
        self.processes.append(process)
        time.sleep(2)

    def start_fcitx(self):
        """Start fcitx input method"""
        process = subprocess.Popen(["fcitx5-remote", "-o"])
        self.processes.append(process)
        time.sleep(1)
        subprocess.run(["fcitx5-remote", "-r"])
        time.sleep(1)
        subprocess.run(["fcitx5", "-rd"])
        time.sleep(1)
        subprocess.run(["xdotool", "key", "Control_L+space"])
        
    def setup_fcitx_profile(self):
        """Setup fcitx5 profile configuration"""
        if not self.is_linux:
            return
             
        fcitx_config_dir = Path.home() / ".config" / "fcitx5"
        fcitx_config_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(fcitx_config_dir / "profile", "w") as f:
                f.write(FCITX5_PROFILE_CONTENT)
            logger.info("Fcitx5 profile configured successfully")
        except Exception as e:
            logger.error(f"Failed to configure fcitx5 profile: {e}")

    def start_all(self):
        """Start all required system processes"""
        if not self.is_linux:
            logger.info("Not running on Linux, skipping system processes")
            return
        
        self.start_dbus()
        self.start_xvfb()
        self.start_x11vnc()
        self.setup_fcitx_profile()
        self.start_fcitx()
        
    def cleanup(self):
        """Cleanup all processes"""
        if not self.is_linux:
            return
            
        for process in self.processes:
            try:
                process.terminate()
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
            except Exception as e:
                logger.error(f"Error cleaning up process: {e}") 