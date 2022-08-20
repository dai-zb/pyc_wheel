import compileall
import os
import shutil
import re
import zipfile
from typing import Union, Optional


# 递归调用，遍历一个目录下的所有文件
def _list_files(path):
    f_lst = []
    files = os.listdir(path)
    for f in files:
        if os.path.isdir(os.path.join(path, f)):
            fs = _list_files(os.path.join(path, f))
            fs = [os.path.join(f, x) for x in fs]
            f_lst.extend(fs)
        else:
            f_lst.append(f)
    return f_lst


# 清除编译的结果 清除#__pycache__ 目录下的所有
def clean(src_dir: str, out_dir: Optional[str] = None):
    dirs_lst = []
    for root, dirs, files in os.walk(src_dir):
        dirs_lst += [os.path.join(root, d) for d in dirs]
    dirs_lst = list(filter(lambda x: '__pycache__' in x, dirs_lst))
    for d in dirs_lst:
        shutil.rmtree(d)
    if out_dir and os.path.exists(out_dir):
        shutil.rmtree(out_dir)


def check_assert(file: str):
    with open(file, "r", encoding="utf-8") as f:
        for n, line in enumerate(f.readlines()):
            if line.lstrip().startswith("assert "):
                print(f'`assert` may be invalid:\n  File "{file}", line {n + 1}\n    {line.strip()}\n')


def comp(src_dir, optimize=2):
    for file in _list_files(src_dir):
        if file.endswith(".py"):
            check_assert(os.path.join(src_dir, file))

    # python -OO -m compileall src/
    compileall.compile_dir(src_dir, optimize=optimize)


# 如果是 __pycache__/xxx.cpython-38.opt-2.pyc 格式的文件，则转换成 xxx.pyc
def _handle_pyc(path):
    p, f = os.path.split(path)
    fs = f.split('.')
    f = f'{fs[0]}.{fs[-1]}'
    p1, p2 = os.path.split(p)
    if p2 == '__pycache__':
        p = p1
    return p, f


def _copy(src, dst):
    d_ = os.path.split(dst)[0]
    if not os.path.exists(d_):
        os.makedirs(d_)
    shutil.copy(src, dst)


# 打成 #压缩包
def zip_file(path, zip_name):
    files = _list_files(path)
    # 添加到压缩包
    with zipfile.ZipFile(zip_name, 'w') as z:  # 要压缩的文件名 会覆盖已经存在的
        for i in files:
            z.write(os.path.join(path, i), i)  # 打包时候重新指定路径名称


# suffix 指定后缀的文件
# dirs  指定的目录
# 只有 pyc 后缀的文件，才会被打包到一起
def package(src_path, dst_path, suffix: Union[str, list, tuple] = 'pyc'):
    files_lst = _list_files(src_path)
    if not isinstance(suffix, str):
        suffix = '|'.join(suffix)
    suffix = rf'^.*\.({suffix})$'
    suffix = re.compile(suffix, re.IGNORECASE)  # type: ignore
    files_lst = list(set(filter(lambda x: re.match(suffix, x) and not x.endswith(".py"), files_lst)))

    for f in files_lst:
        if re.match(r'^.*\.pyc$', f):
            p_, f_ = _handle_pyc(f)
            _copy(os.path.join(src_path, f), os.path.join(dst_path, p_, f_))
        else:
            _copy(os.path.join(src_path, f), os.path.join(dst_path, f))
