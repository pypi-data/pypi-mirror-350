import os
from typing import Dict, Optional

from commons_system.exceptions import (
    PermissionDeniedException,
    ShortcutResolutionException
)


class ShortcutResolver:
    """Windows快捷方式解析器 - 提供多种解析方法"""

    def __init__(self):
        self.desktop_paths = [
            os.path.join(os.path.expanduser("~"), "Desktop"),
            r"C:\Users\Public\Desktop",
            os.path.join(os.path.expanduser("~"), "OneDrive", "Desktop")  # OneDrive桌面
        ]

        # 检查win32com是否可用
        self._win32com_available = self._check_win32com()

    @staticmethod
    def _check_win32com() -> bool:
        """检查win32com是否可用"""
        try:
            import win32com.client
            return True
        except (ImportError, AttributeError) as e:
            print(f"Warning: win32com not available ({e}), using alternative method")
            return False

    def scan_desktop_shortcuts(self) -> Dict[str, str]:
        """扫描桌面快捷方式"""
        shortcuts = {}

        for desktop_path in self.desktop_paths:
            if os.path.exists(desktop_path):
                try:
                    path_shortcuts = self._scan_shortcut_directory(desktop_path)
                    shortcuts.update(path_shortcuts)
                except PermissionDeniedException:
                    continue

        return shortcuts

    def _scan_shortcut_directory(self, directory: str) -> Dict[str, str]:
        """扫描单个目录的快捷方式"""
        shortcuts = {}

        try:
            for file in os.listdir(directory):
                if file.lower().endswith(".lnk"):
                    lnk_path = os.path.join(directory, file)
                    target_path = self.resolve_shortcut(lnk_path)
                    if target_path and os.path.exists(target_path):
                        software_name = file[:-4]  # 移除.lnk后缀
                        install_dir = os.path.dirname(target_path)
                        shortcuts[software_name] = install_dir
        except PermissionError:
            raise PermissionDeniedException("shortcut scan", directory)

        return shortcuts

    def resolve_shortcut(self, shortcut_path: str) -> Optional[str]:
        """
        解析快捷方式目标路径
        优先使用win32com，失败时使用备用方案
        """
        # 方法1: 尝试使用win32com
        if self._win32com_available:
            try:
                return self._resolve_with_win32com(shortcut_path)
            except Exception:
                # win32com方法失败，继续尝试备用方案
                pass

        # 方法2: 使用二进制解析方法
        try:
            return self._resolve_with_binary_parser(shortcut_path)
        except Exception as e:
            raise ShortcutResolutionException(shortcut_path, str(e))

    @staticmethod
    def _resolve_with_win32com(shortcut_path: str) -> Optional[str]:
        """使用win32com解析快捷方式"""
        try:
            import win32com.client
            shell = win32com.client.Dispatch("WScript.Shell")
            shortcut = shell.CreateShortCut(shortcut_path)
            target_path = shortcut.Targetpath

            # 验证目标路径是否有效
            if target_path and os.path.exists(target_path):
                return target_path

            return None

        except Exception as e:
            raise ShortcutResolutionException(shortcut_path, f"win32com error: {str(e)}")

    def _resolve_with_binary_parser(self, shortcut_path: str) -> Optional[str]:
        """
        使用二进制解析方法解析.lnk文件
        这是一个不依赖COM的备用方案
        """
        try:
            with open(shortcut_path, "rb") as f:
                # 读取.lnk文件头
                header = f.read(76)
                if len(header) != 76:
                    return None

                # 检查文件签名
                if header[:4] != b"L\x00\x00\x00":
                    return None

                # 解析链接标志
                link_flags = struct.unpack("<I", header[20:24])[0]

                # 跳过可选的ItemID列表
                if link_flags & 0x01:  # HasLinkTargetIDList
                    idlist_size = struct.unpack("<H", f.read(2))[0]
                    f.read(idlist_size)

                # 读取LinkInfo
                if link_flags & 0x02:  # HasLinkInfo
                    linkinfo_size = struct.unpack("<I", f.read(4))[0]
                    linkinfo_data = f.read(linkinfo_size - 4)

                    # 尝试从LinkInfo中提取路径
                    target_path = self._extract_path_from_linkinfo(linkinfo_data)
                    if target_path and os.path.exists(target_path):
                        return target_path

                # 尝试读取字符串数据
                return self._extract_path_from_strings(f, link_flags)

        except Exception as e:
            raise ShortcutResolutionException(shortcut_path, f"Binary parser error: {str(e)}")

    def _extract_path_from_linkinfo(self, linkinfo_data: bytes) -> Optional[str]:
        """从LinkInfo数据中提取路径"""
        try:
            if len(linkinfo_data) < 16:
                return None

            # 读取偏移量
            local_path_offset = struct.unpack("<I", linkinfo_data[16:20])[0] if len(linkinfo_data) >= 20 else 0

            if local_path_offset > 0 and local_path_offset < len(linkinfo_data):
                # 提取本地路径
                path_start = local_path_offset - 4  # 调整偏移
                if path_start >= 0:
                    path_data = linkinfo_data[path_start:]
                    # 查找null终止符
                    null_pos = path_data.find(b"\x00")
                    if null_pos > 0:
                        path = path_data[:null_pos].decode("cp1252", errors="ignore")
                        if path and "\\" in path:
                            return path

            return None

        except Exception:
            return None

    @staticmethod
    def _extract_path_from_strings(f, link_flags: int) -> Optional[str]:
        """从字符串数据中提取路径"""
        try:
            # 尝试读取字符串数据
            string_flags = [
                (0x04, "name"),  # HasName
                (0x08, "relative_path"),  # HasRelativePath
                (0x10, "working_dir"),  # HasWorkingDir
                (0x20, "arguments"),  # HasArguments
                (0x40, "icon_location")  # HasIconLocation
            ]

            for flag, name in string_flags:
                if link_flags & flag:
                    try:
                        # 读取字符串长度
                        str_len = struct.unpack("<H", f.read(2))[0]
                        if str_len > 0:
                            # 读取字符串数据
                            str_data = f.read(str_len * 2)  # Unicode字符串
                            string_value = str_data.decode("utf-16le", errors="ignore").rstrip("\x00")

                            # 如果是相对路径或工作目录，且包含可执行文件
                            if name in ["relative_path", "working_dir"] and string_value:
                                if string_value.lower().endswith(".exe") and os.path.exists(string_value):
                                    return string_value
                                elif os.path.exists(string_value) and os.path.isdir(string_value):
                                    # 检查目录中是否有exe文件
                                    for file in os.listdir(string_value):
                                        if file.lower().endswith(".exe"):
                                            full_path = os.path.join(string_value, file)
                                            if os.path.exists(full_path):
                                                return full_path
                    except Exception:
                        continue

            return None

        except Exception:
            return None

    def get_shortcut_info(self, shortcut_path: str) -> Dict[str, str]:
        """
        获取快捷方式详细信息
        如果win32com不可用，返回基本信息
        """
        if self._win32com_available:
            try:
                return self._get_shortcut_info_win32com(shortcut_path)
            except Exception:
                pass

        # 备用方案：返回基本信息
        target_path = self.resolve_shortcut(shortcut_path)
        return {
            "target_path": target_path or "",
            "arguments": "",
            "working_directory": os.path.dirname(target_path) if target_path else "",
            "description": os.path.basename(shortcut_path)[:-4],
            "icon_location": "",
            "hotkey": "",
            "window_style": ""
        }

    def _get_shortcut_info_win32com(self, shortcut_path: str) -> Dict[str, str]:
        """使用win32com获取快捷方式详细信息"""
        try:
            import win32com.client
            shell = win32com.client.Dispatch("WScript.Shell")
            shortcut = shell.CreateShortCut(shortcut_path)

            return {
                "target_path": shortcut.Targetpath,
                "arguments": shortcut.Arguments,
                "working_directory": shortcut.WorkingDirectory,
                "description": shortcut.Description,
                "icon_location": shortcut.IconLocation,
                "hotkey": shortcut.Hotkey,
                "window_style": str(shortcut.WindowStyle)
            }

        except Exception as e:
            raise ShortcutResolutionException(shortcut_path, str(e))

    def create_shortcut(self, target_path: str, shortcut_path: str, **kwargs) -> bool:
        """
        创建快捷方式
        需要win32com支持
        """
        if not self._win32com_available:
            raise ShortcutResolutionException(shortcut_path, "Create shortcut requires win32com")

        try:
            import win32com.client
            shell = win32com.client.Dispatch("WScript.Shell")
            shortcut = shell.CreateShortCut(shortcut_path)

            shortcut.Targetpath = target_path

            # 设置可选参数
            if "arguments" in kwargs:
                shortcut.Arguments = kwargs["arguments"]
            if "working_directory" in kwargs:
                shortcut.WorkingDirectory = kwargs["working_directory"]
            if "description" in kwargs:
                shortcut.Description = kwargs["description"]
            if "icon_location" in kwargs:
                shortcut.IconLocation = kwargs["icon_location"]

            shortcut.save()
            return True

        except Exception as e:
            raise ShortcutResolutionException(shortcut_path, f"Create failed: {str(e)}")

    def delete_shortcut(self, shortcut_path: str) -> bool:
        """删除快捷方式"""
        try:
            if os.path.exists(shortcut_path):
                os.remove(shortcut_path)
                return True
            return False
        except Exception as e:
            raise ShortcutResolutionException(shortcut_path, f"Delete failed: {str(e)}")
