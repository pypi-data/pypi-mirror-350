import os
import importlib.util
import sys
from typing import Optional


class PluginServer:
    @staticmethod
    def load_plugin(plugin_path: str):
        """加载指定路径的插件，并返回其模块对象"""
        if not os.path.exists(plugin_path):
            raise FileNotFoundError(f"Plugin file not found at: {plugin_path}")

        # 通过文件路径加载模块
        spec = importlib.util.spec_from_file_location("plugin_module", plugin_path)
        plugin_module = importlib.util.module_from_spec(spec)
        sys.modules["plugin_module"] = plugin_module
        spec.loader.exec_module(plugin_module)
        return plugin_module

    @staticmethod
    def start_server(plugin_path: str, plugin_class_name: str, host: Optional[str] = "0.0.0.0",
                     port: Optional[int] = 8989):
        """根据插件路径和插件类名启动服务"""
        try:
            # 动态加载插件
            plugin_module = PluginServer.load_plugin(plugin_path)

            # 获取用户指定的插件类
            plugin_class = getattr(plugin_module, plugin_class_name, None)
            if plugin_class is None:
                raise AttributeError(f"{plugin_class_name} class not found in {plugin_path}")

            # 实例化并启动插件服务
            plugin_instance = plugin_class(host=host, port=port)
            plugin_instance.serve()

        except Exception as e:
            print(f"Failed to start plugin server: {e}")
            raise


if __name__ == "__main__":
    # 从环境变量获取插件路径和插件类名
    plugin_path = os.getenv("PLUGIN_PATH")
    plugin_class_name = os.getenv("PLUGIN_CLASS_NAME")

    if plugin_path and plugin_class_name:
        # 启动服务器
        PluginServer.start_server(plugin_path, plugin_class_name)
    else:
        print("PLUGIN_PATH and PLUGIN_CLASS_NAME environment variables must be set.")
