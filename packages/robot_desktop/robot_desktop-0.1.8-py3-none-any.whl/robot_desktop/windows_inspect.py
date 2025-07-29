import asyncio
import base64
import json
import logging
import os
import sys
import time
import typing
import uuid
from io import BytesIO
from threading import Thread
from typing import Literal

import psutil
import uiautomation
import websocket as websocket_client
import websockets
import xpath
from PIL import ImageGrab
from pynput import mouse, keyboard
from pyrect import Rect
from robot_base import RectangleWindow, TipWindow
from websockets.legacy.server import WebSocketServerProtocol

from .find_by_xpath import ControlNode


class InspectServer(object):
    def __init__(self, port: int, web_native_port: int, log_path: str):
        self.control_cache = {}
        self.port = port
        self.rectangle_window = RectangleWindow(
            100, 100, 300, 400, text="", color="red"
        )
        self.pick_mode: Literal["auto", "windows", "web", "java"] = "auto"
        self.last_rect: Rect = Rect(0, 0, 0, 0)
        self.last_x = 0
        self.last_y = 0
        self.inspect = False
        self.cancel = False
        self.tip_window = TipWindow(
            text="按下 Esc 退出拾取 \n按下Ctrl并点击鼠标左键拾取元素 \n按下 F1 切换 Web 元素拾取模式 \n按下 F2 切换 Windows 应用拾取模式 \n按下 F3 切换 Java 应用拾取模式 \n按下 F4 切换 自动模式",
            width=300,
            height=100,
        )
        self.ctrl_press = False
        self.tip_window.hide()
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
        uiautomation.Logger.SetLogFile(log_path)

        self.mouse_listener = None
        self.keyboard_listener = None

        self.web_conn_url = f"ws://127.0.0.1:{web_native_port}/ws"
        self.web_conn: typing.Optional[websocket_client.WebSocket, None] = None

        self.message_id = ""
        self.websocket_conn = None
        thread = Thread(target=self.connect_web_socket)
        thread.start()

    async def start(self) -> None:
        uiautomation.GetRootControl()
        async with websockets.serve(self.handler, "localhost", self.port):
            await asyncio.Future()  # run forever

    def connect_web_socket(self):
        try:
            self.web_conn = websocket_client.create_connection(self.web_conn_url)
        except Exception as e:
            self.logger.info(e)

    async def handler(self, websocket: WebSocketServerProtocol):
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
                result = method(**client_message["data"])
                if result is not None:
                    await websocket.send(
                        json.dumps(
                            {
                                "message_id": client_message["message_id"],
                                "result": "ok",
                                "data": result,
                            }
                        )
                    )
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

    def get_root(self) -> list:
        self.control_cache.clear()

        desktop = uiautomation.GetRootControl()
        dump_children = []
        children = desktop.GetChildren()
        for index, control in enumerate(children, 1):
            dump_control = self.cache_dump_control(index, control)
            dump_children.append(dump_control)
        return dump_children

    def get_children(self, control_id: str) -> list:
        if control_id in self.control_cache:
            current = self.control_cache[control_id]
            dump_children = []
            children = current.GetChildren()
            for index, control in enumerate(children, 0):
                dump_control = self.cache_dump_control(index, control)
                dump_children.append(dump_control)
            return dump_children
        else:
            return []

    def highlight_current_control(self, control_id: str):
        if control_id in self.control_cache:
            current = self.control_cache[control_id]
            self.rectangle_window.update_position(
                current.BoundingRectangle.left,
                current.BoundingRectangle.top,
                current.BoundingRectangle.width(),
                current.BoundingRectangle.height(),
                text=current.LocalizedControlType,
            )
            self.rectangle_window.highlight()

    def highlight_control(self):
        self.tip_window.show()
        self.start_mouse_keyboard_listener()
        self.inspect = True
        self.cancel = False
        self.check_web_conn()
        while self.inspect:
            try:
                x, y = uiautomation.GetCursorPos()
                if abs(x - self.last_x) < 2 and abs(y - self.last_y) < 2:
                    continue
                self.last_x = x
                self.last_y = y
                control = find_control_from_point(
                    x, y, uiautomation.ControlFromCursor().GetTopLevelControl()
                )
                if control.ProcessId == os.getpid():
                    continue
                if control is None:
                    self.rectangle_window.hide_all()
                    continue
                if self.pick_mode == "auto":
                    in_web, rect, text = self.is_web_process(control, x, y)
                    if in_web:
                        self.show_highlight_rect(rect, text)
                    else:
                        self.show_highlight_rect(
                            Rect(
                                control.BoundingRectangle.left,
                                control.BoundingRectangle.top,
                                control.BoundingRectangle.width(),
                                control.BoundingRectangle.height(),
                            ),
                            control.LocalizedControlType,
                        )
                elif self.pick_mode == "windows":
                    self.show_highlight_rect(
                        Rect(
                            control.BoundingRectangle.left,
                            control.BoundingRectangle.top,
                            control.BoundingRectangle.width(),
                            control.BoundingRectangle.height(),
                        ),
                        control.LocalizedControlType,
                    )
                elif self.pick_mode == "web":
                    in_web, rect, text = self.is_web_process(control, x, y)
                    if in_web:
                        self.show_highlight_rect(rect, text)
                    else:
                        self.rectangle_window.hide_all()
                        continue
                elif self.pick_mode == "java":
                    pass
            except Exception as error:
                self.logger.exception(error)
            finally:
                time.sleep(0.2)
        if self.cancel:
            raise Exception("cancel")
        else:
            control = find_control_from_point(
                self.last_x,
                self.last_y,
                uiautomation.ControlFromCursor().GetTopLevelControl(),
            )
            if self.pick_mode == "auto":
                in_web, element_info = self.get_web_element_info(
                    control, self.last_x, self.last_y
                )
                if in_web:
                    return element_info
                else:
                    return self.get_windows_control_info(control)
            elif self.pick_mode == "web":
                in_web, element_info = self.get_web_element_info(
                    control, self.last_x, self.last_y
                )
                if in_web:
                    return element_info
                else:
                    raise Exception("不是Web元素")
            elif self.pick_mode == "windows":
                return self.get_windows_control_info(control)
            elif self.pick_mode == "java":
                raise Exception("暂不支持")

    def show_highlight_rect(self, rect, text):
        if self.last_rect == rect:
            return
        else:
            self.last_rect = rect
            self.rectangle_window.update_position(
                rect.left,
                rect.top,
                rect.width,
                rect.height,
                text=text,
            )

    def on_mouse_click(self, x, y, button, pressed):
        if pressed and button == mouse.Button.left and self.ctrl_press:
            self.last_x = x
            self.last_y = y
            self.tip_window.hide()
            self.rectangle_window.hide_all()
            self.mouse_listener.stop()
            self.keyboard_listener.stop()
            self.ctrl_press = False
            self.inspect = False
            self.cancel = False

    def on_key_press(self, key):
        if key == keyboard.Key.esc:
            self.tip_window.hide()
            self.rectangle_window.hide_all()
            self.mouse_listener.stop()
            self.keyboard_listener.stop()
            self.inspect = False
            self.cancel = True
        elif self.ctrl_press and (
            key == keyboard.Key.shift
            or key == keyboard.Key.shift_l
            or key == keyboard.Key.shift_r
        ):
            self.tip_window.hide()
            self.rectangle_window.hide_all()
            self.mouse_listener.stop()
            self.keyboard_listener.stop()
            self.ctrl_press = False
            self.inspect = False
            self.cancel = False
        elif key == keyboard.Key.f1:
            self.pick_mode = "web"
        elif key == keyboard.Key.f2:
            self.pick_mode = "windows"
        elif key == keyboard.Key.f3:
            self.pick_mode = "java"
        elif key == keyboard.Key.f4:
            self.pick_mode = "auto"
        elif (
            key == keyboard.Key.ctrl
            or key == keyboard.Key.ctrl_l
            or key == keyboard.Key.ctrl_r
        ):
            self.ctrl_press = True

    def on_key_release(self, key):
        if key == keyboard.Key.ctrl:
            self.ctrl_press = False

    def start_mouse_keyboard_listener(self):
        self.mouse_listener = mouse.Listener(on_click=self.on_mouse_click)
        self.keyboard_listener = keyboard.Listener(
            on_press=self.on_key_press, on_release=self.on_key_release
        )
        self.mouse_listener.start()
        self.keyboard_listener.start()

    def check_control(self, element_info):
        element_info = json.loads(element_info)
        if element_info["type"] == "windows":
            element_xpath = element_info.get("xpath", "")
            root = ControlNode(uiautomation.GetRootControl())
            controls = xpath.find(element_xpath, root)
            if len(controls) == 0:
                raise Exception("元素未找到")
            else:
                for i in range(min(len(controls), 3)):
                    control = controls[i].current_control
                    self.rectangle_window.update_position(
                        control.BoundingRectangle.left,
                        control.BoundingRectangle.top,
                        control.BoundingRectangle.width(),
                        control.BoundingRectangle.height(),
                        text=control.LocalizedControlType,
                    )
                    self.rectangle_window.highlight()
                return len(controls)
        elif element_info["type"] == "web":
            frame_xpath = element_info.get("iframeXpath", "")
            element_xpath = element_info.get("xpath", "")
            self.check_web_conn()
            count_info = self.get_element_count(element_xpath, frame_xpath)
            count = count_info["count"]
            tag = count_info["tag"]
            if count == 0:
                raise Exception("元素未找到")
            else:
                if not self.is_element_on_viewport(element_xpath, frame_xpath):
                    self.scroll_to_element(element_xpath, frame_xpath)
                rect_array = self.get_element_rect(element_xpath, frame_xpath)
                web_document = get_document_control_from_root()
                if web_document:
                    top = web_document.BoundingRectangle.top
                    left = web_document.BoundingRectangle.left
                    for i in range(min(len(rect_array), 3)):
                        rect = rect_array[i]
                        self.rectangle_window.update_position(
                            int(rect["x"]) + left,
                            int(rect["y"]) + top,
                            int(rect["width"]),
                            int(rect["height"]),
                            text=tag,
                        )
                        self.rectangle_window.highlight()
                return count

    def get_select_control(self, control_id: str):
        if control_id in self.control_cache:
            control: uiautomation.Control = self.control_cache[control_id]
            return self.get_windows_control_info(control)
        else:
            raise Exception("元素未找到")

    @staticmethod
    def get_control_index(control: uiautomation.Control) -> int:
        sibling = control.GetPreviousSiblingControl()
        index = 1
        while sibling is not None:
            if sibling.ControlTypeName == control.ControlTypeName:
                index += 1
            sibling = sibling.GetPreviousSiblingControl()
        return index

    def cache_dump_control(self, index: int, control: uiautomation.Control):
        control_id = uuid.uuid4().hex
        self.control_cache[control_id] = control
        return {
            "id": control_id,
            "automationId": control.AutomationId,
            "name": control.Name,
            "localizeControlType": control.LocalizedControlType,
            "controlTypeName": control.ControlTypeName,
            "className": control.ClassName,
            "frameworkId": control.FrameworkId,
            "index": index,
        }

    def get_windows_control_info(self, control):
        control_path = []
        control_id = uuid.uuid4().hex
        pic = ImageGrab.grab(
            (
                control.BoundingRectangle.left + 1,
                control.BoundingRectangle.top + 1,
                control.BoundingRectangle.left + control.BoundingRectangle.width() - 1,
                control.BoundingRectangle.top + control.BoundingRectangle.height() - 1,
            )
        )
        display_name = get_control_display_name(
            control.Name, control.LocalizedControlType
        )
        image_data = BytesIO()
        pic.save(image_data, format="PNG")
        image_data_bytes = image_data.getvalue()
        encoded_image = base64.b64encode(image_data_bytes).decode("utf-8")
        desktop = uiautomation.GetRootControl()
        process = psutil.Process(control.ProcessId)
        while control and not uiautomation.ControlsAreSame(control, desktop):
            control_path.append(self.generate_windows_control_info(control))
            control = control.GetParentControl()
        control_path.reverse()
        return {
            "id": control_id,
            "type": "windows",
            "processName": get_display_name(process.name()),
            "name": display_name,
            "image": encoded_image,
            "nodes": control_path,
        }

    def generate_windows_control_info(self, control):
        index = self.get_control_index(control)
        attributes = [
            {
                "name": "automationId",
                "value": control.AutomationId,
                "isEnable": False,
                "op": "EqualTo",
            },
            {
                "name": "className",
                "value": control.ClassName,
                "isEnable": False,
                "op": "EqualTo",
            },
            {
                "name": "name",
                "value": control.Name,
                "isEnable": len(control.Name) > 0,
                "op": "EqualTo",
            },
            {
                "name": "index",
                "value": index,
                "isEnable": len(control.Name) == 0,
                "op": "EqualTo",
            },
        ]
        return {
            "displayName": get_control_display_name(
                control.Name, control.LocalizedControlType
            ),
            "name": control.ControlTypeName,
            "isEnable": True,
            "attributes": attributes,
        }

    def is_web_process(self, control, x, y):
        try:
            pro = psutil.Process(control.ProcessId)
            if (
                pro.name() == "chrome.exe"
                or pro.name() == "firefox.exe"
                or pro.name() == "msedge.exe"
                or pro.name() == "360se.exe"
            ):
                web_document = control.GetTopLevelControl().DocumentControl(
                    searchDepth=10
                )
                if web_document:
                    top = web_document.BoundingRectangle.top
                    left = web_document.BoundingRectangle.left
                    tab_width = web_document.BoundingRectangle.width()
                    tab_height = web_document.BoundingRectangle.height()
                    x_in_web = x - left
                    y_in_web = y - top
                    if 0 < x_in_web < tab_width and 0 < y_in_web < tab_height:
                        web_element = self.get_hover_element(
                            int(x_in_web), int(y_in_web)
                        )
                        if web_element != 0:
                            return (
                                True,
                                Rect(
                                    int(web_element["bounding"]["x"] + left),
                                    int(web_element["bounding"]["y"] + top),
                                    int(web_element["bounding"]["width"]),
                                    int(web_element["bounding"]["height"]),
                                ),
                                web_element["tag"],
                            )
        except Exception:
            pass

        return False, Rect(0, 0, 0, 0), ""

    def get_web_element_info(self, control, x: float, y: float):
        try:
            pro = psutil.Process(control.ProcessId)
            if (
                pro.name() == "chrome.exe"
                or pro.name() == "firefox.exe"
                or pro.name() == "msedge.exe"
                or pro.name() == "360se.exe"
            ):
                web_document = control.GetTopLevelControl().DocumentControl()
                if web_document:
                    top = web_document.BoundingRectangle.top
                    left = web_document.BoundingRectangle.left
                    tab_width = web_document.BoundingRectangle.width()
                    tab_height = web_document.BoundingRectangle.height()
                    x_in_web = x - left
                    y_in_web = y - top
                    if 0 < x_in_web < tab_width and 0 < y_in_web < tab_height:
                        web_element = self.get_hover_element(
                            int(x_in_web), int(y_in_web)
                        )
                        if web_element != 0:
                            pic = ImageGrab.grab(
                                (
                                    int(web_element["bounding"]["x"] + left) + 1,
                                    int(web_element["bounding"]["y"] + top) + 1,
                                    int(
                                        web_element["bounding"]["x"]
                                        + left
                                        + web_element["bounding"]["width"]
                                    )
                                    - 1,
                                    int(
                                        web_element["bounding"]["y"]
                                        + top
                                        + web_element["bounding"]["height"]
                                    )
                                    - 1,
                                )
                            )
                            image_data = BytesIO()
                            pic.save(image_data, format="PNG")
                            image_data_bytes = image_data.getvalue()
                            encoded_image = base64.b64encode(image_data_bytes).decode(
                                "utf-8"
                            )
                            element_info = self.get_selected_element(
                                int(x_in_web), int(y_in_web)
                            )
                            nodes = (
                                element_info["nodes"] if element_info["nodes"] else []
                            )
                            for node in nodes:
                                node["displayName"] = node["name"]
                            iframe_nodes = (
                                element_info["iframeNodes"]
                                if element_info["iframeNodes"]
                                else []
                            )
                            for node in iframe_nodes:
                                node["displayName"] = node["name"]
                            nodes.reverse()
                            iframe_nodes.reverse()
                            web_element_info = {
                                "id": uuid.uuid4().hex,
                                "processName": (
                                    get_display_name(
                                        element_info["pageTitle"]
                                        if element_info["pageTitle"]
                                        else element_info["pageUrl"]
                                    )
                                ),
                                "name": get_control_display_name(
                                    element_info["text"], element_info["tag"]
                                ),
                                "type": "web",
                                "image": encoded_image,
                                "nodes": nodes,
                                "xpath": element_info["xpath"],
                                "xpathAuto": True,
                                "iframeNodes": iframe_nodes,
                                "iframeXPath": element_info["iframeXPath"],
                                "iframeXpathAuto": True,
                            }
                            return True, web_element_info
        except Exception:
            pass

        return False, None

    def get_hover_element(self, x: int, y: int):
        return self.request_to_native_host(
            {
                "name": "GetHoveringElementRequest",
                "parameters": {"x": x, "y": y},
                "frameInfos": [],
            }
        )

    def get_selected_element(self, x: int, y: int):
        return self.request_to_native_host(
            {
                "name": "SelectElementRequest",
                "parameters": {"x": x, "y": y},
                "frameInfos": [],
            }
        )

    def get_element_count(self, xpath: str, iframe_xpath: str):
        return self.request_to_native_host(
            {
                "name": "QueryElementCountByXpathRequest",
                "parameters": {
                    "selector": {
                        "name": "",
                        "xpath": xpath,
                        "iframeXPath": iframe_xpath,
                    }
                },
            }
        )

    def get_element_rect(self, xpath: str, iframe_xpath: str):
        return self.request_to_native_host(
            {
                "name": "GetElementRectRequest",
                "parameters": {
                    "selector": {
                        "name": "",
                        "xpath": xpath,
                        "iframeXPath": iframe_xpath,
                    }
                },
            }
        )

    def is_element_on_viewport(self, xpath: str, iframe_xpath: str):
        return self.request_to_native_host(
            {
                "name": "IsElementOnViewportRequest",
                "parameters": {
                    "selector": {
                        "name": "",
                        "xpath": xpath,
                        "iframeXPath": iframe_xpath,
                    }
                },
            }
        )

    def scroll_to_element(self, xpath: str, iframe_xpath: str):
        return self.request_to_native_host(
            {
                "name": "ScrollToElementRequest",
                "parameters": {
                    "selector": {
                        "name": "",
                        "xpath": xpath,
                        "iframeXPath": iframe_xpath,
                    }
                },
            }
        )

    def request_to_native_host(self, data):
        request_id = str(uuid.uuid1())
        data["requestId"] = request_id
        if self.web_conn is None or not self.web_conn.connected:
            raise Exception("web_conn is not connected")
        try:
            self.web_conn.send(json.dumps(data))
        except Exception as e:
            self.web_conn = websocket_client.create_connection(self.web_conn_url)
            self.web_conn.send(json.dumps(data))
        while True:
            resp = self.web_conn.recv()
            resp_data = json.loads(resp)
            self.logger.info(resp_data)
            if "requestId" in resp_data and resp_data["requestId"] == request_id:
                return resp_data["result"]

    def check_web_conn(self):
        try:
            if self.web_conn is None or not self.web_conn.connected:
                self.web_conn = websocket_client.create_connection(self.web_conn_url)
        except Exception:
            pass


