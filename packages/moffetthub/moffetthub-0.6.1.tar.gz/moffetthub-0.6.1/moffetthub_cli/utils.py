import os
import shutil
import requests
import subprocess
import unicodedata
import signal
from pathlib import Path
from typing import Union, List, Optional
from datetime import datetime
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
from .i18n import _

BASE_URL = "https://moffett-release.tos-cn-guangzhou.volces.com/"

# 全局变量用于控制下载任务
_download_tasks = []
_is_interrupted = False

def signal_handler(signum, frame):
    """处理 Ctrl+C 信号"""
    global _is_interrupted
    if not _is_interrupted:
        _is_interrupted = True
        print("\n" + _("Interrupting all downloads..."))
        # 取消所有正在进行的下载任务
        for task in _download_tasks:
            if hasattr(task, 'cancel'):
                task.cancel()
        raise KeyboardInterrupt

# 注册信号处理器
signal.signal(signal.SIGINT, signal_handler)

def extract_with_pigz(file_path, extract_path=".", n_thread=8):
    if shutil.which("pigz"):
        cmd = f"pigz -p {n_thread} -dc {file_path} | tar -xv -C {extract_path} > /dev/null 2>&1"
        subprocess.run(cmd, shell=True, check=True)
    else:
        cmd = f"tar -xvf {file_path} -C {extract_path} > /dev/null 2>&1"
        subprocess.run(cmd, shell=True, check=True)


def select_path_by_priority(paths: List[str],
                            priority_keywords: List[str]) -> Optional[str]:
    """
    从路径列表中选择最优匹配路径。
    
    参数：
        paths: 路径字符串列表。
        priority_keywords: 优先匹配关键词，按优先级排序（高 → 低）。
        
    返回：
        匹配到的第一个路径（优先级最高），如无匹配则返回 None。
    """
    for keyword in priority_keywords:
        for path in paths:
            if keyword in path:
                return path
    return None


def get_display_width(text: str) -> int:
    """
    计算字符串的显示宽度，考虑中文字符的双倍宽度
    """
    width = 0
    for char in text:
        if unicodedata.east_asian_width(char) in {'F', 'W'}:  # 全角或宽字符
            width += 2
        else:
            width += 1
    return width


def format_column(text: str, width: int) -> str:
    """
    格式化列内容，确保对齐
    """
    display_width = get_display_width(text)
    padding = width - display_width
    return text + " " * padding


def format_size(size: int) -> str:
    """格式化文件大小为合适的单位"""
    if size >= 1024**3:  # 大于或等于 1GB
        return f"{size / (1024 ** 3):.2f} GB"
    elif size >= 1024**2:  # 大于或等于 1MB
        return f"{size / (1024 ** 2):.2f} MB"
    elif size >= 1024:  # 大于或等于 1KB
        return f"{size / 1024:.2f} KB"
    else:  # 小于 1KB
        return f"{size} B"


def format_datetime(datetime_str: Union[str, datetime]) -> str:
    """Format time to a more readable format in English"""
    try:
        if isinstance(datetime_str, str):
            dt = datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S.%fZ")
        else:
            dt = datetime_str
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except ValueError:
        return datetime_str  # If parsing fails, return the original string


def extract_first_segment(path: str, prefix_path: str) -> str:
    """
    提取路径的二级目录结构：
    - 从 prefix_path 开始向前找到第一个 '/'
    - 提取该 '/' 后的内容直到第二个 '/'
    - 如果没有第二个 '/'，返回整个剩余字符串
    """
    # 去掉开头的 '/'
    path = path.lstrip("/")
    
    # 找到 prefix_path 在 path 中的位置
    if prefix_path in path:
        # 从 prefix_path 结束位置开始
        start_pos = path.find(prefix_path) + len(prefix_path)
        remaining_path = path[start_pos:]
        
        # 分割路径
        parts = remaining_path.split('/')
        if len(parts) >= 2:
            # 返回前两级目录，不包含最后的斜杠
            return parts[0] + '/' + parts[1]
        elif len(parts) == 1:
            return parts[0]
        else:
            return remaining_path
    else:
        return path


