# bp-config

一个支持 YAML/JSON/TOML 格式的配置文件处理器

## 功能特性

- 支持读取和写入 YAML、JSON、TOML 格式的配置文件
- 自动根据文件扩展名选择对应的解析器
- 支持 UTF-8 编码，完美处理中文内容
- 简洁易用的 API 设计

## 安装

```bash
pip install bp-config
```

快速开始

```python

from bp_config import ConfigHandler

# 初始化处理器
handler = ConfigHandler()

# 读取配置
config = handler.read_config("config.yaml")

# 修改配置
config["new_key"] = "value"

# 写入配置
handler.write_config("config.yaml", config)

```


API 文档

```text
ConfigHandler()

read_config(filename)
读取并解析配置文件

参数:
filename: 配置文件名（相对或绝对路径）
返回: 解析后的字典对象
异常:
ValueError: 不支持的格式
FileNotFoundError: 文件不存在
IOError: 读取失败

write_config(filename, config)
将配置写入文件

参数:
filename: 要写入的文件名
config: 要写入的配置字典
异常:
ValueError: 不支持的格式
IOError: 写入失败
```

许可证
MIT 许可证 - 详见 LICENSE 文件

