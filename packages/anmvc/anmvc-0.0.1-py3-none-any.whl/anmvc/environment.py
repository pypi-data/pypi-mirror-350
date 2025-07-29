import asyncio
import uuid
from typing import Optional

class Environment:
    def __init__(self, container_id: str, name: str, shell_type: str, eid: Optional[str] = None):
        self.id = eid or str(uuid.uuid4())
        self.container_id = container_id
        self.name = name
        self.shell_type = shell_type  # e.g. '/bin/bash', 'pwsh.exe', 'cmd.exe'
        self.process: Optional[asyncio.subprocess.Process] = None
        self.is_running = False

    async def start(self):
        if self.is_running:
            return
        # Start the shell subprocess attached to the container
        self.process = await asyncio.create_subprocess_exec(
            self.shell_type,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        self.is_running = True

    async def stop(self):
        if not self.is_running or self.process is None:
            return
        self.process.terminate()
        await self.process.wait()
        self.is_running = False
        self.process = None

    async def run_command(self, command: str) -> str:
        if not self.is_running or self.process is None:
            raise RuntimeError("Environment not running")
        # Send command + newline
        self.process.stdin.write(command.encode() + b"\n")
        await self.process.stdin.drain()

        # Read output until next prompt or timeout (simple approach)
        output = await self.process.stdout.readline()
        return output.decode().strip()

    async def interact(self):
        if not self.is_running or self.process is None:
            await self.start()

        print(f"Entering interactive shell for env '{self.name}' ({self.shell_type})")
        print("Press Ctrl-D to exit.")

        loop = asyncio.get_event_loop()

        async def read_stdout():
            while True:
                data = await self.process.stdout.read(1024)
                if not data:
                    break
                print(data.decode(), end="", flush=True)

        async def write_stdin():
            while True:
                line = await loop.run_in_executor(None, input)
                if line is None:
                    break
                self.process.stdin.write(line.encode() + b"\n")
                await self.process.stdin.drain()

        await asyncio.gather(read_stdout(), write_stdin())
