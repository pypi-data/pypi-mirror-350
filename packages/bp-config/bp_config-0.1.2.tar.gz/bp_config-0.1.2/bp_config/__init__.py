import os
import json
import yaml
import toml

__all__ = ["ConfigHandler"]


class ConfigHandler:
    def __init__(self):
        """初始化配置处理器

        Args:
            root: 配置文件的根目录路径，所有配置文件将基于此路径进行查找和存储
        """

    def read_config(self, filename):
        """读取并解析配置文件

        根据文件扩展名自动选择对应的解析器(YAML/JSON/TOML)来加载配置文件内容，
        支持UTF-8编码的中文字符

        Args:
            filename (str): 要读取的配置文件路径，可以是绝对路径或相对路径

        Returns:
            dict: 解析后的配置字典对象，包含配置文件中的所有键值对

        Raises:
            ValueError: 当文件格式不被支持时抛出
            FileNotFoundError: 当指定文件不存在时抛出
            IOError: 当文件读取失败时抛出
        """
        with open(filename, "r", encoding="utf-8") as f:
            ext = os.path.splitext(filename)[1].lower()
            if ext in (".yaml", ".yml"):
                return yaml.safe_load(f)
            elif ext == ".json":
                # 确保JSON解析时保留中文原样
                return json.load(f)
            elif ext == ".toml":
                # TOML文件读取时自动处理中文
                return toml.load(f)
            else:
                raise ValueError(f"不支持的配置文件格式: {ext}")

    def write_config(self, filename, config):
        """将配置数据写入指定文件

        根据文件扩展名自动选择对应的序列化器(YAML/JSON/TOML)将配置数据写入文件，
        支持UTF-8编码的中文字符

        Args:
            filename (str): 要写入的配置文件路径，可以是绝对路径或相对路径
            config (dict): 要写入的配置数据字典

        Raises:
            ValueError: 当文件格式不被支持时抛出
            IOError: 当文件写入失败时抛出
        """
        with open(filename, "w", encoding="utf-8") as f:
            ext = os.path.splitext(filename)[1].lower()
            if ext in (".yaml", ".yml"):
                # YAML输出优化：中文支持+美化格式
                yaml.safe_dump(config, f,
                             allow_unicode=True,
                             default_flow_style=False,
                             sort_keys=False,
                             indent=2,
                             width=80,
                             encoding='utf-8')
            elif ext == ".json":
                # JSON输出优化：中文不转义+美化格式
                json.dump(config, f,
                         ensure_ascii=False,
                         indent=4,
                         sort_keys=False)
            elif ext == ".toml":
                # TOML输出优化
                toml.dump(config, f)
            else:
                raise ValueError(f"不支持的配置文件格式: {ext}")
