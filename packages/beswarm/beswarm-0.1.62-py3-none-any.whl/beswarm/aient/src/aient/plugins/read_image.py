import os
import base64
import mimetypes
from .registry import register_tool

@register_tool()
def read_image(image_path: str):
    """
读取本地图片文件，将其转换为 Base64 编码，并返回包含 MIME 类型和完整数据的字符串。
此工具用于将图片内容加载到上下文中。

参数:
    image_path (str): 本地图片文件的路径。

返回:
    str: 成功时返回包含图片MIME类型和Base64编码数据的格式化字符串。
            失败时返回错误信息字符串。
    """
    try:
        # 检查路径是否存在
        if not os.path.exists(image_path):
            return f"<tool_error>图片路径 '{image_path}' 不存在。</tool_error>"
        # 检查是否为文件
        if not os.path.isfile(image_path):
            return f"<tool_error>路径 '{image_path}' 不是一个有效的文件 (可能是一个目录)。</tool_error>"

        # 尝试猜测MIME类型
        mime_type, _ = mimetypes.guess_type(image_path) # encoding 变量通常不需要

        if not mime_type or not mime_type.startswith('image/'):
            # 如果mimetypes无法识别，或者不是图片类型
            return f"<tool_error>文件 '{image_path}' 的MIME类型无法识别为图片 (检测到: {mime_type})。请确保文件是常见的图片格式 (e.g., PNG, JPG, GIF, WEBP)。</tool_error>"

        with open(image_path, "rb") as image_file:
            image_data = image_file.read()

        base64_encoded_data = base64.b64encode(image_data).decode('utf-8')

        # 返回一个描述性字符串，模仿 list_directory.py 的风格
        # 包含完整的 Base64 数据
        # 注意：对于非常大的图片，这可能会产生非常长的输出字符串。
        # return f"成功读取图片 '{image_path}':\n  MIME 类型: {mime_type}\n  Base64 数据: {base64_encoded_data}"
        return f"data:{mime_type};base64," + base64_encoded_data

    except FileNotFoundError:
        # 这个异常通常由 open() 抛出，如果 os.path.exists 通过但文件在读取前被删除
        # 或者路径检查逻辑未能完全覆盖所有情况 (理论上不应发生)
        return f"<tool_error>图片路径 '{image_path}' 未找到 (可能在检查后被删除或移动)。</tool_error>"
    except PermissionError:
        return f"<tool_error>没有权限访问图片路径 '{image_path}'。</tool_error>"
    except IOError as e: # 例如文件损坏无法读取，或磁盘问题
        return f"<tool_error>读取图片 '{image_path}' 时发生 I/O 错误: {e}</tool_error>"
    except Exception as e:
        return f"<tool_error>读取图片 '{image_path}' 时发生未知错误: {e}</tool_error>"