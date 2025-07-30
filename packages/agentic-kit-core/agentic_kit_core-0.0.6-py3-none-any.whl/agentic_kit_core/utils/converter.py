from typing import Any, get_origin, get_args, Type, Optional

from pydantic import Field, create_model, BaseModel

type_mapping = {
    "string": str,
    "int": int,
    "bool": bool,
    "float": float,
    "list": list,
    "dict": dict,
    "None": None
}


def convert_dict_to_fields(fields_dict):
    """递归解析tool args, 转换成可以初始化BaseModel的结构"""
    fields = {}
    for field_name, field_info in fields_dict.items():
        if 'type' in field_info:
            filed_type = type_mapping[field_info['type']]
            filed_description = field_info['description']
            filed_required = field_info['required']
            fields[field_name] = (filed_type if filed_required else Optional[filed_type], filed_description)
        else:  # 嵌套
            _fields = convert_dict_to_fields(field_info)
            fields[field_name] = _fields
    return fields


def create_nested_model(model_name: str, fields: dict[str, Any]) -> Type[BaseModel]:
    """
    递归生成嵌套的 BaseModel 类，并为每个字段添加 Field 描述。
    """
    nested_fields = {}
    for field_name, field_info in fields.items():
        if isinstance(field_info, dict):  # 如果字段是嵌套字典
            nested_model_name = f"{model_name}_{field_name.capitalize()}"
            nested_model = create_nested_model(nested_model_name, field_info)
            nested_fields[field_name] = (nested_model, ...)
        elif isinstance(field_info, tuple):  # 如果字段包含类型和描述
            field_type, field_description = field_info
            if get_origin(field_type) is list:  # 如果字段是列表
                list_type = get_args(field_type)[0]
                nested_fields[field_name] = (list[list_type], Field(..., description=field_description))
            else:  # 普通字段
                nested_fields[field_name] = (field_type, Field(..., description=field_description))
        else:  # 普通字段（无描述）
            nested_fields[field_name] = (field_info, ...)

    return create_model(model_name, **nested_fields)


if __name__ == '__main__':
    fields = {
        "name": (str, Field(..., description="The person's name")),
        "age": (int, Field(..., description="The person's age")),
        "is_student": (bool, Field(False, description="Whether the person is a student")),
        "kwargs": {
            "name": (str, Field(..., description="The person's name")),
            "age": (int, Field(..., description="The person's age")),
            "is_student": (bool, Field(False, description="Whether the person is a student")),
        }
    }

    DynamicModel = create_nested_model("DynamicModel", fields=fields)
    res = DynamicModel.model_json_schema()
    print(type(res))
    print(res)
