from typing import List, Optional, Dict, Any

import psutil

from ...exceptions import ProcessNotFoundException, ProcessOperationException, PermissionDeniedException
from ...models.process import Process


class ProcessManager:
    """Windows进程管理器"""

    def __init__(self):
        self._process_cache = {}
        self._cache_timeout = 5  # 缓存超时时间（秒）
        self._last_cache_time = 0

    def get_all_processes(self, include_details: bool = True) -> List[Process]:
        """
        获取所有运行中的进程信息

        Args:
            include_details: 是否包含详细信息（网络连接、打开文件等）

        Returns:
            进程信息列表
        """
        processes = []

        for proc in psutil.process_iter():
            try:
                process_info = self._create_process_info(proc, include_details)
                if process_info:
                    processes.append(process_info)
            except (psutil.NoSuchProcess, psutil.ZombieProcess):
                # 进程已不存在或是僵尸进程
                continue
            except Exception:
                # 其他异常，跳过该进程
                continue

        return processes

    def get_process_by_pid(self, pid: int, include_details: bool = True) -> Optional[Process]:
        """
        根据PID获取进程信息

        Args:
            pid: 进程ID
            include_details: 是否包含详细信息

        Returns:
            Process对象，如果进程不存在则返回None
        """
        try:
            proc = psutil.Process(pid)
            return self._create_process_info(proc, include_details)
        except psutil.NoSuchProcess:
            return None
        except Exception:
            return None

    def get_processes_by_name(self, process_name: str, exact_match: bool = False, include_details: bool = True) -> List[
        Process]:
        """
        根据进程名获取进程信息

        Args:
            process_name: 进程名
            exact_match: 是否精确匹配
            include_details: 是否包含详细信息

        Returns:
            匹配的进程信息列表
        """
        processes = []
        process_name_lower = process_name.lower()

        for proc in psutil.process_iter(['pid', 'name']):
            try:
                proc_name = proc.info['name'].lower()

                if exact_match:
                    if proc_name == process_name_lower:
                        process_info = self._create_process_info(psutil.Process(proc.info['pid']), include_details)
                        if process_info:
                            processes.append(process_info)
                else:
                    if process_name_lower in proc_name:
                        process_info = self._create_process_info(psutil.Process(proc.info['pid']), include_details)
                        if process_info:
                            processes.append(process_info)

            except (psutil.NoSuchProcess, psutil.ZombieProcess):
                continue
            except Exception:
                continue

        return processes

    def filter_processes(self, processes: List[Process], **filters) -> List[Process]:
        """
        按条件筛选进程

        Args:
            processes: 进程列表
            **filters: 筛选条件
                - name: 进程名包含指定字符串
                - cpu_percent_min: 最小CPU使用率
                - cpu_percent_max: 最大CPU使用率
                - memory_mb_min: 最小内存使用量(MB)
                - memory_mb_max: 最大内存使用量(MB)
                - exclude_system: 是否排除系统进程
                - status: 进程状态
                - username: 用户名
                - has_connections: 是否有网络连接

        Returns:
            筛选后的进程列表
        """
        filtered = processes

        # 按进程名筛选
        if 'name' in filters:
            name_filter = filters['name'].lower()
            filtered = [p for p in filtered if name_filter in p.name.lower()]

        # 按CPU使用率筛选
        if 'cpu_percent_min' in filters:
            min_cpu = filters['cpu_percent_min']
            filtered = [p for p in filtered if p.cpu_percent >= min_cpu]

        if 'cpu_percent_max' in filters:
            max_cpu = filters['cpu_percent_max']
            filtered = [p for p in filtered if p.cpu_percent <= max_cpu]

        # 按内存使用量筛选
        if 'memory_mb_min' in filters:
            min_memory = filters['memory_mb_min']
            filtered = [p for p in filtered if p.memory_mb >= min_memory]

        if 'memory_mb_max' in filters:
            max_memory = filters['memory_mb_max']
            filtered = [p for p in filtered if p.memory_mb <= max_memory]

        # 排除系统进程
        if filters.get('exclude_system', False):
            filtered = [p for p in filtered if not p.is_system_process()]

        # 按进程状态筛选
        if 'status' in filters:
            status_filter = filters['status']
            filtered = [p for p in filtered if p.status == status_filter]

        # 按用户名筛选
        if 'username' in filters:
            username_filter = filters['username']
            filtered = [p for p in filtered if p.username == username_filter]

        # 按网络连接筛选
        if 'has_connections' in filters:
            has_conn = filters['has_connections']
            if has_conn:
                filtered = [p for p in filtered if p.has_network_connections()]
            else:
                filtered = [p for p in filtered if not p.has_network_connections()]

        return filtered

    def kill_process(self, pid: int, force: bool = False) -> bool:
        """
        终止指定PID的进程

        Args:
            pid: 进程ID
            force: 是否强制终止

        Returns:
            True表示成功，False表示失败

        Raises:
            ProcessNotFoundException: 进程不存在
            ProcessOperationException: 进程操作失败
            PermissionDeniedException: 权限不足
        """
        try:
            proc = psutil.Process(pid)

            if force:
                proc.kill()  # 强制终止
            else:
                proc.terminate()  # 优雅终止

            # 等待进程终止
            try:
                proc.wait(timeout=5)
            except psutil.TimeoutExpired:
                if not force:
                    # 超时后强制终止
                    proc.kill()
                    proc.wait(timeout=3)

            return True

        except psutil.NoSuchProcess:
            raise ProcessNotFoundException(str(pid), "pid")
        except psutil.AccessDenied:
            raise PermissionDeniedException("kill process", f"PID {pid}")
        except Exception as e:
            raise ProcessOperationException(pid, "kill", str(e))

    def kill_processes_by_name(self, process_name: str, exact_match: bool = True, force: bool = False) -> int:
        """
        根据进程名终止进程

        Args:
            process_name: 进程名
            exact_match: 是否精确匹配
            force: 是否强制终止

        Returns:
            成功终止的进程数量
        """
        processes = self.get_processes_by_name(process_name, exact_match, include_details=False)
        killed_count = 0

        for process_info in processes:
            try:
                if self.kill_process(process_info.pid, force):
                    killed_count += 1
            except Exception:
                # 忽略单个进程终止失败
                continue

        return killed_count

    def suspend_process(self, pid: int) -> bool:
        """暂停进程"""
        try:
            proc = psutil.Process(pid)
            proc.suspend()
            return True
        except psutil.NoSuchProcess:
            raise ProcessNotFoundException(str(pid), "pid")
        except psutil.AccessDenied:
            raise PermissionDeniedException("suspend process", f"PID {pid}")
        except Exception as e:
            raise ProcessOperationException(pid, "suspend", str(e))

    def resume_process(self, pid: int) -> bool:
        """恢复进程"""
        try:
            proc = psutil.Process(pid)
            proc.resume()
            return True
        except psutil.NoSuchProcess:
            raise ProcessNotFoundException(str(pid), "pid")
        except psutil.AccessDenied:
            raise PermissionDeniedException("resume process", f"PID {pid}")
        except Exception as e:
            raise ProcessOperationException(pid, "resume", str(e))

    def get_process_tree(self, pid: int) -> Dict[str, Any]:
        """获取进程树"""
        try:
            proc = psutil.Process(pid)
            tree = {'process': self._create_process_info(proc, False), 'children': []}

            for child in proc.children(recursive=True):
                try:
                    child_info = self._create_process_info(child, False)
                    if child_info:
                        tree['children'].append({
                            'process': child_info,
                            'children': []
                        })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue

            return tree

        except psutil.NoSuchProcess:
            raise ProcessNotFoundException(str(pid), "pid")
        except Exception as e:
            raise ProcessOperationException(pid, "get tree", str(e))

    def _create_process_info(self, proc: psutil.Process, include_details: bool = True) -> Optional[Process]:
        """从psutil.Process创建Process对象"""
        try:
            # 获取基本信息
            process_info = Process(
                pid=proc.pid,
                name=proc.name(),
                status=proc.status()
            )

            # 获取可执行文件路径
            try:
                process_info.exe_path = proc.exe()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

            # 获取CPU使用率
            try:
                process_info.cpu_percent = proc.cpu_percent()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

            # 获取内存信息
            try:
                memory_info = proc.memory_info()
                process_info.memory_mb = round(memory_info.rss / 1024 / 1024, 2)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

            # 获取创建时间
            try:
                process_info.create_time = proc.create_time()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

            # 获取命令行参数
            try:
                process_info.cmdline = proc.cmdline()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

            # 获取工作目录
            try:
                process_info.cwd = proc.cwd()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

            # 获取用户名
            try:
                process_info.username = proc.username()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

            # 获取父进程ID
            try:
                process_info.parent_pid = proc.ppid()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

            # 获取线程数
            try:
                process_info.num_threads = proc.num_threads()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

            # 获取详细信息（如果需要）
            if include_details:
                # 获取网络连接
                try:
                    connections = proc.connections()
                    process_info.connections = [
                        {
                            'family': conn.family.name if hasattr(conn.family, 'name') else str(conn.family),
                            'type': conn.type.name if hasattr(conn.type, 'name') else str(conn.type),
                            'local_address': f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else None,
                            'remote_address': f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else None,
                            'status': conn.status
                        }
                        for conn in connections
                    ]
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass

                # 获取打开的文件
                try:
                    open_files = proc.open_files()
                    process_info.open_files = [f.path for f in open_files]
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass

            return process_info

        except (psutil.NoSuchProcess, psutil.ZombieProcess):
            return None
        except Exception:
            return None
