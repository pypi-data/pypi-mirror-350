import os
from ninja_syntax import Writer
from pathlib import Path
from typing import List, Dict, Optional

import yaml

from share.utils import load_md_template_data

RESOURCE_PHONY_TARGET = "phony_resources"


class NinjaBuildGenerator:
    def __init__(self, input_dir_path: Path, output_dir_path: Path) -> None:
        self.input_dir_path = input_dir_path
        self.output_dir_path = output_dir_path
        print(f"Input dir: {self.input_dir_path}")
        print(f"Output dir: {self.output_dir_path}")

    def make_build_ninja(self):
        # 规则生成build.ninja
        with open("build.ninja", "w", encoding='utf-8') as buildfile:
            n = Writer(buildfile)
            # 先为全部静态资源生成targets
            resource_phony_target = self.__make_build_targets_for_resource(n)
            # 为所有的模板文件生成targets，隐式的依赖于上面的静态资源targets
            self.__make_build_targets_for_entry_files(n, resource_phony_target)

    def __make_build_targets_for_resource(self, ninja_writer: "Writer"):
        rules = {
            "copy": "cp -f $in $out",
            "drawio": "draw.io.exe --export --scale 1.0 --output $out $in",
            "plantuml": "plantuml-wrap $in $out",
        }
        for key, value in rules.items():
            ninja_writer.rule(key, command=value)

        dst_files = []
        for src_file in self._find_all_resource_files():
            src_file_path = self.input_dir_path / src_file
            dependencies = [src_file_path.as_posix()]

            if src_file.suffix == '.drawio':
                target_file = self.output_dir_path / src_file.with_suffix('')
                if target_file.suffix == '.png':
                    # 仅当文件名满足index.png.drawio时才生成png文件
                    ninja_writer.build(target_file.as_posix(),
                                       "drawio", dependencies)
                else:
                    continue
            elif src_file.suffix == '.puml':
                target_file = self.output_dir_path / src_file.with_suffix('')
                if target_file.suffix == '.png':
                    # 仅当文件名满足index.png.puml时才生成png文件
                    ninja_writer.build(target_file.as_posix(),
                                       "plantuml", dependencies)
                else:
                    continue
            else:
                target_file = self.output_dir_path / src_file
                ninja_writer.build(target_file.as_posix(),
                                   "copy", dependencies)
            dst_files.append(target_file.as_posix())

        if len(dst_files) > 0:
            ninja_writer.build(RESOURCE_PHONY_TARGET, "phony", dst_files)
            return RESOURCE_PHONY_TARGET
        else:
            return None

    def _find_all_resource_files(self) -> List[Path]:
        """在input_dir中入口文件.md以外的文件都被认为是资源文件"""
        files = []
        for dirpath, dirnames, filenames in os.walk(self.input_dir_path):
            dir = Path(dirpath).relative_to(Path(self.input_dir_path))
            # print(dirpath, dirnames, filenames, dir)
            for filename in filenames:
                full_file_path = dir / filename
                file_last_extension = full_file_path.suffix[1:]
                # file_extension = ''.join(full_file_path.suffixes)

                if file_last_extension in ['md']:
                    continue

                files.append(full_file_path)
        return files

    def __make_build_targets_for_entry_files(self, ninja_writer: "Writer",
                                             resource_phony_target):
        """Entry file's front matter:
        ---
        output:
            - template: quarto/arxiv
              ext: pdf
              foo1: bar1
              foo2: bar2
              ...
            - template: hugo/codelabs
              ext: qmd
              foo1: bar1
              ...
        ---
        """
        RULE_J2 = "j2"
        RULE_MD_RENDER = "md_render"
        rules = {
            RULE_J2: "j2 $in $out",
            RULE_MD_RENDER: "md-render $args $in $out"
        }
        for key, value in rules.items():
            ninja_writer.rule(key, command=value)

        for src_file_path, outputs in self._find_all_entry_files().items():
            full_src_file_path = self.input_dir_path / src_file_path

            # 用j2_cli生成入口模板文件.
            full_dst_j2_path = self.output_dir_path / src_file_path
            dependencies = [full_src_file_path.as_posix()]
            ninja_writer.build(
                full_dst_j2_path.as_posix(), RULE_J2, dependencies)

            # 根据上面生成的入口文件的output信息输出目标文件
            for idx, output in enumerate(outputs):
                template = output['template']
                ext = output['ext']

                # NOTE: 在这里增加对全部静态资源目标文件的依赖(implicit dependency)
                dst_output_path = src_file_path.with_suffix(
                    f'.{template.replace('/', '_')}.{ext}'
                )
                full_dst_output_path = self.output_dir_path / dst_output_path
                dependencies = [full_dst_j2_path.as_posix()]
                if resource_phony_target:
                    ninja_writer.build(full_dst_output_path.as_posix(
                    ), RULE_MD_RENDER, inputs=dependencies,
                        variables={"args": f'--template-index {idx}'},
                        implicit=[resource_phony_target])
                else:
                    ninja_writer.build(full_dst_output_path.as_posix(
                    ), RULE_MD_RENDER, inputs=dependencies,
                        variables={"args": f'--template-index {idx}'})

    def _find_all_entry_files(self) -> Dict[Path, List[Dict[str, str]]]:
        """在input_dir中找所有的模板入口文件template_entry_file。
        返回值：{入口文件路径: 入口文件的Output信息列表}
        """
        entry_files = {}
        for dirpath, dirnames, filenames in os.walk(self.input_dir_path,
                                                    followlinks=True):
            dir = Path(dirpath).relative_to(Path(self.input_dir_path))
            for filename in filenames:
                full_file_path = dir / filename

                file_extension = ''.join(full_file_path.suffixes)
                if file_extension not in ['.md']:
                    continue
                entry_file_fullpath = self.input_dir_path / full_file_path
                data_file_path, metadata = load_md_template_data(
                    entry_file_fullpath)
                if not data_file_path:
                    continue
                print(f"Found entry file: {full_file_path}")
                entry_files[full_file_path] = []
                if (metadata
                    and "outputs" in metadata
                        and len(metadata["outputs"]) > 0):
                    outputs = metadata["outputs"]
                    print(f"Found template outputs. {outputs}")
                    entry_files[full_file_path] = outputs
        return entry_files

    def _get_entry_file_metadata(self, full_file_path: "Path"):
        """入口文件要同时满足以下条件：
        - 后缀名为.md
        - 相同目录下存在同名的.yaml文件
        - yaml文件中存在非空的output数组"""
