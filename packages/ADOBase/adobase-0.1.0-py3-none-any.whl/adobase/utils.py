# 工具函数文件，后续可扩展 

import re

def parse_adofai_to_json_str(text: str) -> str:
    """
    将 .adofai 文件内容转换为标准 JSON 字符串：
    - 移除对象和数组中的尾随逗号
    - 保证能被 json.loads 正常解析
    """
    # 移除对象中的尾随逗号
    text = re.sub(r',([ \t\r\n]*[}\]])', r'\1', text)
    return text

def add_bom(text: str) -> str:
    """为字符串添加 UTF-8 BOM"""
    if not text.startswith('\ufeff'):
        return '\ufeff' + text
    return text

def remove_bom(text: str) -> str:
    """去除字符串开头的 UTF-8 BOM"""
    if text.startswith('\ufeff'):
        return text[1:]
    return text

# 需要一行输出的短数组key
SHORT_ARRAY_KEYS = {"parallax", "position", "pivotOffset", "scale", "tile", "parallaxOffset", "failHitboxScale", "failHitboxOffset", "failHitboxRotation"}
# 需要对象一行输出的对象数组key
OBJ_ARRAY_KEYS = {"actions", "decorations"}


def to_adofai_style_json(data, indent_level=0, key_name=None):
    """
    以 ADOFAI 关卡风格格式化 JSON：
    - angleData、短数组一行
    - actions、decorations等对象数组每个对象一行
    - 其余递归格式化
    """
    tab = '\t'
    indent = tab * indent_level
    next_indent = tab * (indent_level + 1)
    if isinstance(data, dict):
        items = []
        for k, v in data.items():
            items.append(f'{next_indent}"{k}": {to_adofai_style_json(v, indent_level + 1, k)}')
        return '{\n' + ',\n'.join(items) + f'\n{indent}' + '}'
    elif isinstance(data, list):
        if not data:
            return '[]'
        # angleData 或短数组一行
        if key_name in ("angleData",) or key_name in SHORT_ARRAY_KEYS:
            return '[' + ', '.join(map(json_repr, data)) + ']'
        # actions、decorations等对象数组，每个对象一行
        elif key_name in OBJ_ARRAY_KEYS and all(isinstance(v, dict) for v in data):
            items = [to_adofai_obj_oneline(v) for v in data]
            return '[\n' + ',\n'.join(f'{next_indent}{item}' for item in items) + f'\n{indent}' + ']'
        else:
            items = [f'{next_indent}{to_adofai_style_json(v, indent_level + 1)}' for v in data]
            return '[\n' + ',\n'.join(items) + f'\n{indent}' + ']'
    else:
        return json_repr(data)

def to_adofai_obj_oneline(obj):
    # 对象所有属性一行输出
    parts = [f'"{k}": {json_repr(v)}' for k, v in obj.items()]
    return '{ ' + ', '.join(parts) + ' }'

def json_repr(val):
    import json
    return json.dumps(val, ensure_ascii=False) 