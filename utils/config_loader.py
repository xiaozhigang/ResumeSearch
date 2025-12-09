"""
配置加载器
"""
import yaml
import os
from typing import Dict, Any


class ConfigLoader:
    """配置加载器类"""

    _instance = None
    _config = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._config is None:
            self.load_config()

    def load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        config_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'config',
            'config.yaml'
        )

        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                self._config = yaml.safe_load(f)
            print(f"配置文件加载成功: {config_path}")
            return self._config
        except Exception as e:
            print(f"配置文件加载失败: {e}")
            raise

    def get(self, key: str, default: Any = None) -> Any:
        """
        获取配置项
        支持点号分隔的多层级配置，例如: openai.api_key
        """
        if self._config is None:
            self.load_config()

        keys = key.split('.')
        value = self._config

        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default

        return value

    def get_openai_config(self) -> Dict[str, Any]:
        """获取OpenAI配置"""
        return self.get('openai', {})

    def get_big_company_config(self) -> Dict[str, Any]:
        """获取大厂判断标准配置"""
        return self.get('big_company', {})

    def get_negative_check_config(self) -> Dict[str, Any]:
        """获取负面舆情检索配置"""
        return self.get('negative_check', {})

    def get_api_config(self) -> Dict[str, Any]:
        """获取API配置"""
        return self.get('api', {})

    def get_concurrent_config(self) -> Dict[str, Any]:
        """获取并发配置"""
        return self.get('concurrent', {})


# 全局配置实例
config = ConfigLoader()
