import os
import time

import robot_basic
import uiautomation
import xpath
from robot_base import log_util

from ..find_by_xpath import ControlNode
from ..index import open_app, window_activate, get_elements, get_element
from ..application import find_controls_by_id


def setup_function():
    os.environ["project_path"] = (
        r"D:\Program Files\GoBot\data\ca990806-ec6b-4d6e-99d5-aab33f4969b1\gobot"
    )
    log_util.Logger("", "INFO")


def teardown():
    pass


def test_open_app():
    open_app(
        executable_path=r"D:\code\GoBot\gobot\build\bin\GoBot.exe",
        work_dir=r"D:\code\GoBot\gobot\build\bin",
        style="max",
        is_admin=True,
    )


def test_find_controls_by_id():
    controls = find_controls_by_id("67ba964633e041bdb52c176846fdf5d0")
    print(controls)


def test_window_activate():
    window_activate(
        windows_element={
            "name": "导航[工具栏]",
            "xpath": "/WindowControl[@name='微信']",
            "frameXpath": None,
        },
        code_block_extra_data={
            "exception": {
                "exception": "error",
                "retry": "False",
                "retry_count": 1,
                "retry_interval": 1,
            },
            "code_map_id": "9jl99FTcDT_Pojvn",
            "code_line_number": "1",
            "code_file_name": "主流程",
            "code_block_name": "激活窗口",
        },
    )


def test_send_keys():
    time.sleep(2)
    uiautomation.SendKeys("中外")


def test_find_by_xpath():
    root = ControlNode(uiautomation.GetRootControl())

    result = xpath.find(
        "/PaneControl[@name='任务栏']/PaneControl[@name='DesktopWindowXamlSource']/PaneControl[1]/PaneControl[1]",
        root,
    )
    print(len(result))


def test_find_child_element():
    for element in get_elements(
        windows_element={
            "name": "所有的组",
            "xpath": "/WindowControl[@name='公众号']/PaneControl[1]/DocumentControl[1]/GroupControl[1]/GroupControl[1]/GroupControl[1]/GroupControl[1]/GroupControl[3]/GroupControl[2]/GroupControl",
            "frameXpath": None,
        },
        code_block_extra_data={
            "exception": {
                "exception": "error",
                "retry": "False",
                "retry_count": 1,
                "retry_interval": 1,
            },
            "code_map_id": "yLrpLWpQHp-JQBDS",
            "code_line_number": "3",
            "code_file_name": "主流程",
            "code_block_name": "循环桌面相似元素",
        },
    ):
        text_element = get_element(
            parent_type="parent_element",
            parent_control=element,
            windows_element={
                "name": "阅读点赞数",
                "xpath": "/GroupControl[1]/GroupControl[1]/GroupControl[1]/TextControl[1]",
                "frameXpath": None,
            },
            code_block_extra_data={
                "exception": {
                    "exception": "error",
                    "retry": "False",
                    "retry_count": 1,
                    "retry_interval": 1,
                },
                "code_map_id": "H3D4Ix4FwNpA2xQi",
                "code_line_number": "4",
                "code_file_name": "主流程",
                "code_block_name": "查找元素",
            },
        )
        robot_basic.print_log(
            log_level="info",
            expression=text_element.Name,
            code_block_extra_data={
                "code_map_id": "gUmwCR1sg6dV4glt",
                "code_line_number": "5",
                "code_file_name": "主流程",
                "code_block_name": "打印日志",
            },
        )
    # EndLoop
