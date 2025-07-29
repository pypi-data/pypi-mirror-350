import fnmatch
import json
import os
import re
import typing

from jinja2 import Template
from uiautomation import uiautomation, Control


def find_control_by_id(
    control_id: str, local_data=None
) -> typing.Optional[uiautomation.Control]:
    if local_data is None:
        local_data = {}
    project_path = os.environ["project_path"]
    selectors_path = os.path.join(project_path, "selector.json")
    with open(selectors_path, "r", encoding="utf8") as fp:
        selectors = json.load(fp)
        paths = selectors[control_id]["nodes"]
        tmpl = Template(json.dumps(paths))
        ret = tmpl.render(local_data)
        paths = json.loads(ret)
        if not paths or len(paths) == 0:
            return None
        else:
            return find_control(paths)


def find_control(control_path: list) -> typing.Optional[uiautomation.Control]:
    desktop = uiautomation.GetRootControl()
    control = desktop
    max_depth = 1
    for path in control_path:
        if path["isEnable"]:

            def compare_control(current, index):
                for attr in path["attributes"]:
                    if attr["name"] != "index" and attr["isEnable"]:
                        if not compare_attribute(
                            get_control_attribute(current, attr["name"]),
                            attr["value"],
                            attr["op"],
                        ):
                            return False
                return True

            index_attr = list(
                filter(lambda attr: attr["name"] == "index", path["attributes"])
            )[0]
            control = uiautomation.FindControl(
                control,
                compare=compare_control,
                maxDepth=max_depth,
                foundIndex=int(index_attr["value"]) if index_attr["isEnable"] else 1,
            )
            max_depth = 1
        else:
            max_depth += 1
        if not control:
            return None
    return control


def find_controls_by_id(control_id: str, local_data=None) -> typing.Optional[list]:
    if local_data is None:
        local_data = {}
    project_path = os.environ["project_path"]
    selectors_path = os.path.join(project_path, "selector.json")
    with open(selectors_path, "r", encoding="utf8") as fp:
        selectors = json.load(fp)
        paths = selectors[control_id]["nodes"]
        tmpl = Template(json.dumps(paths))
        ret = tmpl.render(local_data)
        paths = json.loads(ret)
        if not paths or len(paths) == 0:
            return None
        else:
            return find_controls(paths)


def find_controls(control_path: list) -> typing.Optional[list]:
    desktop = uiautomation.GetRootControl()
    return find_controls_recursion(desktop, control_path, 0, 1)


def find_controls_recursion(
    control: Control, control_path: list, start_index: int, max_depth: int
):
    if control is None:
        return []
    while start_index < len(control_path) and not control_path[start_index]["isEnable"]:
        start_index += 1
        max_depth += 1
    if start_index == len(control_path):
        return [control]
    path = control_path[start_index]

    def compare_control(current, index):
        for attr in path["attributes"]:
            if attr["name"] != "index" and attr["isEnable"]:
                if not compare_attribute(
                    get_control_attribute(current, attr["name"]),
                    attr["value"],
                    attr["op"],
                ):
                    return False
        return True

    controls = []
    index_attr = list(filter(lambda attr: attr["name"] == "index", path["attributes"]))[
        0
    ]
    for control in find_controls_base(
        control,
        compare_control,
        max_depth,
        False,
        int(index_attr["value"]) if index_attr["isEnable"] else -1,
    ):
        ctrs = find_controls_recursion(control, control_path, start_index + 1, 1)
        controls.extend(ctrs)
    return controls


def find_controls_base(
    control: Control,
    compare: typing.Callable[[Control, int], bool],
    max_depth: int = 0xFFFFFFFF,
    find_from_self: bool = False,
    found_index: int = -1,
):
    """
    control: `Control` or its subclass.
    compare: Callable[[Control, int], bool], function(control: Control, depth: int) -> bool.
    maxDepth: int, enum depth.
    findFromSelf: bool, if False, do not compare self.
    foundIndex: int, starts with 1, >= 1.
    Return `Control` subclass or None if not find.
    """
    found_count = 0
    if not control:
        control = uiautomation.GetRootControl()
    traverse_count = 0
    controls = []
    for child, depth in uiautomation.WalkControl(control, find_from_self, max_depth):
        traverse_count += 1
        if compare(child, depth):
            found_count += 1
            if found_index == -1 or found_count == found_index:
                child.traverseCount = traverse_count
                controls.append(child)
    return controls


def compare_attribute(value1: str, value2: str, match: str):
    if match == "EqualTo":
        return value1 == value2
    elif match == "Contains":
        return value1.__contains__(value2)
    elif match == "StartsWith":
        return value1.startswith(value2)
    elif match == "EndsWith":
        return value1.endswith(value2)
    elif match == "WildCard":
        return fnmatch.fnmatch(value1, value2)
    else:
        re.match(value1, value2)


def get_control_attribute(control: uiautomation.Control, attribute_name: str) -> str:
    if attribute_name == "automationId":
        return control.AutomationId
    elif attribute_name == "name":
        return control.Name
    elif attribute_name == "controlTypeName":
        return control.ControlTypeName
    elif attribute_name == "className":
        return control.ClassName
    elif attribute_name == "frameworkId":
        return control.FrameworkId
    else:
        return ""
