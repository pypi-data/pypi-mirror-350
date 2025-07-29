import json
from .utils import parse_adofai_to_json_str, add_bom, remove_bom, to_adofai_style_json

class ADOFAILevel:
    def __init__(self, data: dict, raw_text: str = None):
        self.data = data
        self.raw_text = raw_text  # 保存原始文本，便于原样导出

    @classmethod
    def load(cls, filepath: str):
        """从 .adofai 文件加载关卡，自动修正为标准 JSON，自动去除 BOM"""
        with open(filepath, 'r', encoding='utf-8') as f:
            raw_text = f.read()
        raw_text = remove_bom(raw_text)
        json_str = parse_adofai_to_json_str(raw_text)
        data = json.loads(json_str)
        return cls(data, raw_text=raw_text)

    def save(self, filepath: str):
        """保存关卡到 .adofai 文件（标准 JSON 格式，无 BOM，adodai 风格缩进）"""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(to_adofai_style_json(self.data))

    def export(self, filepath: str, as_original: bool = False):
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

    def print_info(self, *fields):
        """
        打印关卡信息。
        - 不传参数时，打印 settings 下所有字段及其值
        - 传参数为 'levelbase' 时，打印关卡基本信息（song, artist, author）
        - 传参数时，只打印指定字段，若字段不存在则抛出异常
        """
        settings = self.data.get('settings', {})
        if not fields:
            for k, v in settings.items():
                print(f"{k}: {v}")
        elif len(fields) == 1 and fields[0] == 'levelbase':
            for k in ('song', 'artist', 'author'):
                print(f"{k}: {settings.get(k, '')}")
        else:
            for field in fields:
                if field not in settings:
                    raise KeyError(f"关卡文件中不存在字段: {field}")
                print(f"{field}: {settings[field]}")

    def edit_info(self, **kwargs):
        """
        编辑关卡信息。
        允许用户传入要编辑的字段和值，若字段不存在则抛出异常。
        用法：level.edit_info(song="新曲名", bpm=180)
        """
        settings = self.data.get('settings', {})
        for k, v in kwargs.items():
            if k not in settings:
                raise KeyError(f"关卡文件中不存在字段: {k}")
            settings[k] = v 