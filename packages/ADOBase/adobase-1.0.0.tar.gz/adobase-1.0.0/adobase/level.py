import json
from .utils import parse_adofai_to_json_str, add_bom, remove_bom, to_adofai_style_json
from .params import LEVEL_PARAMS, LEVEL_BASE, is_valid_param, LevelSettingsDict

class ADOFAILevel:
    def __init__(self, data: dict, raw_text: str = None):
        self.data = data
        self.raw_text = raw_text  # 保存原始文本，便于原样导出

    @classmethod
    def load(cls, filepath: str) -> 'ADOFAILevel':
        """从 .adofai 文件加载关卡，自动修正为标准 JSON，自动去除 BOM"""
        with open(filepath, 'r', encoding='utf-8') as f:
            raw_text = f.read()
        raw_text = remove_bom(raw_text)
        json_str = parse_adofai_to_json_str(raw_text)
        data = json.loads(json_str)
        return cls(data, raw_text=raw_text)

    def save(self, filepath: str) -> None:
        """保存关卡到 .adofai 文件（标准 JSON 格式，无 BOM，adodai 风格缩进）"""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(to_adofai_style_json(self.data))

    def export(self, filepath: str, as_original: bool = False) -> None:
        """
        导出关卡文件：
        - as_original=True：导出为 .adofai 文件（加 BOM，adodai 风格缩进，始终用当前数据）
        - as_original=False：导出为标准 JSON 文件（无 BOM，adodai 风格缩进）
        """
        if as_original:
            # 始终用当前 self.data 导出，保证修改生效
            content = to_adofai_style_json(self.data)
            content = add_bom(content)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
        else:
            # 导出为标准 JSON，无 BOM，adodai 风格缩进
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(to_adofai_style_json(self.data))

    def get_level_info(self, *fields) -> dict:
        """
        获取关卡信息。
        - 不传参数时，返回 settings 下所有字段及其值的字典
        - 传参数为 'levelbase' 时，返回关卡基本信息字典（song, artist, author）
        - 传多个参数时，支持 levelbase 与其他参数混用，合并返回
        - 传单个参数时，直接返回该字段的值
        """
        settings = self.data.get('settings', {})
        for field in fields:
            if not is_valid_param(field):
                raise ValueError(f"无效的关卡参数: {field}")
        if not fields:
            return settings.copy()
        result = {}
        for field in fields:
            if field == LEVEL_BASE:
                result.update({k: settings.get(k, '') for k in ('song', 'artist', 'author')})
            elif field not in settings:
                raise KeyError(f"关卡文件中不存在字段: {field}")
            else:
                result[field] = settings[field]
        if len(fields) == 1:
            return next(iter(result.values()))
        return result
            
    def print_level_info(self, *fields) -> dict:
        """
        打印关卡信息（兼容旧版本）。
        建议使用 get_level_info() 获取数据后自行处理。
        """
        result = self.get_level_info(*fields)
        if isinstance(result, dict):
            for k, v in result.items():
                print(f"{k}: {v}")
        else:
            # 单个字段的情况
            print(f"{fields[0]}: {result}")
        return result

    def edit_level_info(self, **kwargs) -> None:
        """
        编辑关卡信息。
        允许用户传入要编辑的字段和值，若字段不存在则抛出异常。
        用法：level.edit_level_info(song="新曲名", bpm=180)
        """
        settings = self.data.get('settings', {})
        for k in kwargs:
            if k not in LEVEL_PARAMS:
                raise ValueError(f"无效的关卡参数: {k}")
        for k, v in kwargs.items():
            if k not in settings:
                raise KeyError(f"关卡文件中不存在字段: {k}")
            settings[k] = v 

    def get_tile_event(self, floor: int, event_type: str = None):
        """
        获取指定floor编号的事件。
        参数：
            floor (int): 砖块编号
            event_type (str, 可选): 事件类型（如'MoveDecorations'等）
        返回：
            - 若只传floor，返回该floor的所有事件（列表）
            - 若传floor和event_type，返回该floor上所有该类型事件（列表，可能为空）
        """
        actions = self.data.get('actions', [])
        filtered = [action for action in actions if action.get('floor') == floor]
        if event_type is not None:
            filtered = [action for action in filtered if action.get('eventType') == event_type]
        return filtered 

    def get_event_count(self, floor: int = None, event_type: str = None) -> int:
        """
        统计事件数量。
        参数：
            floor (int, 可选): 砖块编号
            event_type (str, 可选): 事件类型
        返回：
            - 都不传：统计全关卡所有事件数量
            - 只传event_type：统计全关卡该类型事件数量
            - 只传floor：统计该砖块所有事件数量
            - floor和event_type都传：统计该砖块该类型事件数量
        """
        actions = self.data.get('actions', [])
        if floor is None and event_type is None:
            return len(actions)
        if floor is not None and event_type is None:
            return sum(1 for action in actions if action.get('floor') == floor)
        if floor is None and event_type is not None:
            return sum(1 for action in actions if action.get('eventType') == event_type)
        # floor和event_type都传
        return sum(1 for action in actions if action.get('floor') == floor and action.get('eventType') == event_type)

    def batch_get_event_info(self, event_type: str, attr: str = None):
        """
        批量获取所有指定类型事件的信息。
        参数：
            event_type (str): 事件类型（如'MoveDecorations'等）
            attr (str, 可选): 指定属性名，若指定则只返回该属性及其值
        返回：
            - 若指定attr，返回所有该类型事件的该属性值列表（如[{attr: value}, ...]）
            - 未指定attr，返回所有该类型事件的完整信息列表
        """
        actions = self.data.get('actions', [])
        filtered = [action for action in actions if action.get('eventType') == event_type]
        if attr is not None:
            return [{attr: action.get(attr, None)} for action in filtered]
        return filtered

    def get_event_info(self, floor: int, event_type: str, index: int = 0, *attrs):
        """
        获取指定砖块(floor)上指定类型(event_type)的第index个事件信息，支持指定返回的属性。
        参数：
            floor (int): 砖块编号
            event_type (str): 事件类型（如'MoveDecorations'等）
            index (int, 可选): 索引（同类事件有多个时指定第几个，默认0）
            *attrs: 可选，若指定则只返回这些属性的值（单个属性返回值，多属性返回字典）
        返回：
            - 不指定attrs时，返回事件完整字典
            - 指定1个属性时，返回该属性值
            - 指定多个属性时，返回{属性:值}字典
        """
        events = self.get_tile_event(floor, event_type)
        if not events:
            raise IndexError(f"floor={floor} 上没有类型为 {event_type} 的事件")
        if index < 0 or index >= len(events):
            raise IndexError(f"floor={floor} 上类型为 {event_type} 的事件数量为{len(events)}，索引{index}超出范围")
        event = events[index]
        if not attrs:
            return event
        if len(attrs) == 1:
            return event.get(attrs[0], None)
        return {attr: event.get(attr, None) for attr in attrs}

    def edit_event_info(self, floor: int, event_type: str, index: int = 0, **kwargs):
        """
        编辑指定砖块(floor)上指定类型(event_type)的第index个事件的属性。
        参数：
            floor (int): 砖块编号
            event_type (str): 事件类型（如'MoveDecorations'等）
            index (int, 可选): 索引（同类事件有多个时指定第几个，默认0）
            **kwargs: 要修改的属性及其新值
        用法：
            edit_event_info(1, "MoveDecorations", 1, duration=1, tag="2")
        """
        events = self.get_tile_event(floor, event_type)
        if not events:
            raise IndexError(f"floor={floor} 上没有类型为 {event_type} 的事件")
        if index < 0 or index >= len(events):
            raise IndexError(f"floor={floor} 上类型为 {event_type} 的事件数量为{len(events)}，索引{index}超出范围")
        event = events[index]
        for k, v in kwargs.items():
            event[k] = v 

    def batch_edit_event(self, event_type: str, floor: int = None, **kwargs):
        """
        批量修改事件属性。
        参数：
            event_type (str): 事件类型
            floor (int, 可选): 只修改该砖块上的事件，若不填则全关卡
            **kwargs: 要修改的属性及其新值
        返回：
            实际被修改的事件数量
        用法：
            batch_edit_event('MoveDecorations', duration=1, tag='2')  # 全关卡
            batch_edit_event('MoveDecorations', floor=3, duration=2)  # 只修改3号砖块
        """
        actions = self.data.get('actions', [])
        count = 0
        for action in actions:
            if action.get('eventType') == event_type:
                if floor is None or action.get('floor') == floor:
                    for k, v in kwargs.items():
                        action[k] = v
                    count += 1
        return count  # 返回修改的事件数量 
    
    def add_event(self, floor: int, event_type: str, *args, **kwargs):
        """
        向指定floor添加事件。
        参数：
            floor (int): 砖块编号
            event_type (str): 事件类型（如'MoveDecorations'等）
            *args: 可选，若为'default'，则使用默认事件属性
            **kwargs: 事件的自定义属性
        用法：
            add_event(1, "MoveDecorations", 'default')  # 使用默认属性
            add_event(1, "MoveDecorations", duration=1, tag="sampleTag")  # 自定义属性
        """
        from .defaults import get_default_event_attrs
        actions = self.data.setdefault('actions', [])
        if args and args[0] == 'default':
            attrs = get_default_event_attrs(event_type)
            if attrs is None:
                raise ValueError(f"未找到事件类型 {event_type} 的默认属性")
            event = {'floor': floor, 'eventType': event_type}
            event.update(attrs)
        else:
            event = {'floor': floor, 'eventType': event_type}
            event.update(kwargs)

        # 寻找插入位置
        insert_idx = None
        last_same_floor_idx = None
        for idx, act in enumerate(actions):
            if act.get('floor') == floor:
                last_same_floor_idx = idx
        if last_same_floor_idx is not None:
            insert_idx = last_same_floor_idx + 1
        else:
            for idx, act in enumerate(actions):
                if act.get('floor', -1) > floor:
                    insert_idx = idx
                    break
        if insert_idx is not None:
            actions.insert(insert_idx, event)
        else:
            actions.append(event) 

    def remove_event(self, floor: int = None, event_type: str = None, index: int = None):
        """
        删除事件。
        参数：
            floor (int, 可选): 砖块编号。不填时可全局删除event_type类型事件
            event_type (str, 可选): 事件类型（如'MoveDecorations'等），可单独传入
            index (int, 可选): 索引（同类事件有多个时指定第几个，默认全部删除）
        返回：
            被删除的事件（单个或列表）
        用法：
            remove_event(1)  # 删除floor=1的所有事件
            remove_event(1, "MoveTrack")  # 删除floor=1的所有MoveTrack事件
            remove_event(1, "MoveTrack", 0)  # 删除floor=1的第一个MoveTrack事件
            remove_event(event_type="MoveTrack")  # 删除全关卡所有MoveTrack事件
            remove_event()  # 删除所有事件
        """
        actions = self.data.get('actions', [])
        if floor is None and event_type is None and index is None:
            # 无参数，清空所有事件
            removed = actions[:]
            actions.clear()
            return removed
        matched = []
        if floor is None and event_type is not None:
            # 全关卡删除指定类型事件
            for idx, act in enumerate(actions):
                if act.get('eventType') == event_type:
                    matched.append(idx)
        else:
            for idx, act in enumerate(actions):
                if floor is not None and act.get('floor') == floor:
                    if event_type is None or act.get('eventType') == event_type:
                        matched.append(idx)
        if not matched:
            raise IndexError(
                f"未找到要删除的事件："
                + (f"floor={floor} " if floor is not None else "")
                + (f"event_type={event_type}" if event_type is not None else "")
            )
        removed = []
        if index is not None:
            if index < 0 or index >= len(matched):
                raise IndexError(f"事件数量为{len(matched)}，索引{index}超出范围")
            idx_to_remove = matched[index]
            removed.append(actions.pop(idx_to_remove))
        else:
            for idx in reversed(matched):
                removed.append(actions.pop(idx))
            removed.reverse()
        return removed[0] if index is not None else removed

    def get_tile_decoration(self, floor: int, decoration_type: str = None):
        """
        获取指定floor编号的装饰信息。
        参数：
            floor (int): 砖块编号
            decoration_type (str, 可选): 装饰物类型（如'AddDecoration' 'AddText'等）
        返回：
            - 若只传floor，返回该floor的所有装饰物（列表信息）
            - 若传floor和decoration_type，返回该floor上所有该类型装饰物（列表信息，可能为空）
        """
        decorations = self.data.get('decorations', [])
        filtered = [item for item in decorations if item.get('floor') == floor]
        if decoration_type is not None:
            filtered = [item for item in filtered if item.get('eventType') == decoration_type]
        return filtered

    def get_decoration_count(self, floor: int = None, decoration_type: str = None) -> int:
        """
        统计装饰物数量。
        参数：
            floor (int, 可选): 砖块编号
            decoration_type (str, 可选): 装饰物类型
        返回：
            - 都不传：统计全关卡所有装饰物数量
            - 只传decoration_type：统计全关卡该类型装饰物数量
            - 只传floor：统计该砖块所有装饰物数量
            - floor和decoration_type都传：统计该砖块该类型装饰物数量
        """
        decorations = self.data.get('decorations', [])
        if floor is None and decoration_type is None:
            return len(decorations)
        if floor is not None and decoration_type is None:
            return sum(1 for deco in decorations if deco.get('floor') == floor)
        if floor is None and decoration_type is not None:
            return sum(1 for deco in decorations if deco.get('eventType') == decoration_type)
        # floor和decoration_type都传
        return sum(1 for deco in decorations if deco.get('floor') == floor and deco.get('eventType') == decoration_type)

    def batch_get_decoration_info(self, decoration_type: str, attr: str = None):
        """
        批量获取所有指定类型装饰物的信息。
        参数：
            decoration_type (str): 装饰物类型（如'AddDecoration'等）
            attr (str, 可选): 指定属性名，若指定则只返回该属性及其值
        返回：
            - 若指定attr，返回所有该类型装饰物的该属性值列表（如[{attr: value}, ...]）
            - 未指定attr，返回所有该类型装饰物的完整信息列表
        """
        decorations = self.data.get('decorations', [])
        filtered = [deco for deco in decorations if deco.get('eventType') == decoration_type]
        if attr is not None:
            return [{attr: deco.get(attr, None)} for deco in filtered]
        return filtered 

    def get_decoration_info(self, floor: int, decoration_type: str, index: int = 0, *attrs):
        """
        获取指定砖块(floor)上指定类型(decoration_type)的第index个装饰物信息，支持指定返回的属性。
        参数：
            floor (int): 砖块编号
            decoration_type (str): 装饰物类型（如'AddDecoration'等）
            index (int, 可选): 索引（同类装饰物有多个时指定第几个，默认0）
            *attrs: 可选，若指定则只返回这些属性的值（单个属性返回值，多属性返回字典）
        返回：
            - 不指定attrs时，返回装饰物完整字典
            - 指定1个属性时，返回该属性值
            - 指定多个属性时，返回{属性:值}字典
        """
        decorations = self.get_tile_decoration(floor, decoration_type)
        if not decorations:
            raise IndexError(f"floor={floor} 上没有类型为 {decoration_type} 的装饰物")
        if index < 0 or index >= len(decorations):
            raise IndexError(f"floor={floor} 上类型为 {decoration_type} 的装饰物数量为{len(decorations)}，索引{index}超出范围")
        deco = decorations[index]
        if not attrs:
            return deco
        if len(attrs) == 1:
            return deco.get(attrs[0], None)
        return {attr: deco.get(attr, None) for attr in attrs}

    def edit_decoration_info(self, floor: int, decoration_type: str, index: int = 0, **kwargs):
        """
        编辑指定砖块(floor)上指定类型(decoration_type)的第index个装饰物的属性。
        参数：
            floor (int): 砖块编号
            decoration_type (str): 装饰物类型（如'AddDecoration'等）
            index (int, 可选): 索引（同类装饰物有多个时指定第几个，默认0）
            **kwargs: 要修改的属性及其新值
        用法：
            edit_decoration_info(1, "AddDecoration", 1, tag="2")
        """
        decorations = self.get_tile_decoration(floor, decoration_type)
        if not decorations:
            raise IndexError(f"floor={floor} 上没有类型为 {decoration_type} 的装饰物")
        if index < 0 or index >= len(decorations):
            raise IndexError(f"floor={floor} 上类型为 {decoration_type} 的装饰物数量为{len(decorations)}，索引{index}超出范围")
        deco = decorations[index]
        for k, v in kwargs.items():
            deco[k] = v 
            
    def batch_edit_decoration(self, decoration_type: str, floor: int = None, **kwargs):
        """
        批量修改装饰物属性。
        参数：
            decoration_type (str): 装饰物类型（如'AddDecoration'等）
            floor (int, 可选): 只修改该砖块上的装饰物，若不填则全关卡
            **kwargs: 要修改的属性及其新值
        用法：
            batch_edit_decoration('AddDecoration', scale=1.5, tag='background')  # 全关卡
            batch_edit_decoration('AddDecoration', floor=2, scale=2.0)  # 只修改2号砖块
        """
        decorations = self.data.get('decorations', [])
        count = 0
        for decoration in decorations:
            if decoration.get('eventType') == decoration_type:
                if floor is None or decoration.get('floor') == floor:
                    for k, v in kwargs.items():
                        decoration[k] = v
                    count += 1
        return count  # 返回修改的装饰物数量 

    def add_decoration(self, floor: int, decoration_type: str, *args, **kwargs):
        """
        向指定floor添加装饰物。
        参数：
            floor (int): 砖块编号
            decoration_type (str): 装饰物类型（如'AddDecoration'等）
            *args: 可选，若为'default'，则使用默认装饰物属性
            **kwargs: 装饰物的自定义属性
        用法：
            add_decoration(1, "AddDecoration", 'default')  # 使用默认属性
            add_decoration(1, "AddDecoration", scale=1.5, tag="sampleTag")  # 自定义属性
        """
        from .defaults import get_default_decoration_attrs
        decorations = self.data.setdefault('decorations', [])
        if args and args[0] == 'default':
            attrs = get_default_decoration_attrs(decoration_type)
            if attrs is None:
                raise ValueError(f"未找到装饰物类型 {decoration_type} 的默认属性")
            deco = {'floor': floor, 'eventType': decoration_type}
            deco.update(attrs)
        else:
            deco = {'floor': floor, 'eventType': decoration_type}
            deco.update(kwargs)

        # 寻找插入位置
        insert_idx = None
        last_same_floor_idx = None
        for idx, item in enumerate(decorations):
            if item.get('floor') == floor:
                last_same_floor_idx = idx
        if last_same_floor_idx is not None:
            insert_idx = last_same_floor_idx + 1
        else:
            for idx, item in enumerate(decorations):
                if item.get('floor', -1) > floor:
                    insert_idx = idx
                    break
        if insert_idx is not None:
            decorations.insert(insert_idx, deco)
        else:
            decorations.append(deco)

    def remove_decoration(self, floor: int = None, decoration_type: str = None, index: int = None):
        """
        删除装饰物。
        参数：
            floor (int, 可选): 砖块编号。不填时可全局删除decoration_type类型装饰物
            decoration_type (str, 可选): 装饰物类型，可单独传入
            index (int, 可选): 索引（同类装饰物有多个时指定第几个，默认全部删除）
        返回：
            被删除的装饰物（单个或列表）
        用法：
            remove_decoration(1)  # 删除floor=1的所有装饰物
            remove_decoration(1, "AddDecoration")  # 删除floor=1的所有AddDecoration装饰物
            remove_decoration(1, "AddDecoration", 0)  # 删除floor=1的第一个AddDecoration装饰物
            remove_decoration(decoration_type="AddDecoration")  # 删除全关卡所有AddDecoration装饰物
            remove_decoration()  # 删除所有装饰物
        """
        decorations = self.data.get('decorations', [])
        if floor is None and decoration_type is None and index is None:
            # 无参数，清空所有装饰物
            removed = decorations[:]
            decorations.clear()
            return removed
        matched = []
        if floor is None and decoration_type is not None:
            # 全关卡删除指定类型装饰物
            for idx, item in enumerate(decorations):
                if item.get('eventType') == decoration_type:
                    matched.append(idx)
        else:
            for idx, item in enumerate(decorations):
                if floor is not None and item.get('floor') == floor:
                    if decoration_type is None or item.get('eventType') == decoration_type:
                        matched.append(idx)
        if not matched:
            raise IndexError(
                f"未找到要删除的装饰物："
                + (f"floor={floor} " if floor is not None else "")
                + (f"decoration_type={decoration_type}" if decoration_type is not None else "")
            )
        removed = []
        if index is not None:
            if index < 0 or index >= len(matched):
                raise IndexError(f"装饰物数量为{len(matched)}，索引{index}超出范围")
            idx_to_remove = matched[index]
            removed.append(decorations.pop(idx_to_remove))
        else:
            for idx in reversed(matched):
                removed.append(decorations.pop(idx))
            removed.reverse()
        return removed[0] if index is not None else removed 