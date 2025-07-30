import uiautomation
from robot_base import log_decorator, func_decorator


@log_decorator
@func_decorator
def set_text_to_clipboard(text_content, content_type="text", **kwargs):
    if content_type == "plain":
        uiautomation.SetClipboardText(text_content)
    else:
        uiautomation.SetClipboardHtml(text_content)


@log_decorator
@func_decorator
def get_text_from_clipboard(content_type="text", **kwargs):
    if content_type == "plain":
        return uiautomation.GetClipboardText()
    elif content_type == "html":
        return uiautomation.GetClipboardHtml()
