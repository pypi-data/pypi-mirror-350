#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from pathlib import Path
import sys
import argparse
from make_ninja_build.ninja_build_generator import NinjaBuildGenerator


def main():
    parser = argparse.ArgumentParser(
        description='Make ninja build file.',
        formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('--input', type=str,
                        default='data',
                        help='input direcotry path as input')
    parser.add_argument('--output', type=str,
                        default='output',
                        help='dest file path as output')
    args = parser.parse_args()

    input_dir_path = Path(args.input)
    output_dir_path = Path(args.output)

    if not input_dir_path.is_dir():
        print(f"Error: {input_dir_path} is not a directory.")
        sys.exit(1)
        return

    generator = NinjaBuildGenerator(input_dir_path, output_dir_path)
    generator.make_build_ninja()


if __name__ == "__main__":
    main()
