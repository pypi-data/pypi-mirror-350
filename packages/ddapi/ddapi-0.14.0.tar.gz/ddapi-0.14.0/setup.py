from pathlib import Path

import setuptools

with Path.open(Path("README.md"), encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ddapi",
    version="0.14.0",
    author="ByFox",
    description="DDnet api",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ByFox213/ddapi",
    license="MIT",
    project_urls={"Github": "https://github.com/ByFox213/ddapi"},
    package_dir={"": "ddapi"},
    packages=setuptools.find_packages(where="ddapi"),
    python_requires=">=3.10",
)
