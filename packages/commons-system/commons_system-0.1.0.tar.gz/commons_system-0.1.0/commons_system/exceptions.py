class SystemLibraryException(Exception):
    """系统库基础异常类"""

    def __init__(self, message: str, error_code: int = None, details: dict = None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.details = details or {}

    def __str__(self):
        error_info = f"[{self.error_code}] " if self.error_code else ""
        return f"{error_info}{self.message}"


class SystemNotSupportedException(SystemLibraryException):
    """系统不支持异常"""

    def __init__(self, message: str = "Current system is not supported", system_name: str = None):
        super().__init__(message, error_code=1001)
        self.system_name = system_name
        if system_name:
            self.details["system_name"] = system_name


class SoftwareNotFoundException(SystemLibraryException):
    """软件未找到异常"""

    def __init__(self, software_name: str, search_locations: list = None):
        message = f"Software '{software_name}' not found"
        super().__init__(message, error_code=2001)
        self.software_name = software_name
        self.search_locations = search_locations or []
        self.details.update({
            "software_name": software_name,
            "search_locations": self.search_locations
        })


class ProcessNotFoundException(SystemLibraryException):
    """进程未找到异常"""

    def __init__(self, process_identifier: str, identifier_type: str = "name"):
        message = f"Process with {identifier_type} '{process_identifier}' not found"
        super().__init__(message, error_code=3001)
        self.process_identifier = process_identifier
        self.identifier_type = identifier_type
        self.details.update({
            "process_identifier": process_identifier,
            "identifier_type": identifier_type
        })


class PermissionDeniedException(SystemLibraryException):
    """权限拒绝异常"""

    def __init__(self, operation: str, resource: str = None):
        message = f"Permission denied for operation: {operation}"
        if resource:
            message += f" on resource: {resource}"
        super().__init__(message, error_code=4001)
        self.operation = operation
        self.resource = resource
        self.details.update({
            "operation": operation,
            "resource": resource
        })


class RegistryAccessException(SystemLibraryException):
    """注册表访问异常"""

    def __init__(self, registry_path: str, operation: str = "read"):
        message = f"Failed to {operation} registry: {registry_path}"
        super().__init__(message, error_code=5001)
        self.registry_path = registry_path
        self.operation = operation
        self.details.update({
            "registry_path": registry_path,
            "operation": operation
        })


class ProcessOperationException(SystemLibraryException):
    """进程操作异常"""

    def __init__(self, pid: int, operation: str, reason: str = None):
        message = f"Failed to {operation} process {pid}"
        if reason:
            message += f": {reason}"
        super().__init__(message, error_code=6001)
        self.pid = pid
        self.operation = operation
        self.reason = reason
        self.details.update({
            "pid": pid,
            "operation": operation,
            "reason": reason
        })


class FileSystemException(SystemLibraryException):
    """文件系统异常"""

    def __init__(self, path: str, operation: str, reason: str = None):
        message = f"Failed to {operation} path: {path}"
        if reason:
            message += f" ({reason})"
        super().__init__(message, error_code=7001)
        self.path = path
        self.operation = operation
        self.reason = reason
        self.details.update({
            "path": path,
            "operation": operation,
            "reason": reason
        })


class ShortcutResolutionException(SystemLibraryException):
    """快捷方式解析异常"""

    def __init__(self, shortcut_path: str, reason: str = None):
        message = f"Failed to resolve shortcut: {shortcut_path}"
        if reason:
            message += f" ({reason})"
        super().__init__(message, error_code=8001)
        self.shortcut_path = shortcut_path
        self.reason = reason
        self.details.update({
            "shortcut_path": shortcut_path,
            "reason": reason
        })


# 异常映射表 - 便于根据错误码查找异常类型
EXCEPTION_CODE_MAP = {
    1001: SystemNotSupportedException,
    2001: SoftwareNotFoundException,
    3001: ProcessNotFoundException,
    4001: PermissionDeniedException,
    5001: RegistryAccessException,
    6001: ProcessOperationException,
    7001: FileSystemException,
    8001: ShortcutResolutionException,
}


def get_exception_by_code(error_code: int) -> type:
    """根据错误码获取异常类型"""
    return EXCEPTION_CODE_MAP.get(error_code, SystemLibraryException)
