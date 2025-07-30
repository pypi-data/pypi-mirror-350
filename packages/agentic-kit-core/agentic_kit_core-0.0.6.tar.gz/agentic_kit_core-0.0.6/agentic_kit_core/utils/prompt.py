from langchain_core.messages import SystemMessage
from langchain_core.prompts import ChatPromptTemplate


def check_prompt_required_filed(prompt: str, required_field: list[str]):
    """判断prompt必须包含的字段"""
    for field in required_field:
        if field.startswith('{') and field.endswith('}'):
            if field not in prompt:
                return False
        else:
            if ('{' + f'{field}' + '}') not in prompt:
                print('提示词模板中必须包含待填充字段: %s' % field)
                return False
    return True


def generate_system_prompt(prompt: str, **kwargs):
    """根据prompt"""
    template = ChatPromptTemplate.from_messages([SystemMessage(content=prompt)])
    prompt_value = template.invoke(kwargs)
    return prompt_value


def generate_system_prompt_template(prompt: str):
    """根据prompt"""
    template = ChatPromptTemplate.from_messages([SystemMessage(content=prompt)])
    return template


if __name__ == '__main__':
    prompt: str = '''
        # 你是一位负责工作任务分发和监督的主管，你负责分发和监督的任务是：
            {router_desc}，如果超出你的工作范围，直接回复'FINISH'。

        # 你负责管理以下员工或者工作节点的任务分发，他们分别是：
            {options_desc}。

        # 请根据用户的请求，将用户请求做任务分解，将分解后的子任务分配给适合完成这项任务的员工或者工作节点。以下是要求：
            * 如果找到合适的员工和工作节点，请回复下一个员工的name。
            * 如果员工已经执行完成分配给他的任务，就回复他的结果和状态，并回复'FINISH'。
            * 如果任务的答案已经包含在消息列表中，直接回复'FINISH'。
            * 请你一步一步的分配任务，一个任务执行完以后再调用下一个任务。
            * 这次任务分配仅限于本段内容，忽略之前的任务。
    '''

    print(check_prompt_required_filed(prompt=prompt, required_field=['{router_desc}', '{options_desc}']))

    system_prompt = generate_system_prompt(prompt=prompt, **{
        'router_desc': 'xxxxxxx',
        'options_desc': 'yyyyyyy',
    })
    print(system_prompt)
    print(system_prompt.to_messages())
    print(type(system_prompt))

    print(generate_system_prompt_template(prompt=prompt))
