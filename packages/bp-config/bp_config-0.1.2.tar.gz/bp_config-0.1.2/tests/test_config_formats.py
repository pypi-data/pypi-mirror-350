import os
import unittest
from bp_config import ConfigHandler

class TestConfigFormats(unittest.TestCase):
    def setUp(self):
        self.handler = ConfigHandler()
        self.test_files = []
        self.test_data = {
            "名称": "测试配置",
            "作者": "张三",
            "版本": 1.0,
            "功能": ["读取", "写入", "解析"],
            "启用": True,
            "详情": {
                "描述": "这是一个测试配置文件",
                "创建时间": "2023-01-01"
            }
        }
        
    def tearDown(self):
        # 清理测试文件
        for file in self.test_files:
            if os.path.exists(file):
                os.remove(file)

    def test_json_format(self):
        """测试JSON格式的读写"""
        filename = "test_config.json"
        self.test_files.append(filename)
        
        # 写入测试
        self.handler.write_config(filename, self.test_data)
        self.assertTrue(os.path.exists(filename))
        
        # 读取测试
        loaded_data = self.handler.read_config(filename)
        self.assertEqual(loaded_data, self.test_data)

    def test_yaml_format(self):
        """测试YAML格式的读写"""
        filename = "test_config.yaml"
        self.test_files.append(filename)
        
        # 写入测试
        self.handler.write_config(filename, self.test_data)
        self.assertTrue(os.path.exists(filename))
        
        # 读取测试
        loaded_data = self.handler.read_config(filename)
        self.assertEqual(loaded_data, self.test_data)

    def test_toml_format(self):
        """测试TOML格式的读写"""
        filename = "test_config.toml"
        self.test_files.append(filename)
        
        # 写入测试
        self.handler.write_config(filename, self.test_data)
        self.assertTrue(os.path.exists(filename))
        
        # 读取测试
        loaded_data = self.handler.read_config(filename)
        self.assertEqual(loaded_data, self.test_data)

if __name__ == '__main__':
    unittest.main()