def fetch_directory_contents(prefix_path: str = "", base_url: str = BASE_URL):
    """获取目录内容"""
    prefix_dir = "moffett-model-zoo/"
    try:
        prefix_path = prefix_dir + prefix_path
        if not prefix_path.endswith("/"):
            prefix_path = prefix_path + "/"
        if prefix_path == "" or prefix_path is None:
            file_url = base_url
        else:
            file_url = base_url + "?prefix=" + prefix_path
        response = requests.get(file_url)
        response.raise_for_status()
        data = response.json()
        contents = data.get("Contents", [])

        result = {}
        for item in contents:
            current_element = extract_first_segment(
                item["Key"], prefix_path)
            if not current_element == "":  # 判断是否为下一级内容
                if current_element in result.keys():
                    result[current_element] = [
                        result[current_element][0] + item["Size"],
                        max(
                            result[current_element][1],
                            datetime.strptime(item["LastModified"],
                                              "%Y-%m-%dT%H:%M:%S.%fZ"))
                    ]
                else:
                    result[current_element] = [
                        item["Size"],
                        datetime.strptime(item["LastModified"],
                                          "%Y-%m-%dT%H:%M:%S.%fZ")
                    ]

            if "." in result.keys():
                result["."] = [
                    result["."][0] + item["Size"],
                    max(
                        result["."][1],
                        datetime.strptime(item["LastModified"],
                                          "%Y-%m-%dT%H:%M:%S.%fZ"))
                ]
            else:
                result["."] = [
                    item["Size"],
                    datetime.strptime(item["LastModified"],
                                      "%Y-%m-%dT%H:%M:%S.%fZ")
                ]

        # 过滤掉当前目录（.）
        if "." in result:
            del result["."]

        # print(f"result: {result}")
        
        return result, contents
    except Exception as e:
        print(_("failed to get directory contents: {}").format(e))
        return {}, []


def download_single_file(url: str, output_path: str, filename: str) -> None:
    """下载单个文件的函数"""
    global _is_interrupted
    if _is_interrupted:
        return

    try:
        # print(_("downloading {} to {} ...").format(url, output_path))
        response = requests.get(url, stream=True)
        response.raise_for_status()

        # 使用 tqdm 显示下载进度
        total_size = int(response.headers.get('content-length', 0))
        with open(output_path, 'wb') as f, tqdm(
                desc=filename,
                total=total_size,
                unit='B',
                unit_scale=True,
                unit_divisor=1024,
        ) as bar:
            for data in response.iter_content(chunk_size=1024):
                if _is_interrupted:
                    raise KeyboardInterrupt
                f.write(data)
                bar.update(len(data))

        if _is_interrupted:
            return

        # print(_("file {} download completed!").format(filename))
        
        # 如果是 tar.gz 文件，解压并删除
        if filename.endswith(".tar.gz"):
            extract_with_pigz(output_path, os.path.dirname(output_path), n_thread=8)
            os.remove(output_path)
            # print(_("file deleted: {}" ).format(output_path))
            
    except Exception as e:
        if not _is_interrupted:
            print(_("error downloading {}: {}").format(url, e))
        raise


