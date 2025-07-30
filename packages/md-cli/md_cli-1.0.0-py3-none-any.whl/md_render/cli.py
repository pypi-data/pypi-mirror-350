#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from pathlib import Path
import sys
import argparse

from share.utils import load_md_template_data
from .work_dir_context import WorkDirContext
from dotenv import load_dotenv


def main():
    parser = argparse.ArgumentParser(
        description='Render md file with template.',
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('source', type=str,
                        help='source markdown file path as input')
    parser.add_argument('dest', type=str,
                        help='destination file path as output')
    parser.add_argument('--template-index', type=int,
                        help='index of template in the template list')
    args = parser.parse_args()

    load_dotenv()

    if not args.source or not args.dest:
        print(f"arguments are not complete. {args}")
        sys.exit(1)

    src_file_path = Path(args.source)
    dst_file_path = Path(args.dest)

    if not src_file_path.is_file():
        print(f"Error: {src_file_path} is not a file.")
        sys.exit(1)
        return

    data_file_paht, data = load_md_template_data(src_file_path)
    if not data:
        print(f"Error: {src_file_path} does not have data file.")
        sys.exit(1)
        return
    if "outputs" not in data or len(data["outputs"])-1 < args.template_index:
        print(
            f"Error: {data} has no output of index {args.template_index}.")
        sys.exit(1)
        return

    output_config = data["outputs"][args.template_index]

    output_template_dir_path = Path(
        os.path.expanduser(
            os.getenv("template_dir", default="~/repo/md-render-template"))
    ) / output_config["template"]
    if not output_template_dir_path.is_dir():
        print(f"Error: {output_template_dir_path} is not a directory.")
        sys.exit(1)
        return

    context = WorkDirContext(src_file_path, dst_file_path,
                             output_template_dir_path, output_config)
    context.render()
    sys.exit(0)


if __name__ == "__main__":
    main()
