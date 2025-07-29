#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
G2PY: Python数据可视化库
基于蚂蚁集团G2可视化引擎
"""

from setuptools import setup, find_packages
import os

# 读取README文件作为长描述
def read_long_description():
    try:
        with open("README.md", "r", encoding="utf-8") as fh:
            return fh.read()
    except FileNotFoundError:
        return "G2PY: Python数据可视化库，基于蚂蚁集团G2可视化引擎"

# 读取requirements.txt
def read_requirements():
    try:
        with open("requirements.txt", "r", encoding="utf-8") as fh:
            return [line.strip() for line in fh if line.strip() and not line.startswith("#")]
    except FileNotFoundError:
        return ["jinja2>=3.1.0", "simplejson>=3.17.0"]

setup(
    name="g2py",
    version="1.0.0",
    author="G2PY Development Team", 
    author_email="admin@g2py.org",
    description="基于蚂蚁集团G2可视化引擎的Python数据可视化库",
    long_description=read_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/g2py/g2py",
    project_urls={
        "Bug Reports": "https://github.com/g2py/g2py/issues",
        "Source": "https://github.com/g2py/g2py",
        "Documentation": "https://github.com/g2py/g2py/blob/main/README.md",
    },
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "g2py": [
            "templates/*.html",
            "static/*.js",
            "static/*.css",
        ],
    },
    classifiers=[
        # 开发阶段
        "Development Status :: 4 - Beta",
        
        # 目标用户
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",
        
        # 主题分类
        "Topic :: Scientific/Engineering :: Visualization",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Multimedia :: Graphics :: Graphics Conversion",
        
        # 许可证
        "License :: OSI Approved :: MIT License",
        
        # 支持的Python版本
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3 :: Only",
        
        # 操作系统支持
        "Operating System :: OS Independent",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
        
        # 环境
        "Environment :: Web Environment",
        "Environment :: Console",
        "Framework :: Jupyter",
    ],
    keywords="数据可视化, 图表, G2, AntV, Python, Jupyter, 可视化",
    python_requires=">=3.11",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
        "jupyter": [
            "jupyter>=1.0.0",
            "jupyterlab>=3.0.0",
            "ipython>=7.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "g2py=g2py.cli:main",
        ],
    },
    zip_safe=False,
)
