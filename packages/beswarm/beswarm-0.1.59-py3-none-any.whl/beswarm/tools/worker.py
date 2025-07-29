import os
import copy
import platform
from datetime import datetime

from ..aient.src.aient.models import chatgpt
from ..aient.src.aient.plugins import register_tool, get_function_call_list
from ..aient.src.aient.prompt import system_prompt, instruction_system_prompt
from ..utils import extract_xml_content, get_current_screen_image_message

@register_tool()
async def worker(goal, tools, work_dir, cache_messages=None):
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
</work_agent_conversation_end>
任务目标: {goal}

在 tag <work_agent_conversation_start>...</work_agent_conversation_end> 之前的对话历史都是工作智能体的对话历史。

根据以上对话历史和目标，请生成下一步指令。如果任务已完成，请回复"任务已完成"。
            """
            # 让指令agent分析对话历史并生成新指令
            instruction_agent = chatgpt(**instruction_agent_config)
            conversation_history = copy.deepcopy(work_agent.conversation["default"])
            conversation_history.pop(0)
            instruction_agent.conversation["default"][1:] = conversation_history
            if "find_and_click_element" in str(tools_json):
                instruction_prompt = await get_current_screen_image_message(instruction_prompt)
            next_instruction = await instruction_agent.ask_async(instruction_prompt)
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
                if conversation_history == []:
                    next_instruction = (
                        "任务描述：\n"
                        f"{goal}\n\n"
                        "现在开始执行第一步：\n"
                        f"{next_instruction}"
                    )
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
        if "find_and_click_element" in str(tools_json):
            next_instruction = await get_current_screen_image_message(next_instruction)
        result = await work_agent.ask_async(next_instruction)
        if result.strip() == '' or result.strip() == '</content>\n</write_to_file>':
            print("\n❌ 工作智能体回复为空，请重新生成指令。")
            need_instruction = False
            continue
        print("✅ 工作智能体回复:", result)
        need_instruction = True

    return "任务已完成"