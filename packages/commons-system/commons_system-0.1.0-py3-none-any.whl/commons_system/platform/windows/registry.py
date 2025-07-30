import winreg
from typing import Dict, Optional
import os
import re
from loguru import logger

from commons_system.exceptions import (
    RegistryAccessException,
    PermissionDeniedException
)
from commons_system.models.software import Software


class RegistryScanner:
    def __init__(self):
        self.registry_paths = [
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"),
            (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall")
        ]

    def scan_uninstall_entries(self) -> Dict[str, Software]:
        """扫描注册表卸载信息获取软件列表"""
        software_dict = {}

        for hkey, subkey_path in self.registry_paths:
            try:
                entries = self._scan_registry_path(hkey, subkey_path)
                software_dict.update(entries)
            except RegistryAccessException as e:
                # 记录错误但继续处理其他路径
                logger.warning(f"无法访问注册表路径 {hkey} {subkey_path}: {e}")
                continue

        return software_dict

    def _scan_registry_path(self, hkey: int, subkey_path: str) -> Dict[str, Software]:
        """扫描单个注册表路径"""
        software_dict = {}

        try:
            with winreg.OpenKey(hkey, subkey_path) as key:
                num_subkeys = winreg.QueryInfoKey(key)[0]

                for i in range(num_subkeys):
                    try:
                        subkey_name = winreg.EnumKey(key, i)
                        with winreg.OpenKey(key, subkey_name) as subkey:
                            software = self._extract_software(subkey, subkey_path, subkey_name)
                            if software:
                                software_dict[software.name] = software
                    except Exception as e:
                        # 跳过无法访问的条目
                        logger.warning(f"无法访问注册表条目 {subkey_path}\\{subkey_name}: {e}")
                        continue

        except FileNotFoundError:
            raise RegistryAccessException(subkey_path, "access")
        except PermissionError:
            raise PermissionDeniedException("registry access", subkey_path)

        return software_dict

    def _extract_software(self, registry_key, registry_path: str, subkey_name: str) -> Optional[Software]:
        """从注册表项提取软件信息"""
        try:
            # 获取显示名称
            display_name = self._get_registry_value(registry_key, "DisplayName")
            if not display_name:
                return None

            # 获取安装路径
            install_path = self._get_install_path(registry_key)
            if not install_path or not os.path.exists(install_path):
                return None

            software = Software(
                name=display_name,
                install_path=install_path,
                version=self._get_registry_value(registry_key, "DisplayVersion") or "Unknown",
                publisher=self._get_registry_value(registry_key, "Publisher") or "Unknown",
                source="registry",
                display_name=display_name,
                uninstall_string=self._get_registry_value(registry_key, "UninstallString"),
                install_date=self._get_registry_value(registry_key, "InstallDate"),
                registry_key=f"{registry_path}\\{subkey_name}"
            )

            # 获取软件大小
            size_value = self._get_registry_value(registry_key, "EstimatedSize")
            if size_value:
                try:
                    # EstimatedSize 通常以KB为单位
                    software.size_mb = float(size_value) / 1024
                except (ValueError, TypeError):
                    pass

            # 添加额外的元数据
            software.metadata.update({
                "display_icon": self._get_registry_value(registry_key, "DisplayIcon"),
                "install_location": self._get_registry_value(registry_key, "InstallLocation"),
                "modify_path": self._get_registry_value(registry_key, "ModifyPath"),
                "help_link": self._get_registry_value(registry_key, "HelpLink"),
                "url_info_about": self._get_registry_value(registry_key, "URLInfoAbout"),
                "comments": self._get_registry_value(registry_key, "Comments")
            })

            return software

        except Exception as e:
            logger.warning(f"Extract software info failed: {e}")
            return None

    def _get_install_path(self, registry_key) -> Optional[str]:
        """获取软件安装路径"""
        # 方法1: 从InstallLocation获取
        install_location = self._get_registry_value(registry_key, "InstallLocation")
        if install_location and os.path.exists(install_location):
            return install_location

        # 方法2: 从DisplayIcon获取
        display_icon = self._get_registry_value(registry_key, "DisplayIcon")
        if display_icon and display_icon.endswith(".exe"):
            icon_dir = os.path.dirname(display_icon)
            if os.path.exists(icon_dir):
                return icon_dir

        # 方法3: 从UninstallString获取
        uninstall_string = self._get_registry_value(registry_key, "UninstallString")
        if uninstall_string:
            # 尝试提取路径
            match = re.search(r'"([^"]+)"', uninstall_string)
            if match:
                uninstall_exe = match.group(1)
                if os.path.exists(uninstall_exe):
                    return os.path.dirname(uninstall_exe)

        return None

    @staticmethod
    def _get_registry_value(registry_key, value_name: str) -> Optional[str]:
        """获取注册表值"""
        try:
            value, _ = winreg.QueryValueEx(registry_key, value_name)
            return str(value) if value else None
        except FileNotFoundError:
            return None
        except Exception as e:
            logger.warning(f"无法获取注册表值 {value_name}: {e}")
            return None
