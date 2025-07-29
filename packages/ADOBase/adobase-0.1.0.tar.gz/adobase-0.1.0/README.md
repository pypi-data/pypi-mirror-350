# ADOBase

ADOBase 是一个专为 ADOFAI 游戏 .adofai 关卡文件设计的 Python 库，支持关卡文件的读取、写入、格式转换、信息提取与编辑等操作。

## 主要功能
- **读取 .adofai 关卡文件**（自动去除 BOM，自动修正非标准 JSON，如尾随逗号）
- **写入/导出关卡文件**（支持标准 JSON 和 adofai 原格式风格，缩进、数组、对象数组等完全还原）
- **关卡信息提取、打印与编辑**（支持打印全部、基础或指定字段信息，参数校验，支持关卡信息字段的安全编辑）
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

# 打印全部关卡信息（settings 下所有字段）
level.print_info()

# 打印关卡基础信息（曲名、曲师、谱师）
level.print_info('levelbase')

# 打印指定字段（如 bpm、难度）
level.print_info('bpm', 'difficulty')

# 打印不存在的字段会报错
# level.print_info('notexist')  # KeyError: 关卡文件中不存在字段: notexist

# 编辑关卡信息（如修改版本号和 BPM）
level.edit_info(version=15, bpm=180)

# 验证修改
level.print_info('version', 'bpm')

# 导出为标准 JSON 文件（无 BOM，adodai 风格缩进）
level.export('output.json', as_original=False)

# 导出为 adofai 文件（加 BOM，adodai 风格缩进）
level.export('output.adofai', as_original=True)
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

### `ADOFAILevel.print_info(*fields)`
- 打印关卡信息：
    - 不传参数时，打印 settings 下所有字段及其值（完整关卡信息）
    - 传参数为 `'levelbase'` 时，打印关卡基础信息（曲名 song、曲师 artist、谱师 author）
    - 传参数为其它字段时，只打印指定字段，字段不存在则抛出异常

### `ADOFAILevel.edit_info(**kwargs)`
- 编辑关卡信息：
    - 传入要修改的字段和值，如 `level.edit_info(version=15, bpm=180)`
    - 字段不存在会抛出异常，防止误操作

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
- [x] 关卡信息打印（全部、基础、指定字段，参数校验）
- [x] 关卡信息编辑（安全校验）
- [x] 文件选择器交互测试
- [x] 单元测试
- [ ] 关卡内容增删改查（计划中）
- [ ] 更复杂的事件/装饰物操作（计划中）

## 许可证
MIT License 