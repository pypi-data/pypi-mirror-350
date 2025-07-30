from xml.dom import Node

import uiautomation
import xpath
from robot_base import TemporaryException


def find_element_by_xpath(element, parent_control=None, **kwargs):
    element_xpath = element.get("xpath", "")
    if parent_control:
        root = ControlNode(parent_control)
    else:
        root = ControlNode(uiautomation.GetRootControl())
    controls = xpath.find(element_xpath, root)
    if len(controls) == 0:
        raise TemporaryException(f"{element.get('name', '')}:元素未找到")
    return controls[0].current_control


def find_elements_by_xpath(element, parent_control=None, **kwargs):
    element_xpath = element.get("xpath", "")
    if parent_control:
        root = ControlNode(parent_control)
    else:
        root = ControlNode(uiautomation.GetRootControl())
    controls = xpath.find(element_xpath, root)
    return [control.current_control for control in controls]


class ControlNode(Node):
    def __init__(self, control: uiautomation.Control):
        self.current_control = control

    @property
    def nodeType(self):
        return Node.ELEMENT_NODE

    @property
    def ownerDocument(self):
        return ControlNode(uiautomation.GetRootControl())

    @property
    def documentElement(self):
        return None

    @property
    def tagName(self):
        return self.current_control.ControlTypeName

    @property
    def localName(self):
        return self.current_control.ControlTypeName

    @property
    def childNodes(self):
        return [ControlNode(child) for child in self.current_control.GetChildren()]

    @property
    def parentNode(self):
        return ControlNode(self.current_control.GetParentControl())

    @property
    def nextSibling(self):
        return ControlNode(self.current_control.GetNextSiblingControl())

    @property
    def previousSibling(self):
        return ControlNode(self.current_control.GetPreviousSiblingControl())

    @property
    def namespaceURI(self):
        return None

    @property
    def attributes(self):
        attrs = [
            AttributeNode(self.current_control, "name", self.current_control.Name),
            AttributeNode(
                self.current_control, "className", self.current_control.ClassName
            ),
            AttributeNode(
                self.current_control, "automationId", self.current_control.AutomationId
            ),
            AttributeNode(
                self.current_control, "helpText", self.current_control.HelpText
            ),
            AttributeNode(self.current_control, "namespaceURI", ""),
        ]
        return AttrList(self, attrs)


class AttributeNode(Node):
    def __init__(self, control: uiautomation.Control, name, value):
        self.owner_element = control
        self.name = name
        self.value = value

    @property
    def nodeType(self):
        return Node.ATTRIBUTE_NODE

    @property
    def ownerElement(self):
        return ControlNode(uiautomation.GetRootControl())

    @property
    def namespaceURI(self):
        return None

    @property
    def localName(self):
        return self.name


class AttrList(object):
    def __init__(self, element, attrs):
        self.element = element
        self.attrs = attrs

    def item(self, index):
        return self.attrs[index]

    @property
    def length(self):
        return len(self.attrs)
