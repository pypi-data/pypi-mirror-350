from setuptools import setup, find_packages

setup(
    name="gbb-excel-mcp",  # PyPI 显示的包名（确保唯一性）
    version="0.1.5",    # 初始版本号
    author="wangmeng",
    author_email="meng4.wang@gongbangbang.com",
    description="excel文件中内容匹配工邦邦商品sku",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[],  # 依赖的其他包，如 ["requests>=2.25.1"]
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Python 版本要求
)
