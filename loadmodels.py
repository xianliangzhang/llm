import os
import json
from pathlib import Path

class LMStudioConfigManager:
    def __init__(self):
        # Windows上LM Studio的标准配置目录
        self.lm_studio_dir = Path(os.getenv('APPDATA')) / 'LMStudio'
        self.config_file_path = self.lm_studio_dir / 'config.json'
        self.models_dir = self.lm_studio_dir / 'models'
        
    def create_directories(self):
        """创建必要的目录结构"""
        self.lm_studio_dir.mkdir(exist_ok=True)
        self.models_dir.mkdir(exist_ok=True)
        print(f"LM Studio主目录: {self.lm_studio_dir}")
        print(f"模型存储目录: {self.models_dir}")
        
    def get_default_config(self):
        """获取默认配置模板"""
        return {
            "version": "1.0",
            "default_model": "local_gguf_model",
            "models_directory": str(self.models_dir),
            "model_config": {
                "name": "local_gguf_model",
                "type": "llama",
                "path": "C:\\\\Users\\\\YourUsername\\\\.cache\\\\huggingface\\\\hub\\\\models--TheBloke--Llama-2-7B-Chat-GGUF\\\\snapshots\\\\latest\\\\llama-2-7b-chat.Q4_K_M.gguf",
                "context_length": 4096,
                "max_tokens": 2048,
                "temperature": 0.7,
                "top_p": 0.9,
                "repetition_penalty": 1.15,
                "n_gpu_layers": 20,
                "batch_size": 512,
                "threads": 8
            },
            "server_config": {
                "host": "127.0.0.1",
                "port": 8080,
                "cors_origin": "*",
                "ssl_enabled": False
            },
            "quantization": {
                "bits": 4,
                "method": "GGUF"
            }
        }
    
    def save_config(self, config=None):
        """保存配置文件到正确位置"""
        if config is None:
            config = self.get_default_config()
            
        # 创建目录
        self.create_directories()
        
        # 写入配置文件
        with open(self.config_file_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        print(f"配置文件已保存至: {self.config_file_path}")
        return self.config_file_path
    
    def load_config(self):
        """从标准位置加载配置文件"""
        try:
            with open(self.config_file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"配置文件不存在: {self.config_file_path}")
            return None
        except json.JSONDecodeError:
            print(f"配置文件格式错误: {self.config_file_path}")
            return None
    
    def update_model_path(self, new_path):
        """更新模型路径"""
        config = self.load_config()
        if config:
            config['model_config']['path'] = new_path
            self.save_config(config)
            print(f"模型路径已更新为: {new_path}")
        else:
            print("无法加载现有配置，创建新配置")
            default_config = self.get_default_config()
            default_config['model_config']['path'] = new_path
            self.save_config(default_config)

# 使用示例
if __name__ == "__main__":
    manager = LMStudioConfigManager()
    
    # 创建配置文件
    config_path = manager.save_config()
    
    # 显示配置文件位置
    print("\n配置文件位置说明:")
    print("-" * 50)
    print(f"Windows配置文件路径: {config_path}")
    print("或者手动创建: %APPDATA%\\LMStudio\\config.json")
    print("\n如果使用LM Studio GUI，也可以通过界面设置模型路径")
    print("此脚本主要用于自动化配置管理")
    
    # 提供路径查找帮助
    print(f"\nLM Studio根目录: {manager.lm_studio_dir}")
    print(f"推荐模型存储位置: {manager.models_dir}")
