import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Dict


class WorkDirContext:
    def __init__(self, src_file_path: Path, dst_file_path: Path,
                 output_template_dir_path: Path, output_config: dict) -> None:
        self.src_file_path = src_file_path
        self.dst_file_path = dst_file_path
        self.output_config = output_config
        self.output_template_dir_path = output_template_dir_path

        print(f"src_file_path: {src_file_path}")
        print(f"dst_file_path: {dst_file_path}")
        print(f"output_template_dir_path: {output_template_dir_path}")
        print(f"output_config: {output_config}")

    def render(self):
        _oldCWD = os.getcwd()
        delete_tmp_dir = strtobool(os.getenv('delete_tmp_dir', default='true'))
        with tempfile.TemporaryDirectory(delete=delete_tmp_dir) as tempdir:
            print(f"md render temp dir: {tempdir}")
            self.__work_dir_path = Path(tempdir)
            self.__work_dir_abs_path = Path(os.path.abspath(tempdir))
            self.__copy_source()
            os.chdir(self.__work_dir_path)
            try:
                self.__preprocess_source()
                # run template render
                # NOTE：这里的输出文件是在tempdir之外的，需要返回到_oldCWD中
                abs_dst_file_path = Path(_oldCWD) / self.dst_file_path
                cmd = ("python render.py "
                       f"{self.src_file_path} {abs_dst_file_path}")
                return run_cmd(cmd, self.output_config)
            except Exception as e:
                print(f"Render error: {e}")
                return 1
            finally:
                os.chdir(_oldCWD)

    def __copy_source(self):
        # NOTE：运行在workdir临时目录之外!!
        # 首先，把md-render-template目录中对应的template先复制过去
        copy_dir(self.output_template_dir_path, self.__work_dir_path)

        # 然后，简单地把src_file_path的顶层目录复制过去(通常就是output目录)，保持目录结构不变
        source_root_dir = self.src_file_path.parts[0]
        copy_dir(source_root_dir, self.__work_dir_path / source_root_dir)

    def __preprocess_source(self):
        # NOTE：运行在tempdir之内
        # 替换work_dir中所有文件中的$WORK_DIR为当前目录（并转化为windows目录结构）
        replace_in_files(
            ".", r"$PWD", self.__work_dir_abs_path.absolute().as_posix())

    def tree(self):
        os.system(f"tree {self.__work_dir_path}")


def strtobool(val):
    """Convert a string representation of truth to true (1) or false (0).
    True values are 'y', 'yes', 't', 'true', 'on', and '1'; false values
    are 'n', 'no', 'f', 'false', 'off', and '0'.  Raises ValueError if
    'val' is anything else.
    """
    val = val.lower()
    if val in ('y', 'yes', 't', 'true', 'on', '1'):
        return True
    elif val in ('n', 'no', 'f', 'false', 'off', '0'):
        return False
    else:
        raise ValueError("invalid truth value %r" % (val,))


def copy_dir(src, dst):
    print(f"copy dir from {src} to {dst}")
    shutil.copytree(src, dst, dirs_exist_ok=True)


def replace_in_files(directory, old_string, new_string):
    """替换目录下所有文件中的指定字符串
    遍历目录及子目录中的所有文件"""
    for root, dirs, files in os.walk(directory, followlinks=True):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            if not file_path.endswith('.tex'):
                continue
            try:
                # 打开文件并进行替换
                with open(file_path, 'r', encoding='utf-8') as file:
                    file_content = file.read()
                # 替换字符串
                if old_string in file_content:
                    file_content = file_content.replace(old_string, new_string)

                    # 保存修改后的内容回文件
                    with open(file_path, 'w', encoding='utf-8') as file:
                        file.write(file_content)
                    # print(f"# Replaced in: {file_path}")
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
                pass


def run_cmd(cmd, env: Dict):
    if env:
        print(f"run: {cmd}, env: {env}")
        # NOTE: 这里一定要扩展当前的环境变量
        process = subprocess.run(cmd, shell=True, check=True, env={
                                 **os.environ, **env})
    else:
        print(f"run: {cmd}")
        process = subprocess.run(cmd, shell=True, check=True)
    return process.returncode
