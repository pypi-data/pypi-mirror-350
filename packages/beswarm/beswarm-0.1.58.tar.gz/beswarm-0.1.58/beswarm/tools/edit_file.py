import os
import re
from ..aient.src.aient.plugins import register_tool

@register_tool()
def edit_file(file_path, diff_content, match_precision=0.8):
    """
使用diff模式编辑代码文件，支持Git的diff格式，每次修改一处。
你应该清楚地表明编辑内容，同时最小化你写的未更改代码。
你仍应倾向于尽可能少地重复原始文件的行来传达更改。
但是，编辑应包含足够的未更改行上下文，以消除你正在编辑的代码的歧义。

参数:
    file_path: 要编辑的文件路径
    diff_content: diff内容，格式为：
<<<<<<< SEARCH
原始代码
=======
替换代码
>>>>>>> REPLACE
    match_precision: 匹配精度 (0.0-1.0)，值越高要求匹配越精确，默认0.8

返回:
    编辑结果的状态信息，包括成功或错误信息
    """
    try:
        # 检查文件是否存在
        if not os.path.exists(file_path):
            return f"错误: 文件 '{file_path}' 不存在"

        # 检查是否为文件
        if not os.path.isfile(file_path):
            return f"错误: '{file_path}' 不是一个文件"

        # 尝试读取文件的前几个字节来检测是否为二进制文件
        with open(file_path, 'rb') as file:
            data = file.read(1024)
            # 快速检查是否可能是二进制文件
            if b'\x00' in data:
                return f"错误: 文件 '{file_path}' 可能是二进制文件，编码无法解析"

        # 读取原文件内容
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # 解析diff内容中的搜索和替换块
        diff_blocks = re.findall(r'<<<<<<< SEARCH\n(.*?)\n=======\n(.*?)\n>>>>>>> REPLACE', diff_content, re.DOTALL)

        if not diff_blocks:
            return f"错误: 无效的diff格式，未找到搜索和替换块"

        # 记录修改次数和行数变化
        edits_count = 0
        total_original_lines = 0
        total_new_lines = 0

        # 应用每个diff块
        new_content = content
        for search_block, replace_block in diff_blocks:
            # 检查搜索块是否为空
            if not search_block.strip():
                return f"错误: 搜索块不能为空"

            if search_block in new_content:
                # 直接替换完全匹配的块
                new_content = new_content.replace(search_block, replace_block, 1)
                edits_count += 1

                # 计算行数
                original_lines = search_block.count('\n') + 1
                new_lines = replace_block.count('\n') + 1
                total_original_lines += original_lines
                total_new_lines += new_lines
            else:
                # 尝试进行更宽松的匹配
                search_lines = search_block.splitlines()
                content_lines = new_content.splitlines()

                # 避免空搜索块
                if len(search_lines) == 0:
                    return f"错误: 搜索块不能为空"

                # 尝试找到最佳匹配位置
                best_match_index = -1
                best_match_score = 0

                for i in range(len(content_lines) - len(search_lines) + 1):
                    # 计算当前位置的匹配分数
                    match_score = 0
                    total_chars = 0

                    for j in range(len(search_lines)):
                        search_line = search_lines[j]
                        content_line = content_lines[i + j]

                        # 计算两行之间的相似度（使用更精确的算法）
                        # 1. 字符级别的比较
                        common_chars = sum(c1 == c2 for c1, c2 in zip(search_line, content_line))
                        total_line_chars = max(len(search_line), len(content_line))

                        if total_line_chars > 0:
                            line_match = common_chars / total_line_chars
                            match_score += line_match
                            total_chars += 1

                    # 计算整体匹配分数
                    if total_chars > 0:
                        match_score = match_score / total_chars
                    else:
                        match_score = 0

                    # 如果使用高精度匹配 (>0.95)，我们需要更严格地检查匹配结果
                    if match_precision > 0.95:
                        # 字符串长度差异也要考虑
                        search_text = '\n'.join(search_lines)
                        potential_match_text = '\n'.join(content_lines[i:i + len(search_lines)])
                        length_diff_ratio = abs(len(search_text) - len(potential_match_text)) / max(len(search_text), 1)

                        # 如果长度差异太大，降低匹配分数
                        if length_diff_ratio > 0.1:  # 允许10%的长度差异
                            match_score *= (1 - length_diff_ratio)

                    if match_score > best_match_score:
                        best_match_score = match_score
                        best_match_index = i

                # 使用匹配精度作为阈值
                if best_match_score >= match_precision and best_match_index >= 0:
                    # 提取找到的实际文本
                    matched_lines = content_lines[best_match_index:best_match_index + len(search_lines)]
                    actual_search_block = '\n'.join(matched_lines)

                    # 替换找到的匹配项
                    new_content = new_content.replace(actual_search_block, replace_block, 1)
                    edits_count += 1

                    # 计算行数
                    original_lines = len(matched_lines)
                    new_lines = replace_block.count('\n') + 1
                    total_original_lines += original_lines
                    total_new_lines += new_lines
                else:
                    return f"错误: 在文件中未找到足够匹配的代码块，最佳匹配分数为 {best_match_score:.2f}，但要求为 {match_precision:.2f}"

        # 如果没有进行任何编辑，返回错误
        if edits_count == 0:
            return f"错误: 未能应用任何diff编辑"

        # 写入修改后的内容
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(new_content)

        return f"成功: 文件 '{file_path}' 已更新。应用了 {edits_count} 处编辑，替换了 {total_original_lines} 行代码为 {total_new_lines} 行。"

    except PermissionError:
        return f"错误: 没有权限修改文件 '{file_path}'"
    except UnicodeDecodeError:
        return f"错误: 文件 '{file_path}' 不是文本文件或编码不是UTF-8，无法进行编码解析"
    except Exception as e:
        print(f"content: {content}")
        print(f"file_path: {file_path}")
        print(f"diff_content: {diff_content}")
        import traceback
        traceback.print_exc()
        return f"编辑文件时发生错误: {e}"

if __name__ == "__main__":
    edit_str = """
<<<<<<< SEARCH
    parser.add_argument('--dataset', type=str, default='cifar10', choices=['cifar10', 'cifar100', 'imagenet'], help="Dataset to use.")
=======
    parser.add_argument('--dataset', type=str, default='cifar10', choices=['cifar10', 'cifar100', 'imagenet', 'tinyimagenet'], help="Dataset to use.")
>>>>>>> REPLACE
"""

    file_path = "train.py"
# 编辑文件时发生错误: '>' not supported between instances of 'str' and 'float'
    print(edit_file(file_path, edit_str))

# python -m beswarm.tools.edit_file
