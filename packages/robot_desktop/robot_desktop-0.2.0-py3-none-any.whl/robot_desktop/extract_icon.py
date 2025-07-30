import base64
from io import BytesIO

import win32con
import win32gui
import win32ui
from PIL import Image


def extract_icon(executable_path):
    # 从可执行文件中提取图标
    large, small = win32gui.ExtractIconEx(executable_path, 0)
    if not large:
        return ""

    # 创建一个内存设备上下文
    hicon = large[0]
    ico_x = 256
    ico_y = 256
    hdc = win32ui.CreateDCFromHandle(win32gui.GetDC(0))
    mem_dc = hdc.CreateCompatibleDC()
    bitmap = win32ui.CreateBitmap()
    bitmap.CreateCompatibleBitmap(hdc, ico_x, ico_y)
    mem_dc.SelectObject(bitmap)

    # 绘制图标到内存设备上下文
    win32gui.DrawIconEx(
        mem_dc.GetSafeHdc(), 0, 0, hicon, ico_x, ico_y, 0, 0, win32con.DI_NORMAL
    )

    # 转换为 PIL 图像
    bmp_info = bitmap.GetInfo()
    bmp_str = bitmap.GetBitmapBits(True)
    im = Image.frombuffer(
        "RGB", (bmp_info["bmWidth"], bmp_info["bmHeight"]), bmp_str, "raw", "BGRX", 0, 1
    )

    image_data = BytesIO()
    im.save(image_data, format="PNG")
    image_data_bytes = image_data.getvalue()
    encoded_image = base64.b64encode(image_data_bytes).decode("utf-8")
    # 保存图像
    # im.save(output_path, format="PNG")

    # 清理资源
    win32gui.DestroyIcon(hicon)
    win32gui.DeleteObject(bitmap.GetHandle())
    mem_dc.DeleteDC()
    win32gui.ReleaseDC(0, hdc.GetSafeHdc())
    return encoded_image
