from setuptools import setup, find_packages
import os

# 读取requirements.txt中的依赖项
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

# 读取README.md作为长描述
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="orion_browser",
    version="0.4.3",
    author="BTY Team",
    author_email="qianhai@bantouyan.com",
    description="浏览器代理服务器",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bantouyan/orion",
    packages=find_packages(include=['orion_browser', 'orion_browser.*', 'app', 'app.*', 'app_data', 'browser_use', 'browser_use.*']),
    include_package_data=True,
    package_data={
        'app_data': ['js/*.js'],
        'browser_use': ['dom/*', 'browser/*', 'controller/*', 'agent/*', 'telemetry/*'],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'orion-server=app:start_server',
        ],
    },
) 