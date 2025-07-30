import posixpath
import os
from jinja2 import (
    Environment,
    FileSystemLoader
)
from jinja2.loaders import split_template_path
from jinja2.exceptions import TemplateNotFound
import typing as t
from pathlib import Path
import re
from j2.config import get_config
from j2.constant import RESOURCE_PATH_FILTER


class MarkdownFileSystemLoader(FileSystemLoader):
    def __init__(self, *args, **kwargs):
        self.entry_file_path = None
        self.current_file_path = None
        super().__init__(*args, **kwargs)

    def process_content(self, filename):
        # 更新引用的资源路径：这里只处理@开头的绝对路径
        # NOTE：文件与静态图片之间的依赖关系由ninja_cli加入到build.ninja中，不在这处理
        # 参考:make_ninja_build phony_static_res
        with open(filename, encoding=self.encoding) as f:
            # 保存当前处理的文件路径，去除掉searchpath前缀，即去除input_dir前缀
            self.current_file_path = Path(
                filename).relative_to(Path(self.searchpath[0]))
            # 保存入口文件路径
            # NOTE: 首个打开的文件就是入口文件
            if self.entry_file_path is None:
                self.entry_file_path = self.current_file_path

            content = f.read()
            return add_filter_to_md_resource_paths(content)

    def get_source(
        self, environment: "Environment", template: str
    ) -> t.Tuple[str, str, t.Callable[[], bool]]:
        pieces = split_template_path(template)

        for searchpath in self.searchpath:
            # Use posixpath even on Windows to avoid "drive:" or UNC
            # segments breaking out of the search directory.
            filename = posixpath.join(searchpath, *pieces)

            if os.path.isfile(filename):
                break
        else:
            plural = "path" if len(self.searchpath) == 1 else "paths"
            paths_str = ", ".join(repr(p) for p in self.searchpath)
            raise TemplateNotFound(
                template,
                f"{template!r} not found in search {plural}: {paths_str}",
            )

        contents = self.process_content(filename)

        mtime = os.path.getmtime(filename)

        def uptodate() -> bool:
            try:
                return os.path.getmtime(filename) == mtime
            except OSError:
                return False

        # Use normpath to convert Windows altsep to sep.
        return contents, os.path.normpath(filename), uptodate


def add_filter_to_md_resource_paths(markdown_text: str) -> str:
    markdown_text = __add_filter_to_md_res_link_paths(markdown_text)
    return markdown_text


def __add_filter_to_md_res_link_paths(markdown_text: str) -> str:
    """markdown的静态资源链接引用：
    [A sunflower](./sample.png)
    改写为：
    [A sunflower]({{ "./sample.png" | rel_path(loader) }})
    """
    config = get_config()
    # 定义正则表达式，用于匹配Markdown中的链接(包含图片链接)
    pattern = r'\[([^\]]*)\]\(([^)]+)\)'

    # 用于替换的回调函数
    def replace_match(match):
        alt_text = match.group(1)  # 图片的替代文本
        img_path = match.group(2)  # 图片的路径

        # 为所有的资源路径都增加过滤器，过滤器会进行路径处理
        return (f"[{alt_text}]({config['var_start_string']} "
                f"'{img_path}' | {RESOURCE_PATH_FILTER}(loader)"
                f" {config['var_end_string']})")

    # 使用正则替换
    new_md = re.sub(pattern, replace_match, markdown_text)
    # print(f"{markdown_text} ==> {new_md}")
    return new_md
