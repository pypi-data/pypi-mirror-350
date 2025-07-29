from setuptools import setup, find_packages

setup(
    name="ADOBase",
    version="0.1.0",
    description="为 ADOFAI 游戏的 .adofai 关卡文件提供读写、查找、增删改等操作的库",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="memsys-lizi",
    author_email="19100817974@163.com",
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=[],
    url="https://github.com/small-lizi/ADOBase",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    include_package_data=True,
) 