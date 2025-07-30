from typing import List

from langchain_core.tools import BaseTool


def get_tools_desc_for_prompt_zh(tools: List[BaseTool]):
    tools_desc = ''
    counter = 1
    for tool in tools:
        tools_desc += f'''\n\t- [工具编号{counter}]\n'''
        tools_desc += f'''\t\t工具名称：{tool.name}\n'''
        tools_desc += f'''\t\t工具详细描述：{tool.description}\n'''
        tools_desc += f'''\t\t工具调用参数格式：{tool.args}\n'''
        tools_desc += '\n'
        counter += 1
    return tools_desc


def find_tool_by_name(tool_name: str, tools: List[BaseTool]) -> BaseTool:
    """通过name查找tool"""
    current_tool = None
    for tool in tools:
        if tool_name == tool.name:
            current_tool = tool
            break
    return current_tool
