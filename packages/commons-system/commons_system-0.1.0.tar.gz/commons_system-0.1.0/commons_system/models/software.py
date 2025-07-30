import glob
import json
import os
from dataclasses import dataclass, field
from typing import Optional, Dict, Any


@dataclass
class Software:
    # 软件名称
    name: str
    # 安装路径
    install_path: str
    # 版本信息
    version: str = "Unknown"
    # 发布商
    publisher: str = "Unknown"
    # 信息来源 (registry/filesystem/shortcut)
    source: str = "registry"
    # 显示名称
    display_name: Optional[str] = None
    # 卸载命令
    uninstall_string: Optional[str] = None
    # 安装日期
    install_date: Optional[str] = None
    # 占用空间(MB)
    size_mb: Optional[float] = None
    # 注册表键路径
    registry_key: Optional[str] = None
    # 额外元数据
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """初始化后处理"""
        if self.display_name is None:
            self.display_name = self.name

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "name": self.name,
            "install_path": self.install_path,
            "version": self.version,
            "publisher": self.publisher,
            "source": self.source,
            "display_name": self.display_name,
            "uninstall_cmd": self.uninstall_string,
            "install_date": self.install_date,
            "size_mb": self.size_mb,
            "registry_key": self.registry_key,
            "metadata": self.metadata
        }

    def to_json(self, **kwargs) -> str:
        """转换为JSON格式"""
        return json.dumps(self.to_dict(), ensure_ascii=False, **kwargs)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SoftwareInfo":
        """从字典创建实例"""
        return cls(**data)

    @classmethod
    def from_json(cls, json_str: str) -> "SoftwareInfo":
        """从JSON字符串创建实例"""
        data = json.loads(json_str)
        return cls.from_dict(data)

    def is_system_software(self) -> bool:
        """判断是否为系统软件"""
        system_publishers = [
            "Microsoft Corporation",
            "Microsoft",
            "Windows",
            "Intel Corporation",
            "NVIDIA Corporation",
            "AMD"
        ]

        return any(pub.lower() in self.publisher.lower() for pub in system_publishers)

    def has_valid_path(self) -> bool:
        """检查安装路径是否有效"""
        return os.path.exists(self.install_path) if self.install_path else False

    def get_executable_files(self) -> list:
        """获取安装目录下的可执行文件"""

        if not self.has_valid_path():
            return []

        exe_files = []
        try:
            # 查找.exe文件
            pattern = os.path.join(self.install_path, "*.exe")
            exe_files.extend(glob.glob(pattern))

            # 查找子目录中的.exe文件（只查找一层）
            for item in os.listdir(self.install_path):
                item_path = os.path.join(self.install_path, item)
                if os.path.isdir(item_path):
                    sub_pattern = os.path.join(item_path, "*.exe")
                    exe_files.extend(glob.glob(sub_pattern))
        except (OSError, PermissionError):
            pass

        return exe_files

    def __str__(self) -> str:
        return f"Software(name={self.name}, version={self.version}, path={self.install_path})"

    def __repr__(self) -> str:
        return self.__str__()
