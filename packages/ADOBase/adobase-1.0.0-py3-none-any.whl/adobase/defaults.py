import json
import os

# 获取defaults.json的路径（假设与本py文件同级或在上级目录）
DEFAULTS_JSON_PATH = os.path.join(os.path.dirname(__file__), 'defaults.json')

def _load_defaults():
    with open(DEFAULTS_JSON_PATH, 'r', encoding='utf-8-sig') as f:
        return json.load(f)

defaults_data = _load_defaults()

def get_default_event_attrs(event_type: str):
    """
    获取指定事件类型的默认属性字典。
    """
    for action in defaults_data.get('actions', []):
        if action.get('eventType') == event_type:
            # 返回去除floor字段后的默认属性
            return {k: v for k, v in action.items() if k != 'floor'}
    return None 

def get_default_decoration_attrs(decoration_type: str):
    """
    获取指定装饰物类型的默认属性字典。
    """
    for deco in defaults_data.get('decorations', []):
        if deco.get('eventType') == decoration_type:
            # 返回去除floor字段后的默认属性
            return {k: v for k, v in deco.items() if k != 'floor'}
    return None 