from setuptools import setup, find_packages

setup(
    name="tomz_test",
    version="0.1.0",
    packages=find_packages(exclude=["tests*"]),
    install_requires=[
        "requests>=2.25.0",
    ],
    author="TomZz0",
    author_email="1210374096@qq.com",
    description="一个很棒的 Python 工具包",
    url="https://github.com/TomZz0/tomz_test",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
