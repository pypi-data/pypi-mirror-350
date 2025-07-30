
from pathlib import Path

import yaml


def load_md_template_data(md_file_path: Path) -> tuple:
    """加载所有模板的数据，使用md_file_path相同路径下的同名.yaml文件做为数据源"""
    data_file_path = md_file_path.parent / \
        f"{md_file_path.stem}.yaml"
    if not data_file_path.is_file():
        return None, None
    with open(data_file_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
        if data:
            return data_file_path, data
        else:
            return data_file_path, {}
