import re

def extract_xml_content(text, xml_tag):
    result = ''
    pattern = rf'^<{xml_tag}>$\n*([\D\d\s]+?)\n*^<\/{xml_tag}>$'
    match = re.search(pattern, text, re.MULTILINE)
    if match:
        result = match.group(1)
    if not result:
        return ''
    return result

import io
import base64
from .aient.src.aient.core.utils import get_image_message, get_text_message

async def get_current_screen_image_message(prompt):
    print("instruction agent 正在截取当前屏幕...")
    try:
        import pyautogui
        # 使用 pyautogui 截取屏幕，返回 PIL Image 对象
        screenshot = pyautogui.screenshot()
        # img_width, img_height = screenshot.size # 获取截图尺寸
        img_width, img_height = pyautogui.size()
        print(f"截图成功，尺寸: {img_width}x{img_height}")

        # 将 PIL Image 对象转换为 Base64 编码的 PNG 字符串
        buffered = io.BytesIO()
        screenshot.save(buffered, format="PNG")
        base64_encoded_image = base64.b64encode(buffered.getvalue()).decode("utf-8")
        IMAGE_MIME_TYPE = "image/png" # 截图格式为 PNG

    except ImportError:
        # Pillow 也是 pyautogui 的依赖，但以防万一单独处理
        print("\n❌ 请安装所需库: pip install Pillow pyautogui")
        return False
    except Exception as e:
        print(f"\n❌ 截取屏幕或处理图像时出错: {e}")
        return False

    engine_type = "gpt"
    message_list = []
    text_message = await get_text_message(prompt, engine_type)
    image_message = await get_image_message(f"data:{IMAGE_MIME_TYPE};base64," + base64_encoded_image, engine_type)
    message_list.append(text_message)
    message_list.append(image_message)
    return message_list