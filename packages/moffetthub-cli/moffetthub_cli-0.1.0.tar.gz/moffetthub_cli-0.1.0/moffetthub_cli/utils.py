import os
import shutil
import requests
import subprocess
import unicodedata
from pathlib import Path
from typing import Union, List, Optional
from datetime import datetime
from tqdm import tqdm

BASE_URL = "https://moffett-release.tos-cn-guangzhou.volces.com/"


def extract_with_pigz(file_path, extract_path=".", n_thread=8):
    if shutil.which("pigz"):
        cmd = f"pigz -p {n_thread} -dc {file_path} | tar -xv -C {extract_path}"
        subprocess.run(cmd, shell=True, check=True)
        print(f"使用 pigz 快速解压完成：{file_path}")
    else:
        print("未找到 pigz 命令，使用 tar 解压")
        cmd = f"tar -xvf {file_path} -C {extract_path}"
        subprocess.run(cmd, shell=True, check=True)
        print(f"使用 tar 解压完成：{file_path}")


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
    """格式化时间为更可读的格式"""
    try:
        if isinstance(datetime_str, str):
            dt = datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S.%fZ")
        else:
            dt = datetime_str
        return dt.strftime("%Y年%m月%d日 %H:%M:%S")
    except ValueError:
        return datetime_str  # 如果解析失败，返回原始字符串


def extract_first_segment(path: str) -> str:
    """
    提取路径的第一个段内容：
    - 如果路径以 '/' 开头，去掉开头的 '/'。
    - 提取第一个 '/' 前的内容。
    - 如果没有 '/'，返回整个字符串。
    """
    # 去掉开头的 '/'
    path = path.lstrip("/")

    # 提取第一个 '/' 前的内容
    if "/" in path:
        return path.split("/", 1)[0] + "/"
    else:
        return path  # 如果没有 '/'，返回整个字符串


def fetch_directory_contents(file_path: str = "", base_url: str = BASE_URL):
    """获取目录内容"""
    print(f"{file_path}的目录")
    prefix_dir = "moffett-model-zoo"
    try:
        file_path = file_path.lstrip("/")
        if not file_path.startswith(prefix_dir):
            file_path = prefix_dir + "/" + file_path
        if file_path == "" or file_path is None:
            file_url = base_url
        else:
            file_url = base_url + "?prefix=" + file_path
        response = requests.get(file_url)
        response.raise_for_status()
        data = response.json()
        contents = data.get("Contents", [])

        print(f"{'文件名':<60} | {'大小':<15} | {'最后修改时间':<25}")
        print("-" * 105)  # 分隔线

        result = {}
        for item in contents:
            current_element = extract_first_segment(
                item["Key"][len(file_path):])
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

        # 定义列宽
        col1_width = 60  # 文件名列宽
        col2_width = 15  # 大小列宽
        col3_width = 25  # 时间列宽
        for file_name, size_date in result.items():
            size_formatted = format_size(size_date[0])
            datetime_formatted = format_datetime(size_date[1])
            print(
                f"{format_column(file_name, col1_width)} | {format_column(size_formatted, col2_width)} | {format_column(datetime_formatted, col3_width)}"
            )
        return contents
    except Exception as e:
        print(f"获取目录内容失败: {e}")
        return []


def download_file(file_path: str,
                  output_dir: str = ".",
                  base_url: str = BASE_URL):
    """批量下载文件到指定目录"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    try:
        url = os.path.join(base_url, file_path)
        filename = os.path.basename(file_path)
        output_path = os.path.join(output_dir, filename)

        print(f"正在下载 {url} 到 {output_path}...")
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
                f.write(data)
                bar.update(len(data))

        print(f"文件 {filename} 下载完成！")
    except Exception as e:
        print(f"下载 {url} 时出错: {e}")


def download_model(model_path: str,
                   output_dir: str = "./moffetthub",
                   base_url: str = BASE_URL,
                   serving_mode: str = ""):

    prefix_dir = "moffett-model-zoo"
    if model_path.startswith(prefix_dir) or model_path.startswith(
            f"/{prefix_dir}"):
        fixed_model_path = model_path
    else:
        fixed_model_path = "/" + prefix_dir + "/" + model_path.lstrip("/")
    try:
        contents = fetch_directory_contents(fixed_model_path,
                                            base_url=base_url)

        if len(contents) >= 1:
            valid_model_paths = [
                item['Key'] for item in contents if "tar.gz" in item['Key']
            ]
            priority = ["pd_auto", "decode"]
            if serving_mode in ["pd_auto", "decode_cpu"]:
                valid_model_path = select_path_by_priority(
                    valid_model_paths, [serving_mode])
                valid_model_paths = [valid_model_path]
        elif len(contents) == 0:
            raise FileNotFoundError(f"{model_path} is not found")

        for valid_model_path in valid_model_paths:
            print(f"valid_model_path: {valid_model_path}")
            url = os.path.join(base_url, valid_model_path)
            filename = os.path.basename(valid_model_path)
            user_model = "/".join(Path(valid_model_path).parts[-3:-1])
            output_file_dir = os.path.join(output_dir, user_model)
            output_path = os.path.join(output_file_dir, filename)
            """批量下载文件到指定目录"""
            if not os.path.exists(output_file_dir):
                os.makedirs(output_file_dir)

            print(f"正在下载 {url} 到 {output_path} ...")
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
                    f.write(data)
                    bar.update(len(data))

            print(f"文件 {filename} 下载完成！")
            if filename.endswith(".tar.gz"):
                extract_with_pigz(output_path, output_file_dir, n_thread=8)
                os.remove(output_path)
                print(f"已删除文件: {output_path}")

    except FileNotFoundError as e:
        print(f"❌ 错误: {e}")
    except Exception as e:
        print(f"下载 {url} 时出错: {e}")
