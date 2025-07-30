import os
import string
from typing import Dict, List

from commons_system.exceptions import FileSystemException, PermissionDeniedException


class FileSystemScanner:
    """多驱动器Windows文件系统扫描器"""

    def __init__(self):
        self.common_paths_templates = [
            r"{drive}:\Program Files",
            r"{drive}:\Program Files (x86)",
            r"{drive}:\ProgramData"
        ]

        # 用户相关路径（只在系统盘扫描）
        self.user_paths_templates = [
            # os.path.expanduser(r"~\AppData\Local"),
            # os.path.expanduser(r"~\AppData\Roaming")
        ]

    def scan_common_directories(self) -> Dict[str, str]:
        """扫描所有驱动器的常见安装目录"""
        software_dirs = {}

        available_drives = self._get_available_drives()
        for drive in available_drives:
            drive_paths = [template.format(drive=drive) for template in self.common_paths_templates]

            for base_path in drive_paths:
                if os.path.exists(base_path):
                    try:
                        entries = self._scan_directory(base_path)
                        # 为结果添加驱动器信息以避免重名冲突
                        for name, path in entries.items():
                            # 如果软件名已存在，添加驱动器标识
                            unique_name = name
                            if unique_name in software_dirs:
                                unique_name = f"{name} ({drive}:)"
                            software_dirs[unique_name] = path
                    except (PermissionDeniedException, FileSystemException):
                        continue

        # 扫描用户目录（只在当前用户的系统盘）
        for user_path in self.user_paths_templates:
            if os.path.exists(user_path):
                try:
                    entries = self._scan_directory(user_path)
                    for name, path in entries.items():
                        if name not in software_dirs:
                            software_dirs[name] = path
                except (PermissionDeniedException, FileSystemException):
                    continue

        return software_dirs

    @staticmethod
    def _get_available_drives() -> List[str]:
        """获取所有可用的驱动器列表"""
        available_drives = []

        # 检查A-Z所有可能的驱动器字母
        for drive_letter in string.ascii_uppercase:
            drive_path = f"{drive_letter}:\\"
            if os.path.exists(drive_path):
                try:
                    # 尝试列出驱动器内容来确认可访问
                    os.listdir(drive_path)
                    available_drives.append(drive_letter)
                except (PermissionError, OSError):
                    # 驱动器存在但不可访问（如光驱无盘）
                    continue

        return available_drives

    def _scan_directory(self, directory: str) -> Dict[str, str]:
        """扫描单个目录"""
        software_dirs = {}

        try:
            items = os.listdir(directory)
            for item in items:
                full_path = os.path.join(directory, item)
                if os.path.isdir(full_path):
                    if self._has_executable_files(full_path):
                        software_dirs[item] = full_path
        except PermissionError:
            raise PermissionDeniedException("directory scan", directory)
        except OSError as e:
            raise FileSystemException(directory, "scan", str(e))

        return software_dirs

    @staticmethod
    def _has_executable_files(directory: str) -> bool:
        """检查目录是否包含可执行文件"""
        try:
            # 检查根目录
            for file in os.listdir(directory):
                if file.lower().endswith(".exe"):
                    return True

            # 检查一级子目录
            for item in os.listdir(directory):
                item_path = os.path.join(directory, item)
                if os.path.isdir(item_path):
                    try:
                        for file in os.listdir(item_path):
                            if file.lower().endswith(".exe"):
                                return True
                    except (PermissionError, OSError):
                        continue
                    # 只检查几个子目录，避免深度递归
                    break
        except (PermissionError, OSError):
            pass

        return False

    @staticmethod
    def get_directory_info(directory: str) -> Dict[str, any]:
        """获取目录详细信息"""
        if not os.path.exists(directory):
            raise FileSystemException(directory, "access", "Directory does not exist")

        try:
            stat = os.stat(directory)
            exe_files = []
            total_files = 0

            # 收集可执行文件信息
            for root, dirs, files in os.walk(directory):
                total_files += len(files)
                for file in files:
                    if file.lower().endswith(".exe"):
                        exe_files.append(os.path.join(root, file))
                # 限制扫描深度
                if len(root.split(os.sep)) - len(directory.split(os.sep)) > 2:
                    dirs.clear()

            return {
                "path": directory,
                "exists": True,
                "size_bytes": stat.st_size,
                "created_time": stat.st_ctime,
                "modified_time": stat.st_mtime,
                "executable_files": exe_files,
                "total_files": total_files
            }

        except PermissionError:
            raise PermissionDeniedException("directory info", directory)
        except OSError as e:
            raise FileSystemException(directory, "get info", str(e))

    def get_scan_summary(self) -> Dict[str, any]:
        """获取扫描摘要信息"""
        available_drives = self._get_available_drives()
        scan_paths = []

        # 构建所有扫描路径
        for drive in available_drives:
            for template in self.common_paths_templates:
                path = template.format(drive=drive)
                scan_paths.append({
                    "path": path,
                    "exists": os.path.exists(path),
                    "accessible": self._is_path_accessible(path) if os.path.exists(path) else False
                })

        # 添加用户路径
        for user_path in self.user_paths_templates:
            scan_paths.append({
                "path": user_path,
                "exists": os.path.exists(user_path),
                "accessible": self._is_path_accessible(user_path) if os.path.exists(user_path) else False
            })

        return {
            "available_drives": available_drives,
            "total_drives": len(available_drives),
            "scan_paths": scan_paths,
            "accessible_paths": len([p for p in scan_paths if p["accessible"]])
        }

    @staticmethod
    def _is_path_accessible(path: str) -> bool:
        """检查路径是否可访问"""
        try:
            os.listdir(path)
            return True
        except (PermissionError, OSError):
            return False
