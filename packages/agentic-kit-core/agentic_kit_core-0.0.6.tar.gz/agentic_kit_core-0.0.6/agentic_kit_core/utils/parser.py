import json
from io import StringIO

import yaml


def parse_yaml_llm_response(content: str):
    """解析yaml格式的llm输出"""
    if content.startswith('```yaml'):
        content = content.split('```yaml', 1)[-1].rstrip('```')
    elif content.startswith('`'):
        content = content.split('`', 1)[-1].rstrip('`')
    elif content.startswith('```'):
        content = content.split('```', 1)[-1].rstrip('```')
    yaml_content = yaml.safe_load(StringIO(content))
    return yaml_content


def parse_json_llm_response(content: str):
    """解析json格式的llm输出"""
    if content.startswith('```json'):
        content = content.split('```json', 1)[-1].rstrip('```')
    elif content.startswith('`'):
        content = content.split('`', 1)[-1].rstrip('`')
    elif content.startswith('```'):
        content = content.split('```', 1)[-1].rstrip('```')
    json_content = json.loads(content)
    return json_content


if __name__ == '__main__':
    content = '''plans:\n  - step_name: "Step#1"\n    plan: "计算上个月的工资总额。"\n    tool: "calculator_add_tool[{\'x\': 10, \'y\': 30}]"\n    tool_args: "{\'x\': 10, \'y\': 30}"\n    tool_name: "calculator_add_tool"\n    is_last_step: false\n  - step_name: "Step#2"\n    plan: "计算这个月的工资总额。"\n    tool: "calculator_add_tool[{\'x\': 10, \'y\': 60}]"\n    tool_args: "{\'x\': 10, \'y\': 60}"\n    tool_name: "calculator_add_tool"\n    is_last_step: false\n  - step_name: "Step#3"\n    plan: "计算两个月的总工资。"\n    tool: "calculator_add_tool[#E1 + #E2]"\n    tool_args: "{\'x\': \'#E1\', \'y\': \'#E2\'}"\n    tool_name: "calculator_add_tool"\n    is_last_step: false\n  - step_name: "Step#4"\n    plan: "从总工资中减去购买车的费用，得到剩余的钱。"\n    tool: "calculator_sub_tool[#E3 - 200]"\n    tool_args: "{\'x\': \'#E3\', \'y\': 200}"\n    tool_name: "calculator_sub_tool"\n    is_last_step: true'''
    res = parse_yaml_llm_response(content)
    print(res)
