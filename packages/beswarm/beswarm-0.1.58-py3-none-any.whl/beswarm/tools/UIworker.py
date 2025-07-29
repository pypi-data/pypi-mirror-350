import os
import io
import copy
import base64
import platform
from datetime import datetime
from ..aient.src.aient.plugins import register_tool, get_function_call_list

from ..aient.src.aient.models import chatgpt
from ..aient.src.aient.prompt import system_prompt, instruction_system_prompt
from ..aient.src.aient.core.utils import get_image_message, get_text_message

from ..utils import extract_xml_content

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

@register_tool()
async def UIworker(goal, tools, work_dir, cache_messages=None):
    """
    启动一个 **工作智能体 (Worker Agent)** 来自动完成指定的任务目标 (`goal`)。

    这个工作智能体接收一个清晰的任务描述、一组可供调用的工具 (`tools`)，以及一个工作目录 (`work_dir`)。
    它会利用语言模型的能力，结合可用的工具，自主规划并逐步执行必要的操作，直到最终完成指定的任务目标。
    核心功能是根据输入的目标，驱动整个任务执行流程。

    Args:
        goal (str): 需要完成的具体任务目标描述。工作智能体将围绕此目标进行工作。必须清晰、具体。
        tools (list[str]): 一个包含可用工具函数对象的列表。工作智能体在执行任务时可能会调用这些工具来与环境交互（例如读写文件、执行命令等）。
        work_dir (str): 工作目录的绝对路径。工作智能体将在此目录上下文中执行操作。

    Returns:
        str: 当任务成功完成时，返回字符串 "任务已完成"。
    """

    tools_json = [value for _, value in get_function_call_list(tools).items()]
    work_agent_system_prompt = system_prompt.format(
        os_version=platform.platform(),
        workspace_path=work_dir,
        shell=os.getenv('SHELL', 'Unknown'),
        tools_list=tools_json
    )

    work_agent_config = {
        "api_key": os.getenv("API_KEY"),
        "api_url": os.getenv("BASE_URL"),
        "engine": os.getenv("MODEL"),
        "system_prompt": work_agent_system_prompt,
        "print_log": True,
        # "max_tokens": 8000,
        "temperature": 0.5,
        "function_call_max_loop": 100,
    }
    if cache_messages:
        work_agent_config["cache_messages"] = cache_messages

    instruction_agent_config = {
        "api_key": os.getenv("API_KEY"),
        "api_url": os.getenv("BASE_URL"),
        "engine": os.getenv("MODEL"),
        "system_prompt": instruction_system_prompt.format(os_version=platform.platform(), tools_list=tools_json, workspace_path=work_dir, current_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        "print_log": False,
        # "max_tokens": 4000,
        "temperature": 0.7,
        "use_plugins": False,
    }

    # 工作agent初始化
    work_agent = chatgpt(**work_agent_config)
    async def instruction_agent_task():
        while True:
            instruction_prompt = f"""
任务目标: {goal}

以上对话都是工作智能体的对话历史。

根据以上对话历史和目标，请生成下一步指令。如果任务已完成，请回复"任务已完成"。
            """
            # 让指令agent分析对话历史并生成新指令
            instruction_agent = chatgpt(**instruction_agent_config)
            conversation_history = copy.deepcopy(work_agent.conversation["default"])
            conversation_history.pop(0)
            instruction_agent.conversation["default"][1:] = conversation_history
            new_prompt = await get_current_screen_image_message(instruction_prompt)
            next_instruction = await instruction_agent.ask_async(new_prompt)
            print("\n🤖 指令智能体生成的下一步指令:", next_instruction)
            if "fetch_gpt_response_stream HTTP Error', 'status_code': 404" in next_instruction:
                raise Exception(f"Model: {instruction_agent_config['engine']} not found!")
            if "'status_code': 413" in next_instruction:
                raise Exception(f"The request body is too long, please try again.")
            next_instruction = extract_xml_content(next_instruction, "instructions")
            if not next_instruction:
                print("\n❌ 指令智能体生成的指令不符合要求，请重新生成。")
                continue
            else:
                break
        return next_instruction

    need_instruction = True
    while True:
        next_instruction = ''
        if need_instruction:
            next_instruction = await instruction_agent_task()

            # 检查任务是否完成
            if "任务已完成" in next_instruction:
                print("\n✅ 任务已完成！")
                break
        new_prompt = await get_current_screen_image_message(next_instruction)
        result = await work_agent.ask_async(new_prompt)
        if result.strip() == '':
            print("\n❌ 工作智能体回复为空，请重新生成指令。")
            need_instruction = False
            continue
        print("✅ 工作智能体回复:", result)
        need_instruction = True

    return "任务已完成"