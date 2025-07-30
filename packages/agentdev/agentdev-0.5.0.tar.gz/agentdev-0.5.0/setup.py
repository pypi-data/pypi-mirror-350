# -*- coding: utf-8 -*-
from setuptools import find_packages, setup

import configparser
import os.path
import sys
from shutil import rmtree
from typing import List

# make sure the build file is up to date
if os.path.exists("./build"):
    rmtree("./build")
if os.path.exists("./agentdev.egg-info"):
    rmtree("./agentdev.egg-info")

# build different package for different condition
package_name = "internal"
for i, arg in enumerate(sys.argv):
    if arg == "--package" and i + 1 < len(sys.argv):
        package_name = sys.argv[i + 1]
        sys.argv.remove("--package")
        sys.argv.remove(package_name)
        break

# get config from setup.cfg
config = configparser.ConfigParser()
config.read("setup.cfg")

# get packages to exclude
exclude_packages = []
if package_name and package_name in config:
    exclude_packages = config[package_name]["exclude_packages"].split(",")
packages = find_packages(exclude=exclude_packages)


# get requirements
def parse_requirements(file_name: str) -> List[str]:
    with open(file_name) as f:
        return [
            require.strip()
            for require in f
            if require.strip() and not require.startswith("#")
        ]


# get readme
def readme() -> str:
    with open("README.md", encoding="utf-8") as f:
        content = f.read()
    return content


# get version file
version_file = "agentdev/version.py"


def get_version() -> str:
    with open(version_file, "r", encoding="utf-8") as f:
        exec(compile(f.read(), version_file, "exec"))
    version = locals()["__version__"]
    if package_name == "internal":
        version += "-alpha"
    return version


# build method
setup(
    name="agentdev",
    version=get_version(),
    description="AgentDev provides basic components that used on Bailian."
    "platform with unified API",
    author="Bailian Team",
    author_email="zhangzhicheng.zzc@alibaba-inc.com",
    keywords="python, Agent, AIGC, LLM,  Components",
    url="https://code.alibaba-inc.com/dashscope/bailiansdk",
    license="Apache License 2.0",
    packages=packages,
    include_package_data=False,
    install_requires=parse_requirements("requirements.txt"),
    long_description=readme(),
    long_description_content_type="text/markdown",
)
