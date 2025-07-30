# ADOBase

ADOBase 是一个专为 ADOFAI 游戏 .adofai 关卡文件设计的 Python 库，支持关卡文件的读取、写入、格式转换、信息提取、事件查找与批量编辑等操作。

## 主要功能
- **读取 .adofai 关卡文件**（自动去除 BOM，自动修正非标准 JSON，如尾随逗号）
- **写入/导出关卡文件**（支持标准 JSON 和 adofai 原格式风格，缩进、数组、对象数组等完全还原）
- **关卡信息提取与编辑**（支持获取全部、基础或指定字段信息，参数校验，支持关卡信息字段的安全编辑）
- **事件查找与编辑**（支持按砖块、事件类型、索引查找事件，支持单个/批量事件属性编辑）
- **支持文件选择器交互**（测试脚本可直接选择输入输出文件）
- **兼容大部分 ADOFAI 关卡文件格式细节**

## 安装

```bash
pip install ADOBase
```

## 用法示例

```python
from adobase import ADOFAILevel

# 读取关卡文件（自动处理 BOM 和非标准 JSON）
level = ADOFAILevel.load('main.adofai')

# 获取关卡信息
all_info = level.get_level_info()  # 获取全部关卡信息
basic_info = level.get_level_info('levelbase')  # 获取基础信息（曲名、曲师、谱师）
bpm = level.get_level_info('bpm')  # 获取单个值
specific = level.get_level_info('bpm', 'difficulty')  # 获取多个指定字段

# 打印关卡信息（兼容旧版本）
level.print_level_info('levelbase')  # 打印基础信息
level.print_level_info('bpm', 'difficulty')  # 打印指定字段

# 编辑关卡信息（如修改版本号和 BPM）
level.edit_level_info(version=15, bpm=180)

# 验证修改
print(level.get_level_info('version', 'bpm'))

# 获取某砖块的所有事件
events = level.get_tile_event(1)  # 获取1号砖块的所有事件
move_events = level.get_tile_event(1, 'MoveDecorations')  # 获取1号砖块所有MoveDecorations事件

# 获取某砖块某类型事件的详细信息
info = level.get_event_info(1, 'MoveDecorations', 0)  # 获取第一个MoveDecorations事件的全部信息
props = level.get_event_info(1, 'MoveDecorations', 0, 'duration', 'tag')  # 获取指定属性

# 编辑某砖块某类型事件的属性
level.edit_event_info(1, 'MoveDecorations', 0, duration=2, tag='newtag')

# 批量修改所有某类型事件的属性
level.batch_edit_event('MoveDecorations', duration=1, tag='2')
level.batch_edit_event('MoveDecorations', floor=3, duration=2)  # 只修改3号砖块

# 获取某砖块的所有装饰物
decorations = level.get_tile_decoration(1)  # 获取1号砖块的所有装饰物
add_decorations = level.get_tile_decoration(1, 'AddDecoration')  # 获取1号砖块所有AddDecoration装饰物

# 获取某砖块某类型装饰物的详细信息
deco_info = level.get_decoration_info(1, 'AddDecoration', 0)  # 获取第一个AddDecoration装饰物的全部信息
deco_props = level.get_decoration_info(1, 'AddDecoration', 0, 'scale', 'tag')  # 获取指定属性

# 编辑某砖块某类型装饰物的属性
level.edit_decoration_info(1, 'AddDecoration', 0, scale=1.5, tag='newtag')

# 批量修改所有某类型装饰物的属性
level.batch_edit_decoration('AddDecoration', scale=1.5, tag='background')
level.batch_edit_decoration('AddDecoration', floor=2, scale=2.0)  # 只修改2号砖块

# 批量获取所有某类型事件的完整信息
all_move_events = level.batch_get_event_info('MoveDecorations')
# 批量获取所有某类型事件的某个属性
move_durations = level.batch_get_event_info('MoveDecorations', 'duration')

# 批量获取所有某类型装饰物的完整信息
all_add_decos = level.batch_get_decoration_info('AddDecoration')
# 批量获取所有某类型装饰物的某个属性
add_scales = level.batch_get_decoration_info('AddDecoration', 'scale')

# 新增事件
level.add_event(1, "MoveTrack", "default")  # 在1号砖块插入一个默认MoveTrack事件
level.add_event(2, "Twirl", duration=1.5, tag="mytag")  # 在2号砖块插入自定义Twirl事件

# 删除事件
level.remove_event(1)  # 删除1号砖块的所有事件
level.remove_event(1, "MoveTrack")  # 删除1号砖块所有MoveTrack事件
level.remove_event(1, "MoveTrack", 0)  # 删除1号砖块第一个MoveTrack事件
level.remove_event(event_type="Twirl")  # 删除全关卡所有Twirl事件
level.remove_event()  # 删除所有事件（清空actions）

# 新增装饰物
level.add_decoration(2, "AddDecoration", "default")  # 在2号砖块插入一个默认AddDecoration装饰物
level.add_decoration(3, "AddDecoration", scale=2.0, tag="mytag")  # 在3号砖块插入自定义AddDecoration装饰物

# 删除装饰物
level.remove_decoration(2)  # 删除2号砖块的所有装饰物
level.remove_decoration(2, "AddDecoration")  # 删除2号砖块所有AddDecoration装饰物
level.remove_decoration(2, "AddDecoration", 0)  # 删除2号砖块第一个AddDecoration装饰物
level.remove_decoration(decoration_type="AddDecoration")  # 删除全关卡所有AddDecoration装饰物
level.remove_decoration()  # 删除所有装饰物（清空decorations）

# 导出为标准 JSON 文件（无 BOM，adodai 风格缩进）
level.export('output.json', as_original=False)

# 导出为 adofai 文件（加 BOM，adodai 风格缩进）
level.export('output.adofai', as_original=True)

# 统计事件数量
all_event_count = level.get_event_count()  # 全关卡事件总数
move_event_count = level.get_event_count(event_type='MoveDecorations')  # 全关卡某类型事件数
floor_event_count = level.get_event_count(floor=1)  # 1号砖块所有事件数
floor_move_event_count = level.get_event_count(floor=1, event_type='MoveDecorations')  # 1号砖块某类型事件数

# 统计装饰物数量
all_deco_count = level.get_decoration_count()  # 全关卡装饰物总数
add_deco_count = level.get_decoration_count(decoration_type='AddDecoration')  # 全关卡某类型装饰物数
floor_deco_count = level.get_decoration_count(floor=1)  # 1号砖块所有装饰物数
floor_add_deco_count = level.get_decoration_count(floor=1, decoration_type='AddDecoration')  # 1号砖块某类型装饰物数
```

