# setup.py
# 告诉 setuptools 怎么编译 C++ 扩展模块
#
# 当你执行 pip install . 或 uv pip install . 时：
#   1. setuptools 读取这个文件
#   2. 调用 C++ 编译器编译 .cpp 文件
#   3. 链接 pybind11 和 Python 库
#   4. 生成 crc_module.pyd（Windows）
#   5. 安装到虚拟环境的 site-packages 中
#   6. 之后 import crc_module 就能用了

import platform
from pybind11.setup_helpers import Pybind11Extension, build_ext
from setuptools import setup

extra_compile_args = []
if platform.system() == "Windows":
    extra_compile_args.append("/utf-8")

ext_modules = [
    Pybind11Extension(
        "crc_module",
        ["crc_calculator.cpp", "bindings.cpp"],
        language="c++",
        extra_compile_args=extra_compile_args,
    ),
]

setup(
    name="test-0626-pybind-00",
    version="0.1.0",
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext},   # 使用 pybind11 的构建命令
)