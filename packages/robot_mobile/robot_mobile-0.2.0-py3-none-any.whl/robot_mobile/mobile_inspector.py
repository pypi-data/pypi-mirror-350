import asyncio
import base64
import io
import json
import logging
import sys
import time
import typing
from threading import Thread

import uiautomator2
import websockets
from robot_mobile.uidumplib import android_hierarchy_to_json
from websockets.legacy.server import WebSocketServerProtocol
from websockets.protocol import State


class InspectServer(object):
    def __init__(self, port, log_path: str):
        self.port = port
        self.log_path = log_path
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        console_handler = logging.StreamHandler(stream=sys.stdout)
        console_handler.setFormatter(formatter)
        th = logging.FileHandler(filename=log_path, encoding="utf-8")
        th.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        self.logger.addHandler(th)
        self.message_id = ""
        self.websocket_conn: typing.Union[WebSocketServerProtocol, None] = None
        self.monitoring = False
        self.device: typing.Union[uiautomator2.Device, None] = None
        self.last_dump_hierarchy = None

    async def start(self) -> None:
        async with websockets.serve(self.handler, "localhost", self.port):
            await asyncio.Future()  # run forever

    async def handler(self, websocket):
        async for message in websocket:
            await self.process(message, websocket)

    async def process(self, message, websocket: WebSocketServerProtocol):
        self.logger.info(f"收到请求:{message}")
        client_message = json.loads(message)
        self.message_id = client_message["message_id"]
        self.websocket_conn = websocket
        try:
            if "method" not in client_message:
                raise Exception("No method in client message")
            method = getattr(self, client_message["method"])
            if method:
                await method(**client_message["data"])
            else:
                raise Exception(f"{client_message['method']}方法未定义")
        except Exception as e:
            self.logger.exception(e)
            await websocket.send(
                json.dumps(
                    {
                        "message_id": client_message["message_id"],
                        "result": "error",
                        "reason": str(e),
                    }
                )
            )

    async def start_monitor(self):
        self.monitoring = True
        self.logger.info("开始监听")
        self.device = uiautomator2.connect()
        thread = Thread(target=self.monitor_mobile)
        thread.start()

    def monitor_mobile(self):
        while self.monitoring and self.websocket_conn.state == State.OPEN:
            try:
                result = self.device.dump_hierarchy()
                if result != self.last_dump_hierarchy:
                    self.last_dump_hierarchy = result
                    json_data = android_hierarchy_to_json(result.encode("utf-8"))
                    self.logger.info("更新UI")
                    screen_image = self.device.screenshot()
                    buffered = io.BytesIO()
                    screen_image.save(buffered, format="PNG")
                    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
                    response = json.dumps(
                        {
                            "message_id": self.message_id,
                            "result": "ok",
                            "dump_hierarchy": json_data,
                            "image_data": img_str,
                        }
                    )
                    asyncio.run(self.websocket_conn.send(response))
            except:
                self.logger.exception("监听异常")

            time.sleep(2)


if __name__ == "__main__":
    inspect_server = InspectServer(port=9999, log_path=r"D:\ProgramData\tmp\mobile.log")
    asyncio.run(inspect_server.start())
