import os.path
import zipfile


def inject(wheel_path: str, name: str, out_dir: str):
    z1 = zipfile.ZipFile(wheel_path, 'r')  # 要压缩的文件名 会覆盖已经存在的
    path, file = os.path.split(wheel_path)
    p1, p2 = os.path.split(path)
    path = os.path.join(p1, f".{p2}")
    if not os.path.exists(path):
        os.mkdir(path)
    z2 = zipfile.ZipFile(os.path.join(path, file), 'w')  # 要压缩的文件名 会覆盖已经存在的
    for x in z1.namelist():
        if x.endswith(".py"):
            x = x + "c"  # .py  => .pyc
            with open(os.path.join(out_dir, x), "rb") as f:
                bs = f.read()
        else:
            bs = z1.read(x)
        z2.writestr(x, bs)

    z1.close()
    z2.close()
