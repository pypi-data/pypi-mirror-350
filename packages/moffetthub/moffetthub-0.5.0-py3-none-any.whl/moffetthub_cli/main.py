import os
import argparse
from moffetthub_cli import download_model, list_model, list_cache, remove_cache  # 确保工具函数在 utils.py 中
from .i18n import _

VERSION = "0.5.0"

def main():
    parser = argparse.ArgumentParser(
        description=_("moffetthub-cli: a commnad tool to download models from the moffett model zoo"))
    parser.add_argument('-v', '--version', action='version', version=f'moffetthub-cli {VERSION}')
    subparsers = parser.add_subparsers(dest="command", help=_("available commands"))

    # 查询目录文件命令
    list_parser = subparsers.add_parser("list", help=_("list the supported model"))
    # list_parser.add_argument("path", type=str, nargs="?", default="", help=_("directory path to query"))

    # 下载模型命令
    download_parser = subparsers.add_parser("download", help=_("download model (saved in ~/.moffetthub_cache)"))
    download_parser.add_argument("model",
                                 type=str,
                                 nargs="+", 
                                 help=_("model to download (repo-name/model-name)"))
    download_parser.add_argument("--strategy",
                                 type=str,
                                 choices=["all", "decode", "pd_auto", "pd_separate", "pd_separate_cpu", "speculative", "speculative_cpu"],
                                 default="all",
                                 help=_("model running strategy (default: all)"))
    # download_parser.add_argument("--output-dir",
    #                              type=str,
    #                              default="~/.moffetthub_cache",
    #                              help=_("directory where to save the downloaded files"))
    
    # 列出本地缓存命令
    list_cache_parser = subparsers.add_parser("list-cache", help=_("list locally cached models"))
    
    # 删除本地缓存命令
    remove_cache_parser = subparsers.add_parser("remove-cache", help=_("remove locally cached models"))
    remove_cache_parser.add_argument("model",
                                    type=str,
                                    nargs="+",
                                    help=_("model to remove (repo-name/model-name)"))
    remove_cache_parser.add_argument("--strategy",
                                    type=str,
                                    choices=["all", "decode", "pd_auto", "pd_separate", "pd_separate_cpu", "speculative", "speculative_cpu"],
                                    default="all",
                                    help=_("strategy to remove (default: all)"))

    args = parser.parse_args()

    # 固定使用 ~/.moffetthub_cache
    cache_dir = os.path.expanduser("~/.moffetthub_cache")

    if args.command == "list":
        list_model()
    elif args.command == "download":
        for file_path in args.model:
            print(_("downloading model..."))
            download_model(file_path, cache_dir, strategy=args.strategy)
    elif args.command == "list-cache":
        list_cache(cache_dir)
    elif args.command == "remove-cache":
        for model in args.model:
            remove_cache(model, cache_dir, strategy=args.strategy)
    else:   
        parser.print_help()


if __name__ == "__main__":
    main()