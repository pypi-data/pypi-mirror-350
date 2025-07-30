from setuptools import setup, find_packages

# setup(
#     name="hello",          # 包名（pip install 时用）
#     version="0.1.1",           # 版本号
#     package_dir={"": "dist3"},   # 指定源码目录为 src/
#     packages=find_packages(where='dist3'),  # 自动发现 src/ 下的包
#     include_package_data=True,
#     data_files=[('', ['dist3\hello\pyarmor_runtime_000000\pyarmor_runtime.pyd'])],
# )
setup(
    name="hello-ronalgao",          # 包名（pip install 时用）
    version="0.1.8",
    package_dir={"": "dist3"},   # 指定源码目录为 dist3/
    packages=find_packages(where='dist3'),  # 自动发现 dist3/ 下的包
    include_package_data=True,
    data_files=[('', ['dist3\hello\pytransform\_pytransform.dll'])],
)