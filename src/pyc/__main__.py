import glob
import sys

from .pyc_package import clean, comp, package, zip_file
from .inject_to_wheel import inject


def run(src: str, name: str, dist: str, out: str, optimize: int, suffix: str):
    src_dir = f"{src}/{name}"

    clean(src_dir, out)
    # 编译为pyc
    comp(src_dir, optimize)
    # 将编译后的文件复制出来
    package(src_dir, f"{out}/{name}", suffix)
    zip_file(f"{out}/{name}", f"{out}/{name}.py{sys.version_info.major}{sys.version_info.minor}")
    clean(src_dir)

    # 找得到打包后的wheel
    _wheel_path = glob.glob(f"{dist}/{name}-*.whl")
    if len(_wheel_path) == 1:
        wheel_path = _wheel_path[0]
        # 使用pyc打成wheel包
        inject(wheel_path, name, out)
        # clean(src_dir, out)


def main():
    cfg = {
        "dist": "dist",
        "out": ".pyc",
        "optimize": "2",
        "suffix": "pyc"  # ".*"
    }

    args = ["src", "name", "dist", "out", "optimize", "suffix"]

    for a, arg in zip(args, sys.argv[1:]):
        cfg[a] = arg
    cfg["optimize"] = int(cfg["optimize"])  # type: ignore

    print()
    print(cfg)
    print()

    run(**cfg)  # type: ignore


if __name__ == '__main__':
    # 先打包成为wheel
    # python setup.py bdist_wheel
    main()
