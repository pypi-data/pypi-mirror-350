#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
j2-cli
==========

j2 ~/data/foo/bar/index.md ~/output/foo/bar/index_quarto_arxiv_pdf.md

args:
    ~/data/foo/bar/index.md: 输入的jinja2入口模板文件路径
    ~/output/foo/bar/index_quarto_arxiv_pdf.md: 输出文件路径

This command will use `~/data/foo/bar/index.md` as j2 template,
and render to `~/output/foo/bar/index_quarto_arxiv_pdf.md` as j2 output.

using the following data files in order:
    ~/data/foo/bar/index.yaml

using the following environment variables in order:
    .j2.env
    ~/data/foo/bar/index.j2.env
    
If the sourcee template file use `include` directive,
all the data associated with the included files will also be used recursively.
"""

import os
from pathlib import Path
import sys
import argparse
from .markdown_environment import MarkdownEnvironment
from dotenv import load_dotenv


def main():
    parser = argparse.ArgumentParser(
        description='Render Jinja2 template file.',
        formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('source', type=str,
                        help='source jinja2 template file path as input')
    parser.add_argument('dest', type=str,
                        help='dest file path as output')
    args = parser.parse_args()

    src_file_path = Path(os.path.expanduser(args.source))
    dst_file_path = Path(os.path.expanduser(args.dest))

    if not src_file_path.is_file():
        print(f"Error: {src_file_path} is not a file.")
        sys.exit(1)
        return

    # 加载环境变量
    if Path('.j2.env').is_file():
        load_dotenv('.j2.env')
    if src_file_path.parent.joinpath('.j2.env').is_file():
        load_dotenv(src_file_path.parent.joinpath('.j2.env'))

    env = MarkdownEnvironment(src_file_path, dst_file_path)
    env.render()
    sys.exit(0)


if __name__ == "__main__":
    main()
