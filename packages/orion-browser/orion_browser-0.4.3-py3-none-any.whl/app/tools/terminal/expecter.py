import asyncio
import json
import re
from typing import AsyncGenerator, Awaitable, Callable, Tuple

from pexpect.exceptions import EOF, TIMEOUT
from pexpect.expect import Expecter

class MyExpecter(Expecter):
    async def my_expect_loop(
        self,
        PS1_REG,
        get_user_input: Callable[[], Awaitable[bytes]]
    ) -> AsyncGenerator[Tuple[bool, bytes], None]:
        """
        Asynchronous expect loop that handles terminal interactions.
        
        Args:
            PS1_REG: Regular expression pattern for the prompt.
            get_user_input: Coroutine function to get user input.
        
        Returns:
            An async generator yielding tuples of (bool, bytes) representing
            the state of the terminal output.
        """
        existing = self.existing_data()
        if existing is not None:
            return

        while True:
            try:
                # clear the user input buffer
                await get_user_input()
                data = self.spawn.read_nonblocking(self.spawn.maxread, timeout=0.01)
                m = re.search(PS1_REG, data)
                extra_input = await get_user_input()
                
                if extra_input:
                    data += extra_input
                if m:
                    result = (True, data[0:m.start()])
                else:
                    result = (False, data)
                extra = self.new_data(data)

                yield result

                if extra is not None:
                    return

            except TIMEOUT:
                await asyncio.sleep(0.2)
                continue
            except EOF:
                yield (True, b'')
                return
            except Exception as e:
                yield (True, ("Error in expect loop: " + str(e)).encode())
                break

            await asyncio.sleep(0.2)
