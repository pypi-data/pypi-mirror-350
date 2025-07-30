import json
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List, Dict, Any


@dataclass
class Process:
    """进程信息数据类"""
    # 进程ID
    pid: int
    # 进程名
    name: str
    # 可执行文件路径
    exe_path: Optional[str] = None
    # 进程状态
    status: str = "unknown"
    # CPU使用率
    cpu_percent: float = 0.0
    # 内存使用量(MB)
    memory_mb: float = 0.0
    # 创建时间戳
    create_time: Optional[float] = None
    # 命令行参数
    cmdline: List[str] = field(default_factory=list)
    # 工作目录
    cwd: Optional[str] = None
    # 用户名
    username: Optional[str] = None
    # 父进程ID
    parent_pid: Optional[int] = None
    # 线程数
    num_threads: int = 0
    # 网络连接
    connections: List[Dict] = field(default_factory=list)
    # 打开的文件
    open_files: List[str] = field(default_factory=list)
    # 额外元数据
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "pid": self.pid,
            "name": self.name,
            "exe_path": self.exe_path,
            "status": self.status,
            "cpu_percent": self.cpu_percent,
            "memory_mb": self.memory_mb,
            "create_time": self.create_time,
            "cmdline": self.cmdline,
            "cwd": self.cwd,
            "username": self.username,
            "parent_pid": self.parent_pid,
            "num_threads": self.num_threads,
            "connections": self.connections,
            "open_files": self.open_files,
            "metadata": self.metadata
        }

    def to_json(self, **kwargs) -> str:
        """转换为JSON格式"""
        return json.dumps(self.to_dict(), ensure_ascii=False, **kwargs)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ProcessInfo":
        """从字典创建实例"""
        return cls(**data)

    @classmethod
    def from_json(cls, json_str: str) -> "ProcessInfo":
        """从JSON字符串创建实例"""
        data = json.loads(json_str)
        return cls.from_dict(data)

    def get_create_datetime(self) -> Optional[datetime]:
        """获取创建时间的datetime对象"""
        if self.create_time:
            return datetime.fromtimestamp(self.create_time)
        return None

    def get_running_time_seconds(self) -> Optional[float]:
        """获取运行时长（秒）"""
        if self.create_time:
            import time
            return time.time() - self.create_time
        return None

    def is_system_process(self) -> bool:
        """判断是否为系统进程"""
        if not self.exe_path:
            return True

        system_paths = [
            "C:\\Windows\\System32",
            "C:\\Windows\\SysWOW64",
            "C:\\Windows",
            "System32"
        ]

        return any(path.lower() in self.exe_path.lower() for path in system_paths)

    def get_install_directory(self) -> Optional[str]:
        """获取进程的安装目录"""
        if self.exe_path:
            import os
            return os.path.dirname(self.exe_path)
        return None

    def has_network_connections(self) -> bool:
        """检查是否有网络连接"""
        return len(self.connections) > 0

    def get_memory_usage_category(self) -> str:
        """获取内存使用量分类"""
        if self.memory_mb < 10:
            return "low"
        elif self.memory_mb < 100:
            return "medium"
        elif self.memory_mb < 500:
            return "high"
        else:
            return "very_high"

    def get_cpu_usage_category(self) -> str:
        """获取CPU使用率分类"""
        if self.cpu_percent < 1:
            return "idle"
        elif self.cpu_percent < 5:
            return "low"
        elif self.cpu_percent < 20:
            return "medium"
        elif self.cpu_percent < 50:
            return "high"
        else:
            return "very_high"

    def format_summary(self) -> str:
        """格式化进程摘要信息"""
        return (f"PID: {self.pid} | Name: {self.name} | "
                f"CPU: {self.cpu_percent:.1f}% | Memory: {self.memory_mb:.1f}MB | "
                f"Status: {self.status}")

    def __str__(self) -> str:
        return f"Process(pid={self.pid}, name={self.name}, status={self.status})"

    def __repr__(self) -> str:
        return self.__str__()