## API 说明

### `ADOFAILevel.load(filepath)`
- 读取 .adofai 文件，自动去除 BOM，自动修正为标准 JSON。
- 返回 `ADOFAILevel` 实例。

### `ADOFAILevel.export(filepath, as_original=False)`
- 导出关卡文件。
    - `as_original=True`：导出为 adofai 文件（加 BOM，adodai 风格缩进）
    - `as_original=False`：导出为标准 JSON 文件（无 BOM，adodai 风格缩进）

### `ADOFAILevel.save(filepath)`
- 保存为标准 JSON 文件（无 BOM，adodai 风格缩进）。

### `ADOFAILevel.get_level_info(*fields)`
- 获取关卡信息：
    - 不传参数时，返回 settings 下所有字段及其值的字典
    - 传参数为 `'levelbase'` 时，返回关卡基础信息字典（曲名 song、曲师 artist、谱师 author）
    - 传多个参数时，返回指定字段的字典，若字段不存在则抛出异常
    - 传单个参数时，直接返回该字段的值

### `ADOFAILevel.print_level_info(*fields)`
- 打印关卡信息（兼容旧版本）：
    - 内部调用 `get_level_info()` 获取数据并打印
    - 同时返回获取的数据

### `ADOFAILevel.edit_level_info(**kwargs)`
- 编辑关卡信息：
    - 传入要修改的字段和值，如 `level.edit_level_info(version=15, bpm=180)`
    - 字段不存在会抛出异常，防止误操作

