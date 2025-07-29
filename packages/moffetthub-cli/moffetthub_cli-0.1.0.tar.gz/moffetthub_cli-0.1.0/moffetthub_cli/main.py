import os
import argparse
from moffetthub_cli import fetch_directory_contents, download_model  # 确保工具函数在 utils.py 中

def main():
    parser = argparse.ArgumentParser(
        description="moffetthub-cli: 一个用于查询目录文件和批量下载文件的命令行工具")
    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # 查询目录文件命令
    list_parser = subparsers.add_parser("list", help="列出目录内容")
    list_parser.add_argument("path", type=str, help="要查询的目录路径")

    # 批量下载文件命令
    download_parser = subparsers.add_parser("download", help="批量下载文件")
    download_parser.add_argument("--file_paths",
                                 type=str,
                                 nargs="+", 
                                 required=True,
                                 help="要下载的文件路径列表")
    download_parser.add_argument("--serving_mode",
                                 type=str,
                                 default="",
                                 help="不同推理模式下载对应模型结构，可选(pd_auto 或 decode_cpu),默认为空，下载全部")
    download_parser.add_argument("--output-dir",
                                 type=str,
                                 default="./downloads",
                                 help="下载文件保存的目录")
    

    args = parser.parse_args()

    if args.command == "list":
        fetch_directory_contents(file_path=args.path)
    elif args.command == "download":
        for file_path in args.file_paths:
            download_model(file_path, args.output_dir)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()