def download_model(model_path: str,
                   output_dir: str = "~/.moffetthub_cache",
                   base_url: str = BASE_URL,
                   strategy: str = "all",
                   max_workers: int = 4):

    output_dir = os.path.expanduser(output_dir)
    global _download_tasks, _is_interrupted
    _is_interrupted = False
    _download_tasks = []

    try:
        result, contents = fetch_directory_contents(model_path, base_url=base_url)
        if len(contents) >= 1:
            valid_model_paths = [
                item['Key'] for item in contents if 'Key' in item and "tar.gz" in item['Key']
            ]
            
            # 根据不同的 strategy 选择对应的文件
            if strategy == "all":
                valid_model_paths = valid_model_paths
            elif strategy == "decode":
                valid_model_paths = [path for path in valid_model_paths if path.endswith("decode.tar.gz")]
            elif strategy == "pd_auto":
                valid_model_paths = [path for path in valid_model_paths if path.endswith("pd_auto.tar.gz")]
            elif strategy == "pd_separate":
                valid_model_paths = [path for path in valid_model_paths if path.endswith("prefill.tar.gz") or path.endswith("decode.tar.gz")]
            elif strategy == "pd_separate_cpu":
                valid_model_paths = [path for path in valid_model_paths if path.endswith("prefill.tar.gz") or path.endswith("decode_cpu.tar.gz")]
            elif strategy == "speculative":
                valid_model_paths = [path for path in valid_model_paths if path.endswith("speculative.tar.gz")]
            elif strategy == "speculative_cpu":
                valid_model_paths = [path for path in valid_model_paths if path.endswith("decode_cpu.tar.gz")]
            
            if not valid_model_paths:
                raise FileNotFoundError(f"no strategy found for {model_path}: {strategy}")
        elif len(contents) == 0:
            raise FileNotFoundError(f"{model_path} is not found")

        # 准备下载任务
        download_tasks = []
        for valid_model_path in valid_model_paths:
            url = os.path.join(base_url, valid_model_path)
            filename = os.path.basename(valid_model_path)
            user_model = "/".join(Path(valid_model_path).parts[-3:-1])
            output_file_dir = os.path.join(output_dir, user_model)
            output_path = os.path.join(output_file_dir, filename)
            
            # 检查目标目录是否已存在
            if filename.endswith("decode_cpu.tar.gz"):
                target_dir = "decode_cpu.gguf"
            else:
                target_dir = os.path.splitext(os.path.splitext(filename)[0])[0]  # 去掉 .tar.gz 后缀
            target_path = os.path.join(output_file_dir, target_dir)

            if os.path.exists(target_path):
                print(_("{}: [done]").format(filename))
                continue
            
            # 确保输出目录存在
            if not os.path.exists(output_file_dir):
                os.makedirs(output_file_dir)
                
            download_tasks.append((url, output_path, filename))

        if not download_tasks:
            print(_("All files already exist, nothing to download"))
            return

        # 使用线程池并行下载
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [
                executor.submit(download_single_file, url, output_path, filename)
                for url, output_path, filename in download_tasks
            ]
            _download_tasks = futures
            
            # 等待所有下载完成
            for future in as_completed(futures):
                try:
                    future.result()
                except KeyboardInterrupt:
                    print(_("\nDownload interrupted by user"))
                    return
                except Exception as e:
                    if not _is_interrupted:
                        print(_("error in download task: {}").format(e))
                    raise

        if not _is_interrupted:
            print(_("model downloaded successfully"))
    except FileNotFoundError as e:
        print(_("error: {}" ).format(e))
    except KeyboardInterrupt:
        print(_("\nDownload interrupted by user"))
    except Exception as e:
        print(_("error downloading model: {}" ).format(e))
    finally:
        _download_tasks = []
        _is_interrupted = False