### `ADOFAILevel.get_tile_event(floor, event_type=None)`
- 获取指定砖块的事件：
    - 只传 `floor`，返回该砖块的所有事件（列表）
    - 传 `floor` 和 `event_type`，返回该砖块所有该类型事件（列表）

### `ADOFAILevel.get_event_info(floor, event_type, index=0, *attrs)`
- 获取指定砖块、事件类型、索引的事件信息：
    - 不传 `attrs`，返回事件完整字典
    - 传1个属性名，返回该属性值
    - 传多个属性名，返回{属性:值}字典
    - 若找不到事件或属性，返回 None 或抛出 IndexError

### `ADOFAILevel.edit_event_info(floor, event_type, index=0, **kwargs)`
- 编辑指定砖块、事件类型、索引的事件属性：
    - 传入要修改的属性及新值，如 `edit_event_info(1, 'MoveDecorations', 0, duration=2, tag='newtag')`
    - 若找不到事件，抛出 IndexError

### `ADOFAILevel.batch_edit_event(event_type, floor=None, **kwargs)`
- 批量修改事件属性：
    - 只传 `event_type`，全关卡批量修改该类型事件
    - 同时传 `event_type` 和 `floor`，只修改该砖块上的该类型事件
    - 返回实际被修改的事件数量

### `ADOFAILevel.get_tile_decoration(floor, decoration_type=None)`
- 获取指定砖块的装饰物：
    - 只传 `floor`，返回该砖块的所有装饰物（列表）
    - 传 `floor` 和 `decoration_type`，返回该砖块所有该类型装饰物（列表）

### `ADOFAILevel.get_decoration_info(floor, decoration_type, index=0, *attrs)`
- 获取指定砖块、装饰物类型、索引的装饰物信息：
    - 不传 `attrs`，返回装饰物完整字典
    - 传1个属性名，返回该属性值
    - 传多个属性名，返回{属性:值}字典
    - 若找不到装饰物或属性，返回 None 或抛出 IndexError

### `ADOFAILevel.edit_decoration_info(floor, decoration_type, index=0, **kwargs)`
- 编辑指定砖块、装饰物类型、索引的装饰物属性：
    - 传入要修改的属性及新值，如 `edit_decoration_info(1, 'AddDecoration', 0, scale=1.5, tag='newtag')`
    - 若找不到装饰物，抛出 IndexError

### `ADOFAILevel.batch_edit_decoration(decoration_type, floor=None, **kwargs)`
- 批量修改装饰物属性：
    - 只传 `decoration_type`，全关卡批量修改该类型装饰物
    - 同时传 `decoration_type` 和 `floor`，只修改该砖块上的该类型装饰物
    - 返回实际被修改的装饰物数量

### `ADOFAILevel.batch_get_event_info(event_type, attr=None)`
- 批量获取所有指定类型事件的信息：
    - 只传 `event_type`，返回所有该类型事件的完整信息列表
    - 传 `event_type` 和 `attr`，返回所有该类型事件的该属性值列表（如 `[{attr: value}, ...]`）

### `ADOFAILevel.batch_get_decoration_info(decoration_type, attr=None)`
- 批量获取所有指定类型装饰物的信息：
    - 只传 `decoration_type`，返回所有该类型装饰物的完整信息列表
    - 传 `decoration_type` 和 `attr`，返回所有该类型装饰物的该属性值列表（如 `[{attr: value}, ...]`）

### `ADOFAILevel.add_event(floor, event_type, *args, **kwargs)`
- 向指定砖块添加事件。
    - `floor`：砖块编号（int）
    - `event_type`：事件类型（如 "MoveTrack"、"Twirl" 等）
    - `*args`：可选，若为 `'default'`，则使用默认事件属性（需配置 defaults.json）
    - `**kwargs`：自定义事件属性（如 `duration=1.5, tag="mytag"`）
