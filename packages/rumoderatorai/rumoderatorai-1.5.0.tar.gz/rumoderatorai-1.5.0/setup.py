import setuptools

import os


version = {}
with open("rumoderatorai/data.py") as fp:
    exec(fp.read(), version)
    version = version["__version__"]

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


if os.path.exists("dist"):
    if any(version in dist for dist in os.listdir("dist")):
        print("Version already exists")
        exit(1)


setuptools.setup(
    name="rumoderatorai",
    version=version,
    author="PyWebSol",
    description="Библиотека для использования Omni Antispam API (https://moderator.omni-devel.ru)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://moderator.omni-devel.ru",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=["aiohttp", "Pillow", "boltons"],
)