def list_model(prefix_path: str = "", base_url: str = BASE_URL):
    """列出模型信息并打印，自动调整列宽，支持中英文对齐"""
    result, contents = fetch_directory_contents(prefix_path, base_url)
    
    # 获取每个模型支持的策略
    model_strategies = {}
    for item in contents:
        if 'Key' in item and "tar.gz" in item['Key']:
            model_path = "/".join(Path(item['Key']).parts[-3:-1])
            if model_path not in model_strategies:
                model_strategies[model_path] = {
                    'files': set(),
                    'strategies': set()
                }
            
            filename = os.path.basename(item['Key'])
            model_strategies[model_path]['files'].add(filename)
    
    # 根据文件组合判断策略
    for model_path, info in model_strategies.items():
        files = info['files']
        strategies = info['strategies']
        
        # 检查各个策略所需的文件
        if "decode.tar.gz" in files:
            strategies.add("decode")
        
        if "pd_auto.tar.gz" in files:
            strategies.add("pd_auto")
        
        if "prefill.tar.gz" in files and "decode.tar.gz" in files:
            strategies.add("pd_separate")
        
        if "prefill.tar.gz" in files and "decode_cpu.tar.gz" in files:
            strategies.add("pd_separate_cpu")
        
        if "speculative.tar.gz" in files:
            strategies.add("speculative")
        
        if "decode_cpu.tar.gz" in files:
            strategies.add("speculative_cpu")
    
    # 计算每列最大宽度（用显示宽度）
    model_name_header = _('model name')
    strategy_header = _('strategy')
    size_header = _('size')
    last_modified_header = _('last modified')
    
    # 准备所有可能显示的内容
    model_names = list(result.keys()) + [model_name_header]
    sizes = [format_size(size_date[0]) for size_date in result.values()] + [size_header]
    dates = [format_datetime(size_date[1]) for size_date in result.values()] + [last_modified_header]
    
    # 收集所有策略名称
    all_strategies = [strategy_header]
    for info in model_strategies.values():
        all_strategies.extend(sorted(info['strategies']))

    def get_max_width(items):
        return max(get_display_width(str(item)) for item in items)

    # 计算每列的最大宽度
    col1_width = get_max_width(model_names)
    col2_width = get_max_width(all_strategies)  # 使用所有策略名称的最大宽度
    col3_width = get_max_width(sizes)
    col4_width = get_max_width(dates)

    # 打印表头
    print("-" * (col1_width + col2_width + col3_width + col4_width + 9))
    header = f"{format_column(model_name_header, col1_width)} | {format_column(strategy_header, col2_width)} | {format_column(size_header, col3_width)} | {format_column(last_modified_header, col4_width)}"
    print(header)
    print("-" * (col1_width + col2_width + col3_width + col4_width + 9))
    
    # 打印每个模型的信息
    for i, (file_name, size_date) in enumerate(result.items()):
        size_formatted = format_size(size_date[0])
        datetime_formatted = format_datetime(size_date[1])
        strategies_list = sorted(model_strategies[file_name]['strategies'])
        
        # 打印第一行（包含模型名称、第一个策略、大小和日期）
        if strategies_list:
            first_strategy = strategies_list[0]
            line = f"{format_column(file_name, col1_width)} | {format_column(first_strategy, col2_width)} | {format_column(size_formatted, col3_width)} | {format_column(datetime_formatted, col4_width)}"
            print(line)
            
            # 打印剩余的策略（如果有的话）
            for strategy in strategies_list[1:]:
                line = f"{format_column('', col1_width)} | {format_column(strategy, col2_width)} | {format_column('', col3_width)} | {format_column('', col4_width)}"
                print(line)
        else:
            # 如果没有策略，只打印一行
            line = f"{format_column(file_name, col1_width)} | {format_column('', col2_width)} | {format_column(size_formatted, col3_width)} | {format_column(datetime_formatted, col4_width)}"
            print(line)
        
        print("-" * (col1_width + col2_width + col3_width + col4_width + 9))