def find_control_from_point(x, y, control=None):
    if len(control.GetChildren()) == 0:
        return control
    controls = [
        node
        for node in control.GetChildren()
        if node.BoundingRectangle and node.BoundingRectangle.contains(x, y)
    ]
    if len(controls) == 0:
        return control
    results = []
    for control in controls:
        result = find_control_from_point(x, y, control)
        if result:
            results.append(result)
    if len(results) > 0:
        sorted_results = sorted(
            results,
            key=lambda node: node.BoundingRectangle.width()
            * node.BoundingRectangle.height(),
        )
        return sorted_results[0]
    return None


def get_document_control_from_root():
    root = uiautomation.GetRootControl()
    controls = root.GetChildren()
    for control in controls:
        pro = psutil.Process(control.ProcessId)
        if (
            pro.name() == "chrome.exe"
            or pro.name() == "firefox.exe"
            or pro.name() == "msedge.exe"
            or pro.name() == "360se.exe"
        ):
            return control.DocumentControl()


def get_control_display_name(text, tag):
    if len(text) == 0:
        return tag
    elif len(text) > 30:
        return text[:30] + "...[" + tag + "]"
    else:
        return text + "[" + tag + "]"


def get_display_name(text):
    if len(text) <= 30:
        return text
    return text[:30] + "..."


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("参数错误", file=sys.stderr)
    else:
        inspect_server = InspectServer(int(sys.argv[1]), int(sys.argv[2]), sys.argv[3])
        asyncio.run(inspect_server.start())
