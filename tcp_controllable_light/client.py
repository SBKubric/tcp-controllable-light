import asyncio
from polog import log
from json import loads, JSONDecodeError


class TcpLightClient:
    def __init__(self, host: str, port: int, max_package_size: int, encoding: str, queue: asyncio.Queue):
        self.host = host
        self.port = port
        self.max_package_size = max_package_size
        self.encoding = encoding
        self._reader: asyncio.StreamReader
        self._writer: asyncio.StreamWriter
        self._queue: asyncio.Queue = queue
        self._keep_running: bool = True
    
    @log('Connected to server') # type: ignore
    async def open_connection(self):
        self._reader, self._writer = await asyncio.open_connection(
                self.host, self.port)
    
    @log('Received data from server') # type: ignore
    async def _read_socket(self) -> str:
        if not self._reader:
            raise ConnectionError('No established connection to server')
        return (await self._reader.read(self.max_package_size)).decode(self.encoding)
    

    async def read(self) -> dict | None:
        commands_str: str = await self._read_socket()
        if not commands_str:
            return 
        try:
            return loads(commands_str)
        except JSONDecodeError:
            log(f'Failed to decode command: {commands_str}')


    async def run(self):
        await self.open_connection()
        while self._keep_running:
            command = await self.read()
            if not command:
                continue
            with log(f'Put command {command} into queue'): # type: ignore
                await self._queue.put(command)
        self._writer.close()
        await self._writer.wait_closed()
        log(f'Stopped listening to the server {self.host}:{self.port}')


    def stop(self):
        self._keep_running = False




