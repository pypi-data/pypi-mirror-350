import asyncio
from http.server import HTTPServer
from typing import Optional
import threading

from promptlab._config import TracerConfig
from promptlab.studio.api import StudioApi
from promptlab.studio.async_api import AsyncStudioApi
from promptlab.studio.web import StudioWebHandler


class Studio:
    def __init__(self, tracer_config: TracerConfig):
        self.tracer_config = tracer_config

        self.web_server: Optional[HTTPServer] = None
        self.api_server = None  # Can be either StudioApi or AsyncStudioApi
        self.api_thread: Optional[threading.Thread] = None
        self.web_thread: Optional[threading.Thread] = None
        self.api_task = None  # For async operation

    def start_api_server(self, api_port: int):
        """Start the API server synchronously"""
        self.api_server = StudioApi(self.tracer_config)
        self.api_thread = threading.Thread(
            target=self.api_server.run, args=("localhost", api_port), daemon=True
        )

        self.api_thread.start()

    async def start_api_server_async(self, api_port: int):
        """Start the API server asynchronously"""
        self.api_server = AsyncStudioApi(self.tracer_config)
        await self.api_server.run("localhost", api_port)

    def start_web_server(self, web_port: int):
        """Start the web server in a separate thread"""
        self.web_server = HTTPServer(("localhost", web_port), StudioWebHandler)

        self.web_thread = threading.Thread(
            target=self.web_server.serve_forever, daemon=True
        )

        self.web_thread.start()

    def shutdown(self):
        """Shutdown all servers"""
        if self.web_server:
            self.web_server.shutdown()

        if self.web_thread and self.web_thread.is_alive():
            self.web_thread.join(timeout=5)

        if self.api_thread and self.api_thread.is_alive():
            self.api_thread.join(timeout=5)

        if self.api_task:
            self.api_task.cancel()

    def start(self, port: int = 8000):
        """Start the studio synchronously"""
        try:
            # Start API server first in a separate thread
            self.start_api_server(port + 1)

            # Start web server in separate thread
            self.start_web_server(port)

            print(f"Studio started at http://localhost:{port}")

            # Keep main thread alive until interrupted
            try:
                while True:
                    import time

                    time.sleep(1)
            except KeyboardInterrupt:
                print("\nShutting down servers...")
                self.shutdown()

        except Exception:
            self.shutdown()
            raise

    async def start_async(self, port: int = 8000):
        """Start the studio asynchronously"""
        try:
            # Start web server in a separate thread
            self.start_web_server(port)

            # Start API server asynchronously
            self.api_task = asyncio.create_task(self.start_api_server_async(port + 1))

            print(f"Studio started at http://localhost:{port}")

            # Keep the task running
            await self.api_task

        except asyncio.CancelledError:
            print("\nShutting down servers...")
            self.shutdown()
        except Exception as e:
            self.shutdown()
            raise e
