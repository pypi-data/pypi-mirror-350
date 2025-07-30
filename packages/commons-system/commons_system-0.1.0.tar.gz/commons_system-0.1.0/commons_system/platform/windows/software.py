import platform
import time
from datetime import datetime
from typing import Dict, Optional, List, Any

from commons_system.exceptions import SystemNotSupportedException
from commons_system.models.software import Software

if platform.system() == "Windows":
    from commons_system.platform.windows.registry import RegistryScanner
    from commons_system.platform.windows.filesystem import FileSystemScanner
    from commons_system.platform.windows.shortcut import ShortcutResolver
else:
    raise SystemNotSupportedException(f"Platform {platform.system()} is not supported yet")


class SoftwareManager:
    """
    软件管理器 - 提供完整的软件检测、管理和信息查询功能

    功能特性:
    - 多源软件信息检测 (注册表、文件系统、快捷方式)
    - 智能缓存机制
    - 模糊匹配和精确搜索
    - 软件分类和筛选
    - 数据导出和持久化
    - 异步扫描支持
    """

    def __init__(self, cache_timeout: int = 300, auto_refresh: bool = True):
        """
        初始化软件管理器

        Args:
            cache_timeout: 缓存超时时间(秒)，默认5分钟
            auto_refresh: 是否自动刷新过期缓存，默认True
        """
        self._cache_timeout = cache_timeout
        self._auto_refresh = auto_refresh

        # 缓存相关
        self._software_cache: Dict[str, Software] = {}
        self._cache_timestamp: float = 0
        self._cache_valid = False

        # 扫描器实例
        self._registry_scanner = RegistryScanner()
        self._filesystem_scanner = FileSystemScanner()
        self._shortcut_resolver = ShortcutResolver()

        # 统计信息
        self._scan_history: List[Dict] = []
        self._last_scan_duration: float = 0

        # 配置选项
        self._include_system_software = True
        self._min_confidence_score = 0.5

    # ==================== 核心API方法 ====================

    def get_software_install_path(self, software_name: str, fuzzy_match: bool = True) -> Optional[str]:
        """
        获取软件安装路径

        Args:
            software_name: 软件名称
            fuzzy_match: 是否启用模糊匹配

        Returns:
            软件安装路径，未找到返回None
        """
        software_info = self.get_software_info(software_name, fuzzy_match)
        return software_info.install_path if software_info else None

    def get_software_info(self, software_name: str, fuzzy_match: bool = True) -> Optional[Software]:
        """
        获取软件详细信息

        Args:
            software_name: 软件名称
            fuzzy_match: 是否启用模糊匹配

        Returns:
            Software对象，未找到返回None
        """
        self._ensure_cache_valid()

        # 精确匹配
        if software_name in self._software_cache:
            return self._software_cache[software_name]

        # 模糊匹配
        if fuzzy_match:
            matches = self._fuzzy_search(software_name, limit=1)
            return matches[0] if matches else None

        return None

    def get_all_software(self, refresh: bool = False) -> Dict[str, Software]:
        """
        获取所有已安装软件信息

        Args:
            refresh: 是否强制刷新缓存

        Returns:
            软件信息字典 {软件名称: Software}
        """
        if refresh:
            self.refresh_cache()
        else:
            self._ensure_cache_valid()

        return self._software_cache.copy()

    def search_software(self, keyword: str, limit: int = None, **filters) -> List[Software]:
        """
        搜索软件

        Args:
            keyword: 搜索关键词
            limit: 结果数量限制
            **filters: 额外筛选条件
                - publisher: 发布商筛选
                - version_pattern: 版本号模式匹配
                - size_min/size_max: 软件大小范围
                - source: 信息来源筛选

        Returns:
            匹配的软件信息列表
        """
        self._ensure_cache_valid()

        results = self._fuzzy_search(keyword, limit)

        # 应用额外筛选条件
        if filters:
            results = self._apply_filters(results, **filters)

        return results

    def find_software_by_path(self, path: str) -> List[Software]:
        """
        根据路径查找软件

        Args:
            path: 文件或目录路径

        Returns:
            匹配的软件信息列表
        """
        self._ensure_cache_valid()

        path = os.path.normpath(path).lower()
        matches = []

        for software in self._software_cache.values():
            if software.install_path and path in software.install_path.lower():
                matches.append(software)

        return matches

    def get_software_by_publisher(self, publisher: str, fuzzy_match: bool = True) -> List[Software]:
        """
        根据发布商查找软件

        Args:
            publisher: 发布商名称
            fuzzy_match: 是否模糊匹配

        Returns:
            该发布商的软件列表
        """
        self._ensure_cache_valid()

        matches = []
        publisher_lower = publisher.lower()

        for software in self._software_cache.values():
            if fuzzy_match:
                if publisher_lower in software.publisher.lower():
                    matches.append(software)
            else:
                if software.publisher.lower() == publisher_lower:
                    matches.append(software)

        return matches

    # ==================== 缓存管理 ====================

    def refresh_cache(self, sources: List[str] = None) -> Dict[str, Any]:
        """
        刷新软件信息缓存

        Args:
            sources: 指定要刷新的数据源，None表示全部
                   可选值: ['registry', 'filesystem', 'shortcuts']

        Returns:
            扫描结果统计信息
        """
        start_time = time.time()
        scan_sources = sources or ['registry', 'filesystem', 'shortcuts']

        self._software_cache.clear()
        scan_stats = {
            'start_time': datetime.now().isoformat(),
            'sources_scanned': scan_sources,
            'registry_count': 0,
            'filesystem_count': 0,
            'shortcuts_count': 0,
            'total_count': 0,
            'errors': []
        }

        try:
            # 扫描注册表
            if 'registry' in scan_sources:
                try:
                    registry_software = self._registry_scanner.scan_uninstall_entries()
                    self._software_cache.update(registry_software)
                    scan_stats['registry_count'] = len(registry_software)
                except Exception as e:
                    scan_stats['errors'].append(f"Registry scan failed: {str(e)}")

            # 扫描文件系统
            if 'filesystem' in scan_sources:
                try:
                    filesystem_dirs = self._filesystem_scanner.scan_common_directories()
                    filesystem_count = 0
                    for name, path in filesystem_dirs.items():
                        if name not in self._software_cache:
                            self._software_cache[name] = Software(
                                name=name,
                                install_path=path,
                                source="filesystem"
                            )
                            filesystem_count += 1
                    scan_stats['filesystem_count'] = filesystem_count
                except Exception as e:
                    scan_stats['errors'].append(f"Filesystem scan failed: {str(e)}")

            # 扫描快捷方式
            if 'shortcuts' in scan_sources:
                try:
                    shortcut_dirs = self._shortcut_resolver.scan_desktop_shortcuts()
                    shortcuts_count = 0
                    for name, path in shortcut_dirs.items():
                        if name not in self._software_cache:
                            self._software_cache[name] = Software(
                                name=name,
                                install_path=path,
                                source="shortcut"
                            )
                            shortcuts_count += 1
                    scan_stats['shortcuts_count'] = shortcuts_count
                except Exception as e:
                    scan_stats['errors'].append(f"Shortcuts scan failed: {str(e)}")

            # 更新缓存状态
            self._cache_timestamp = time.time()
            self._cache_valid = True
            self._last_scan_duration = self._cache_timestamp - start_time

            # 完善统计信息
            scan_stats.update({
                'total_count': len(self._software_cache),
                'duration_seconds': self._last_scan_duration,
                'end_time': datetime.now().isoformat(),
                'success': True
            })

            # 记录扫描历史
            self._scan_history.append(scan_stats)
            if len(self._scan_history) > 10:  # 只保留最近10次记录
                self._scan_history.pop(0)

        except Exception as e:
            scan_stats.update({
                'success': False,
                'error': str(e),
                'duration_seconds': time.time() - start_time
            })
            raise

        return scan_stats

    def clear_cache(self):
        """清空缓存"""
        self._software_cache.clear()
        self._cache_valid = False
        self._cache_timestamp = 0

    def is_cache_valid(self) -> bool:
        """检查缓存是否有效"""
        if not self._cache_valid:
            return False

        if self._cache_timeout <= 0:
            return True

        return (time.time() - self._cache_timestamp) < self._cache_timeout

    def get_cache_info(self) -> Dict[str, Any]:
        """获取缓存信息"""
        return {
            'cached_software_count': len(self._software_cache),
            'cache_valid': self._cache_valid,
            'cache_age_seconds': time.time() - self._cache_timestamp if self._cache_timestamp > 0 else 0,
            'cache_timeout': self._cache_timeout,
            'last_scan_duration': self._last_scan_duration,
            'auto_refresh': self._auto_refresh
        }

    # ==================== 数据分析和统计 ====================

    def get_software_statistics(self) -> Dict[str, Any]:
        """获取软件统计信息"""
        self._ensure_cache_valid()

        if not self._software_cache:
            return {'total_count': 0}

        # 基础统计
        total_count = len(self._software_cache)
        system_count = sum(1 for s in self._software_cache.values() if s.is_system_software())
        user_count = total_count - system_count

        # 按来源统计
        source_stats = {}
        for software in self._software_cache.values():
            source = software.source
            source_stats[source] = source_stats.get(source, 0) + 1

        # 按发布商统计 (top 10)
        publisher_stats = {}
        for software in self._software_cache.values():
            publisher = software.publisher
            if publisher and publisher != "Unknown":
                publisher_stats[publisher] = publisher_stats.get(publisher, 0) + 1

        top_publishers = sorted(publisher_stats.items(), key=lambda x: x[1], reverse=True)[:10]

        # 计算总大小
        total_size_mb = 0
        software_with_size = 0
        for software in self._software_cache.values():
            if software.size_mb and software.size_mb > 0:
                total_size_mb += software.size_mb
                software_with_size += 1

        return {
            'total_count': total_count,
            'system_software_count': system_count,
            'user_software_count': user_count,
            'source_distribution': source_stats,
            'top_publishers': top_publishers,
            'total_size_mb': round(total_size_mb, 2),
            'software_with_size_info': software_with_size,
            'average_size_mb': round(total_size_mb / software_with_size, 2) if software_with_size > 0 else 0
        }

    def get_software_by_category(self) -> Dict[str, List[Software]]:
        """按类别分组软件"""
        self._ensure_cache_valid()

        categories = {
            'system': [],
            'development': [],
            'office': [],
            'multimedia': [],
            'games': [],
            'utilities': [],
            'security': [],
            'communication': [],
            'other': []
        }

        # 定义分类关键词
        category_keywords = {
            'development': ['visual studio', 'python', 'java', 'git', 'docker', 'nodejs', 'npm', 'compiler', 'ide',
                            'sdk'],
            'office': ['office', 'word', 'excel', 'powerpoint', 'adobe', 'pdf', 'reader'],
            'multimedia': ['media', 'player', 'vlc', 'spotify', 'itunes', 'photoshop', 'video', 'audio'],
            'games': ['game', 'steam', 'epic', 'uplay', 'origin', 'battle.net'],
            'utilities': ['winrar', '7-zip', 'notepad', 'utility', 'tool', 'cleaner'],
            'security': ['antivirus', 'defender', 'firewall', 'security', 'malware', 'norton', 'kaspersky'],
            'communication': ['skype', 'zoom', 'teams', 'discord', 'telegram', 'whatsapp', 'qq', '微信']
        }

        for software in self._software_cache.values():
            if software.is_system_software():
                categories['system'].append(software)
                continue

            categorized = False
            software_name_lower = software.name.lower()

            for category, keywords in category_keywords.items():
                if any(keyword in software_name_lower for keyword in keywords):
                    categories[category].append(software)
                    categorized = True
                    break

            if not categorized:
                categories['other'].append(software)

        return categories

    # ==================== 数据导出和持久化 ====================

    def export_software_list(self, file_path: str, format: str = 'json', **options) -> bool:
        """
        导出软件列表到文件

        Args:
            file_path: 导出文件路径
            format: 导出格式 ('json', 'csv', 'xlsx')
            **options: 格式特定选项

        Returns:
            导出是否成功
        """
        self._ensure_cache_valid()

        try:
            if format.lower() == 'json':
                return self._export_to_json(file_path, **options)
            elif format.lower() == 'csv':
                return self._export_to_csv(file_path, **options)
            elif format.lower() == 'xlsx':
                return self._export_to_xlsx(file_path, **options)
            else:
                raise ValueError(f"Unsupported export format: {format}")
        except Exception as e:
            raise FileSystemException(file_path, "export", str(e))

    def load_software_cache(self, file_path: str) -> bool:
        """从文件加载软件缓存"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            self._software_cache.clear()
            for name, software_data in data.items():
                self._software_cache[name] = Software.from_dict(software_data)

            self._cache_valid = True
            self._cache_timestamp = time.time()
            return True

        except Exception as e:
            raise FileSystemException(file_path, "load cache", str(e))

    def save_software_cache(self, file_path: str) -> bool:
        """保存软件缓存到文件"""
        try:
            data = {name: software.to_dict() for name, software in self._software_cache.items()}

            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            return True

        except Exception as e:
            raise FileSystemException(file_path, "save cache", str(e))

    # ==================== 高级功能 ====================

    def validate_software_paths(self, fix_invalid: bool = False) -> Dict[str, Any]:
        """
        验证软件安装路径的有效性

        Args:
            fix_invalid: 是否尝试修复无效路径

        Returns:
            验证结果统计
        """
        self._ensure_cache_valid()

        valid_count = 0
        invalid_count = 0
        fixed_count = 0
        invalid_software = []

        for name, software in self._software_cache.items():
            if software.has_valid_path():
                valid_count += 1
            else:
                invalid_count += 1
                invalid_software.append(name)

                if fix_invalid:
                    # 尝试通过可执行文件路径修复
                    try:
                        exe_files = software.get_executable_files()
                        if exe_files:
                            new_path = os.path.dirname(exe_files[0])
                            if os.path.exists(new_path):
                                software.install_path = new_path
                                fixed_count += 1
                    except:
                        pass

        return {
            'total_software': len(self._software_cache),
            'valid_paths': valid_count,
            'invalid_paths': invalid_count,
            'fixed_paths': fixed_count,
            'invalid_software_list': invalid_software
        }

    def find_duplicate_software(self) -> List[List[Software]]:
        """查找可能重复的软件"""
        self._ensure_cache_valid()

        duplicates = []
        checked = set()

        for name1, software1 in self._software_cache.items():
            if name1 in checked:
                continue

            similar_group = [software1]
            checked.add(name1)

            for name2, software2 in self._software_cache.items():
                if name2 in checked:
                    continue

                # 检查相似性
                if self._are_software_similar(software1, software2):
                    similar_group.append(software2)
                    checked.add(name2)

            if len(similar_group) > 1:
                duplicates.append(similar_group)

        return duplicates

    def get_scan_history(self) -> List[Dict]:
        """获取扫描历史记录"""
        return self._scan_history.copy()

    # ==================== 内部辅助方法 ====================

    def _ensure_cache_valid(self):
        """确保缓存有效"""
        if not self.is_cache_valid():
            if self._auto_refresh:
                self.refresh_cache()
            else:
                raise Exception("Software cache is invalid and auto-refresh is disabled")

    def _fuzzy_search(self, keyword: str, limit: int = None) -> List[Software]:
        """模糊搜索实现"""
        keyword_lower = keyword.lower()
        matches = []

        for software in self._software_cache.values():
            score = 0

            # 名称匹配
            if keyword_lower in software.name.lower():
                score += 10
                if software.name.lower().startswith(keyword_lower):
                    score += 5

            # 发布商匹配
            if keyword_lower in software.publisher.lower():
                score += 3

            # 路径匹配
            if software.install_path and keyword_lower in software.install_path.lower():
                score += 2

            if score > 0:
                matches.append((software, score))

        # 按分数排序
        matches.sort(key=lambda x: x[1], reverse=True)
        results = [match[0] for match in matches]

        return results[:limit] if limit else results

    def _apply_filters(self, software_list: List[Software], **filters) -> List[Software]:
        """应用筛选条件"""
        filtered = software_list

        if 'publisher' in filters:
            publisher_filter = filters['publisher'].lower()
            filtered = [s for s in filtered if publisher_filter in s.publisher.lower()]

        if 'source' in filters:
            source_filter = filters['source']
            filtered = [s for s in filtered if s.source == source_filter]

        if 'size_min' in filters:
            size_min = filters['size_min']
            filtered = [s for s in filtered if s.size_mb and s.size_mb >= size_min]

        if 'size_max' in filters:
            size_max = filters['size_max']
            filtered = [s for s in filtered if s.size_mb and s.size_mb <= size_max]

        if 'exclude_system' in filters and filters['exclude_system']:
            filtered = [s for s in filtered if not s.is_system_software()]

        return filtered

    def _are_software_similar(self, software1: Software, software2: Software) -> bool:
        """判断两个软件是否相似（可能重复）"""
        # 发布商相同且名称相似
        if (software1.publisher == software2.publisher and
                software1.publisher != "Unknown"):
            name1_words = set(software1.name.lower().split())
            name2_words = set(software2.name.lower().split())
            common_words = name1_words & name2_words
            if len(common_words) >= 2:  # 至少2个共同单词
                return True

        # 安装路径相似
        if (software1.install_path and software2.install_path):
            path1_parts = software1.install_path.lower().split(os.sep)
            path2_parts = software2.install_path.lower().split(os.sep)
            if len(set(path1_parts) & set(path2_parts)) >= 3:  # 路径至少3层相同
                return True

        return False

    def _export_to_json(self, file_path: str, **options) -> bool:
        """导出为JSON格式"""
        include_metadata = options.get('include_metadata', True)
        pretty_print = options.get('pretty_print', True)

        export_data = {}
        for name, software in self._software_cache.items():
            if include_metadata:
                export_data[name] = software.to_dict()
            else:
                export_data[name] = {
                    'name': software.name,
                    'install_path': software.install_path,
                    'version': software.version,
                    'publisher': software.publisher
                }

        with open(file_path, 'w', encoding='utf-8') as f:
            if pretty_print:
                json.dump(export_data, f, ensure_ascii=False, indent=2)
            else:
                json.dump(export_data, f, ensure_ascii=False)

        return True

    def _export_to_csv(self, file_path: str, **options) -> bool:
        """导出为CSV格式"""
        import csv

        columns = options.get('columns', ['name', 'version', 'publisher', 'install_path', 'source'])

        with open(file_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=columns)
            writer.writeheader()

            for software in self._software_cache.values():
                row = {}
                for col in columns:
                    row[col] = getattr(software, col, '')
                writer.writerow(row)

        return True

    def _export_to_xlsx(self, file_path: str, **options) -> bool:
        """导出为Excel格式"""
        try:
            import openpyxl
            from openpyxl.utils.dataframe import dataframe_to_rows
            import pandas as pd
        except ImportError:
            raise ImportError("openpyxl and pandas are required for Excel export")

        # 准备数据
        data = []
        for software in self._software_cache.values():
            data.append({
                'Name': software.name,
                'Version': software.version,
                'Publisher': software.publisher,
                'Install Path': software.install_path,
                'Source': software.source,
                'Size (MB)': software.size_mb or 0,
                'Install Date': software.install_date or ''
            })

        df = pd.DataFrame(data)

        with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Software List', index=False)

            # 添加统计信息
            stats = self.get_software_statistics()
            stats_df = pd.DataFrame(list(stats.items()), columns=['Metric', 'Value'])
            stats_df.to_excel(writer, sheet_name='Statistics', index=False)

        return True

    # ==================== 上下文管理器支持 ====================

    def __enter__(self):
        """上下文管理器入口"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        pass

    def __repr__(self):
        cache_info = self.get_cache_info()
        return (f"SoftwareManager(cached_software={cache_info['cached_software_count']}, "
                f"cache_valid={cache_info['cache_valid']})")
