import os
from pathlib import Path
from j2.config import get_config
from j2.constant import RESOURCE_PATH_FILTER
from share.utils import load_md_template_data
from .markdown_file_system_loader import MarkdownFileSystemLoader
from jinja2 import (
    Environment
)


class MarkdownEnvironment(Environment):
    def __init__(self, src_file_path: Path, dst_file_path: Path):
        self.src_file_path = src_file_path
        self.dst_file_path = dst_file_path

        config = get_config()

        # 设置模板的搜索路径
        # 默认搜索当前目录和源文件所在目录；
        search_path = [str(src_file_path.parent)]

        # 额外目录由环境变量配置指定
        add_path = config['template_search_path']
        if add_path:
            search_path.extend([os.path.expanduser(p)
                                for p in add_path.split(':')])
        search_path.extend(['.'])

        self.__md_loader = MarkdownFileSystemLoader(search_path)
        super().__init__(loader=self.__md_loader,
                         block_start_string=config['block_start_string'],
                         block_end_string=config['block_end_string'],
                         variable_start_string=config['var_start_string'],
                         variable_end_string=config['var_end_string'],
                         comment_start_string=config['comment_start_string'],
                         comment_end_string=config['comment_end_string'],
                         autoescape=True)

    def render(self):
        # 注册自定义file system loader
        self.globals['loader'] = self.__md_loader
        # 注册处理资源路径的过滤器
        self.filters[RESOURCE_PATH_FILTER] = rel_path

        # 加载模板数据
        data_file_path, data = load_md_template_data(self.src_file_path)

        # NOTE: 对markdown的处理在MarkdownFileSystemLoader的get_source函数中，不要在这里处理
        content = self.get_template(str(self.src_file_path)).render(data)

        # 写入输出文件
        self.dst_file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.dst_file_path, "w", encoding='utf-8') as file:
            file.write(content)

        print("Render done.")
        print(f"    src: {self.src_file_path}")
        print(f"    dst: {self.dst_file_path}")

    def join_path(self, template, parent):
        """Override join_path() to enable relative template paths."""
        # 就是把template路径上的../相对路径，全部从template的路径上删除掉
        while (True):
            if template.startswith("../"):
                template = template[3:]
                parent = '/'.join(parent.split('/')[:-1])  # parent也相应的减一个目录
            else:
                break
        if template.startswith('/'):
            # 直接去掉/即可，因为模板引擎已经设置搜索目录为input_dir
            included_file_path = template[1:]
        else:
            included_file_path = f"{os.path.dirname(parent)}/{template}"

        if included_file_path.startswith('/'):
            included_file_path = included_file_path[1:]

        return included_file_path


def rel_path(resource_path, loader: "MarkdownFileSystemLoader"):
    """自定义过滤器，仅用于资源的相对路径，将相对路径转变为资源相对于入口文件的相对路径
    NOTE: 策略就是将所有资源的引用路径都修改为相对于入口文件的路径"""
    if loader.entry_file_path is None:
        raise ValueError("entry_file_path is None")
    if loader.current_file_path is None:
        raise ValueError("current_file_path is None")

    if resource_path.startswith("/"):
        # 绝对路径处理：把/替换为相对于入口文件的路径
        rel_resource_path = __get_rel_path(
            loader.entry_file_path) / resource_path[1:]
        return rel_resource_path
    else:
        # 相对路径：
        if loader.current_file_path == loader.entry_file_path:
            # 如果当前文件就是入口文件，则直接返回相对路径
            return resource_path
        else:
            # 如果不是入口文件，则把相对路径转变为相对于入口文件的路径
            res_file_path = loader.current_file_path.parent / \
                Path(resource_path)
            entry_file_path = loader.entry_file_path
            rel_res_file_path = Path(os.path.relpath(
                res_file_path, entry_file_path.parent))
            return rel_res_file_path.as_posix()


def __get_rel_path(file_path: "Path") -> Path:
    """Path对象对为入参，例如：Path('foo/bar/index.md')
    从它的目录结构foo/bar中返回一个相对路径：../.."""
    # 获取当前路径的父目录
    parent_dir = file_path.parent

    # 获取当前目录的层级
    levels = len(parent_dir.parts)

    # 构建相对根目录的路径
    relative_path = Path(*(['..'] * levels))
    return relative_path