def list_cache(output_dir: str):
    """列出本地缓存的模型和策略"""
    output_dir = os.path.expanduser(output_dir)
    if not os.path.exists(output_dir):
        print(_("No cached models found"))
        return

    # 收集所有模型信息
    cache_info = {}
    try:
        for repo_name in os.listdir(output_dir):
            repo_path = os.path.join(output_dir, repo_name)
            if not os.path.isdir(repo_path):
                continue
                
            for model_name in os.listdir(repo_path):
                model_path = os.path.join(repo_path, model_name)
                if not os.path.isdir(model_path):
                    continue
                    
                strategies = set()
                # 检查各个策略的目录
                if os.path.exists(os.path.join(model_path, "decode")):
                    strategies.add("decode")
                if os.path.exists(os.path.join(model_path, "pd_auto")):
                    strategies.add("pd_auto")
                if os.path.exists(os.path.join(model_path, "prefill")) and os.path.exists(os.path.join(model_path, "decode")):
                    strategies.add("pd_separate")
                if os.path.exists(os.path.join(model_path, "prefill")) and os.path.exists(os.path.join(model_path, "decode_cpu.gguf")):
                    strategies.add("pd_separate_cpu")
                if os.path.exists(os.path.join(model_path, "speculative")):
                    strategies.add("speculative")
                if os.path.exists(os.path.join(model_path, "decode_cpu.gguf")):
                    strategies.add("speculative_cpu")
                    
                if strategies:
                    cache_info[f"{repo_name}/{model_name}"] = strategies

        if not cache_info:
            print(_("no cached models found"))
            return

        # 计算列宽
        model_name_header = _('local model')
        strategy_header = _('strategy')
        
        model_names = list(cache_info.keys()) + [model_name_header]
        all_strategies = [strategy_header]
        for strategies in cache_info.values():
            all_strategies.extend(sorted(strategies))

        def get_max_width(items):
            return max(get_display_width(str(item)) for item in items)

        col1_width = get_max_width(model_names)
        col2_width = get_max_width(all_strategies)

        # 打印表头
        print("-" * (col1_width + col2_width + 5))
        header = f"{format_column(model_name_header, col1_width)} | {format_column(strategy_header, col2_width)}"
        print(header)
        print("-" * (col1_width + col2_width + 5))

        # 打印每个模型的信息
        for model_name, strategies in sorted(cache_info.items()):
            strategies_list = sorted(strategies)
            if strategies_list:
                first_strategy = strategies_list[0]
                line = f"{format_column(model_name, col1_width)} | {format_column(first_strategy, col2_width)}"
                print(line)
                
                for strategy in strategies_list[1:]:
                    line = f"{format_column('', col1_width)} | {format_column(strategy, col2_width)}"
                    print(line)
            print("-" * (col1_width + col2_width + 5))
    except Exception as e:
        print(_("error listing cache: {}").format(e))

def remove_cache(model_path: str, output_dir: str, strategy: str = "all"):
    """删除本地缓存的模型"""
    model_dir = os.path.join(output_dir, model_path)
    if not os.path.exists(model_dir):
        print(_("error: model {} not found in cache").format(model_path))
        return

    if strategy == "all":
        # 删除整个模型目录
        shutil.rmtree(model_dir)
        print(_("removed all cached files for model {}").format(model_path))
    else:
        # 根据策略删除特定目录或文件
        strategy_dirs = {
            "decode": ["decode"],
            "pd_auto": ["pd_auto"],
            "pd_separate": ["prefill", "decode"],
            "pd_separate_cpu": ["prefill", "decode_cpu.gguf"],
            "speculative": ["speculative"],
            "speculative_cpu": ["decode_cpu.gguf"]
        }
        
        if strategy not in strategy_dirs:
            print(_("error: invalid strategy: {}").format(strategy))
            return
            
        removed = False
        for path_name in strategy_dirs[strategy]:
            path = os.path.join(model_dir, path_name)
            if os.path.exists(path):
                if os.path.isdir(path):
                    shutil.rmtree(path)
                else:
                    os.remove(path)
                removed = True
                
        if removed:
            print(_("removed {} strategy files for model {}").format(strategy, model_path))
        else:
            print(_("error: no {} strategy files found for model {}").format(strategy, model_path))
            
        # 如果模型目录为空，删除整个目录
        if not os.listdir(model_dir):
            shutil.rmtree(model_dir)
            # print(_("removed empty model directory {}").format(model_path))
