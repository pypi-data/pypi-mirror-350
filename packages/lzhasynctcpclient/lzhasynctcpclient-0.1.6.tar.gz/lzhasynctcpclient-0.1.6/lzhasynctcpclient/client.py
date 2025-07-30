import threading
import asyncio
import struct
import logging
from lzhgetlogger import get_logger

logger = get_logger(level = logging.WARNING)

class AsyncTcpClient:
    def __init__(
        self,
        host: str = '127.0.0.1',
        port: int = 9000,
        on_message=None,
        on_connect=None,
        heartbeat_require_response: bool= False,
        heartbeat_interval: int = 1,
        reconnect_interval: int = 1,
        heartbeat_message: str = "__PING__",
        name: str = 'AsyncTcpClient',
    ):
        self._host = host
        self._port = port
        self._on_message = on_message
        self._on_connect = on_connect
        self._heartbeat_interval = heartbeat_interval
        self._reconnect_interval = reconnect_interval
        self._heartbeat_message = heartbeat_message
        self._heartbeat_require_response = heartbeat_require_response
        self._name = name

        self._latest_message = ''
        self._loop = None
        self._writer = None
        self._reader = None
        self._stop_event = threading.Event()

        def run():
            self._loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._loop)
            while not self._stop_event.is_set():
                try:
                    self._loop.run_until_complete(self._main_loop())
                except Exception as e:
                    logger.error(f"Event loop error: {e}")
                    logger.info(f"Reconnecting in {self._reconnect_interval} seconds...")
                    import time
                    time.sleep(self._reconnect_interval)

            self._loop.close()

        self._thread = threading.Thread(target=run, name=f"Thread-{self._name}", daemon=True)

    def start(self):
        if self._thread and not self._thread.is_alive():
            self._thread.start()
            logger.info(f"Thread started")

    def stop(self):
        self._stop_event.set()
        if self._loop:
            self._loop.call_soon_threadsafe(self._loop.stop)
        logger.info(f"Stopped client")

    def send(self, message: str):
        try:
            if self._loop and self._writer and not self._writer.is_closing():
                asyncio.run_coroutine_threadsafe(self._send(message), self._loop)
        except Exception as e:
            logger.error(f"Failed to send message: {e}")

    @property
    def latest_message(self):
        return self._latest_message

    async def _main_loop(self):
        while not self._stop_event.is_set():
            try:
                logger.info(f"Connecting to {self._host}:{self._port}")
                self._reader, self._writer = await asyncio.open_connection(self._host, self._port)
                logger.info(f"Connected to server")
                if self._on_connect:
                    self._on_connect()
                self._heartbeat_timeout_event = asyncio.Event()

                tasks = [
                    asyncio.create_task(self._recv_loop()),
                    asyncio.create_task(self._heartbeat_loop()),
                ]
                await asyncio.wait(tasks, return_when=asyncio.FIRST_EXCEPTION)
            except Exception as e:
                logger.warning(f"Connection failed: {e}")
            finally:
                if self._writer:
                    self._writer.close()
                    await self._writer.wait_closed()
                self._writer = None
                self._reader = None
                if not self._stop_event.is_set():
                    logger.info(f"Reconnecting in {self._reconnect_interval} seconds...")
                    await asyncio.sleep(self._reconnect_interval)

    async def _send(self, message: str):
        try:
            data = message.encode('utf-8')
            packet = struct.pack(">I", len(data)) + data
            self._writer.write(packet)
            await self._writer.drain()
            await asyncio.sleep(0)
        except Exception as e:
            logger.error(f"Send error: {e}")
        
    async def _recv_loop(self):
        try:
            while not self._writer.is_closing():
                header = await self._reader.readexactly(4)
                length = struct.unpack(">I", header)[0]
                data = await self._reader.readexactly(length)
                message = data.decode('utf-8')
                self._latest_message = message
                if message == self._heartbeat_message:
                    self._heartbeat_timeout_event.clear()
                else:
                    logger.info(f"Received message: {message}")
                    if self._on_message:
                        result = self._on_message(message)
                        if asyncio.iscoroutine(result):
                            await result
                await asyncio.sleep(0)
        except asyncio.IncompleteReadError:
            logger.warning(f"Connection closed by server")
        except Exception as e:
            logger.error(f"Receive error: {e}")
        
    async def _heartbeat_loop(self):
        try:
            while not self._writer.is_closing():
                await asyncio.sleep(self._heartbeat_interval)
                if self._heartbeat_timeout_event.is_set() and self._heartbeat_require_response:
                    raise Exception("Heartbeat lost")
                await self._send(f'{self._heartbeat_message}')
                self._heartbeat_timeout_event.set()
                await asyncio.sleep(0)
        except Exception as e:
            logger.error(f"Heartbeat error: {e}")
            raise
