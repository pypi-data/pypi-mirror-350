import asyncio
import threading
import time
from abc import ABC
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn
from typing import Dict, AsyncGenerator
from pydantic import BaseModel
from sse_starlette.sse import EventSourceResponse
from pulsekit.hardwareinfo.hardware_info import HardwareInfo
from pulsekit.util.progress_reporter import ProgressReporter
from .plugin import PluginBase, PluginType
from .plugin_context import PluginContext

class RunRequest(BaseModel):
    env: Dict[str, str] = {}
    hardware_info: HardwareInfo
    args: Dict[str,str] = {}

class ParseRequest(BaseModel):
    output: str

class RemotePlugin(PluginBase, ABC):
    def __init__(self, host: str = "0.0.0.0", port: int = 8989):
        self.app = FastAPI()
        self.host = host
        self.port = port
        self.register_routes()

    def register_routes(self):
        @self.app.post("/run")
        async def run_plugin(req: RunRequest):
            context = PluginContext(env=req.env, hardware_info=req.hardware_info, args=req.args)
            progress = ProgressReporter()
            def run_with_result():
                output = self.run(context, progress)
                progress.mark_done(output)
            threading.Thread(target=run_with_result).start()
            return EventSourceResponse(self.report_progress(progress))

        @self.app.post("/install")
        async def install_deps(req: RunRequest):
            context = PluginContext(env=req.env, hardware_info=req.hardware_info, args=req.args)
            progress = ProgressReporter()
            def run_with_result():
                self.install_dependencies(context, progress)
                progress.mark_done()
            threading.Thread(target=run_with_result).start()
            return EventSourceResponse(self.report_progress(progress))

        @self.app.post("/parse")
        async def parse_result(req: ParseRequest):
            result = self.get_json_result(req.output)
            return JSONResponse(content={"result": result})

        @self.app.get("/health")
        async def health_check():
            return {"status": "running"}

    async def report_progress(self, progress: ProgressReporter) -> AsyncGenerator[str, None]:
        queue: asyncio.Queue[str] = asyncio.Queue()
        def listener():
            for prog, log in progress.stream_updates():
                loop.call_soon_threadsafe(queue.put_nowait, {"event": "progress", "data": f"{prog:.2f}"})
                if log:
                    loop.call_soon_threadsafe(queue.put_nowait, {"event": "log", "data": log})


        loop = asyncio.get_event_loop()
        # 把同步监听逻辑放到线程池中运行
        loop.run_in_executor(None, listener)

        while True:
            try:
                msg = await asyncio.wait_for(queue.get(), timeout=1.0)
                yield msg
            except asyncio.TimeoutError:
                pass

            if progress.is_done() and queue.empty():
                yield {"event":"done", "data":progress.get_result()}
                time.sleep(0.1)
                break

    def serve(self):
        uvicorn.run(self.app, host=self.host, port=self.port)

    def get_type(self) ->PluginType:
        return PluginType.Remote