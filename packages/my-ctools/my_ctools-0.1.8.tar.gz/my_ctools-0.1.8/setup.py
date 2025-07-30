from setuptools import setup, Extension
import pybind11
import platform

# 配置各个C++模块
cpp_modules = [
    "cal_cpr",
    "cal_all_largest_indicators",
    "cal_all_longest_indicators",
    "cal_longest_dd_recover",
    "cal_max_dd",
    "cal_rolling_gain_loss",
]

extra_compile_args = [
    '-std=c++17',  # 使用 C++17 标准
    '-O3',  # 开启最高级别优化（优化性能）
    '-fPIC'  # 生成位置无关代码
]

arch = platform.machine()  # 动态检测当前平台架构

# 判断是否为 x86_64 架构
if arch == "x86_64":
    extra_compile_args.append('-mavx')  # 启用 AVX SIMD 指令集

ext_modules = [
    Extension(
        # 模块名称，格式为 my_ctools.xxx，xxx 为具体模块名
        name=f"my_ctools.{mod}",
        # C++源文件路径，每个模块对应一个 cpp 文件
        sources=[f"my_ctools/{mod}.cpp"],
        # 包含目录，用于指定头文件路径，pybind11.get_include() 获取 pybind11 的头文件路径
        include_dirs=[pybind11.get_include()],
        # 指定编程语言为 C++
        language="c++",
        # 编译参数，如 -std=c++17（C++17 标准）、-O3（最高优化级别）等
        extra_compile_args=extra_compile_args,
    )
    for mod in cpp_modules  # 遍历 cpp_modules 列表，为每个模块生成配置
]


setup(
    # 包名，安装后的模块名称
    name="my_ctools",
    # 版本号，用于标识模块版本
    version="0.1.8",
    # 作者名称，显示在包的元数据中
    author="KevinCJM",
    # 描述信息，简要说明该模块的功能
    description="Fast C++ indicators for fund analytics",
    # 包列表，指定需要打包的 Python 包
    packages=["my_ctools"],
    # 扩展模块列表，包含所有通过 pybind11 编译的 C++ 扩展模块
    ext_modules=ext_modules,
    # 是否允许 zip 安装，设置为 False 表示不支持 zip 安装
    zip_safe=False,
    # Python 版本要求，表示该模块需要 Python 3.8 或更高版本
    python_requires=">=3.8",
)