- 插入规则：会插入到该砖块最后一个事件后面；若该砖块没有事件，则插入到第一个比该砖块编号大的事件前面，否则插入到末尾。

### `ADOFAILevel.remove_event(floor=None, event_type=None, index=None)`
- 删除事件，支持多种用法：
    - `remove_event(1)`：删除1号砖块的所有事件
    - `remove_event(1, "MoveTrack")`：删除1号砖块所有MoveTrack事件
    - `remove_event(1, "MoveTrack", 0)`：删除1号砖块第一个MoveTrack事件
    - `remove_event(event_type="Twirl")`：删除全关卡所有Twirl事件
    - `remove_event()`：删除所有事件（清空actions）
- 返回被删除的事件（单个或列表），找不到会抛出 IndexError。

### `ADOFAILevel.get_event_count(floor=None, event_type=None)`
- 统计事件数量：
    - 都不传：统计全关卡所有事件数量
    - 只传event_type：统计全关卡该类型事件数量
    - 只传floor：统计该砖块所有事件数量
    - floor和event_type都传：统计该砖块该类型事件数量

### `ADOFAILevel.get_decoration_count(floor=None, decoration_type=None)`
- 统计装饰物数量：
    - 都不传：统计全关卡所有装饰物数量
    - 只传decoration_type：统计全关卡该类型装饰物数量
    - 只传floor：统计该砖块所有装饰物数量
    - floor和decoration_type都传：统计该砖块该类型装饰物数量

### `ADOFAILevel.add_decoration(floor, decoration_type, *args, **kwargs)`
- 向指定砖块添加装饰物。
    - `floor`：砖块编号（int）
    - `decoration_type`：装饰物类型（如 "AddDecoration" 等）
    - `*args`：可选，若为 `'default'`，则使用默认装饰物属性（需配置 defaults.json）
    - `**kwargs`：自定义装饰物属性（如 `scale=2.0, tag="mytag"`）
- 插入规则：会插入到该砖块最后一个装饰物后面；若该砖块没有装饰物，则插入到第一个比该砖块编号大的装饰物前面，否则插入到末尾。

### `ADOFAILevel.remove_decoration(floor=None, decoration_type=None, index=None)`
- 删除装饰物，支持多种用法：
    - `remove_decoration(2)`：删除2号砖块的所有装饰物
    - `remove_decoration(2, "AddDecoration")`：删除2号砖块所有AddDecoration装饰物
    - `remove_decoration(2, "AddDecoration", 0)`：删除2号砖块第一个AddDecoration装饰物
    - `remove_decoration(decoration_type="AddDecoration")`：删除全关卡所有AddDecoration装饰物
    - `remove_decoration()`：删除所有装饰物（清空decorations）
- 返回被删除的装饰物（单个或列表），找不到会抛出 IndexError。

## 关卡格式兼容性
- 自动去除 UTF-8 BOM
- 自动修正尾随逗号等非标准 JSON 问题
- 输出文件严格还原 adofai 关卡风格：
    - Tab 缩进
    - angleData、parallax、position 等数组一行
    - actions、decorations 等对象数组每个对象一行
    - 其余对象递归缩进

## 交互式测试

运行：
```bash
python -m adobase.tests.test_level
```
即可弹窗选择输入输出文件，体验关卡格式转换与信息查看。

## 开发进度
- [x] 关卡文件读取（BOM/非标准 JSON 兼容）
- [x] 关卡文件写入/导出（adodai 风格格式化）
- [x] 关卡信息获取与打印（全部、基础、指定字段，参数校验）
- [x] 关卡信息编辑（安全校验）
- [x] 事件查找与单个/批量编辑
- [x] 装饰物查找与单个/批量编辑
- [x] 关卡内容增删改查（事件/装饰物的灵活增删改查）
- [x] 更复杂的事件/装饰物操作（批量、默认参数、灵活插入等）
- [x] 文件选择器交互测试
- [x] 单元测试

## 许可证
MIT License 