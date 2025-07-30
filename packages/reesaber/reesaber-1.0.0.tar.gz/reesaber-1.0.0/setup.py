import os
import re
from setuptools import setup, find_packages

long_description = """
# reesaber-py
Make ReeSaber Presets in Python!

**reesaber-py is designed for 0.3.7+ but could work on other versions. I will not provide support for versions older than 0.3.7.**

## Feature Support
- ✅: Fully supported
- ⚠: Partially implemented (and by extension experimental)
- ❌: Not implemented

## Modules
| Module        | Support |
|---------------|---|
| Blur Saber    |✅|
| Trail         |✅|
| Points VFX    |❌|
| Sparks VFX    |❌|
| Ribbons VFX   |❌|
| Vanilla Saber |✅|

## License
MIT
"""
def get_version():
    init_file_path = os.path.join("reesaber", "__init__.py")
    with open(init_file_path, "r", encoding="utf-8") as f:
        init_content = f.read()
    version_match = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', init_content)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Cannot find version information")

setup(
    name="reesaber",
    version=get_version(),
    author="CodeSoftGit",
    author_email="hello@mail.codesoft.is-a.dev",
    description="A Python library for creating Beat Saber ReeSaber mod configurations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CodeSoftGit/reesaber-py",
    project_urls={
        "Bug Tracker": "https://github.com/CodeSoftGit/reesaber-py/issues",
        "Documentation": "https://github.com/CodeSoftGit/reesaber-py/wiki/Docs",
        "Source Code": "https://github.com/CodeSoftGit/reesaber-py",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Games/Entertainment",
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities",
    ],
    packages=find_packages(include=["reesaber", "reesaber.*"]),
    python_requires=">=3.8",
    install_requires=[
        "pydantic>=2.0.0",
        "pillow",  # For image processing
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=23.0.0",
            "isort>=5.10.0",
            "mypy>=1.0.0",
            "flake8>=6.0.0",
        ],
    },
    keywords="beatsaber, reesaber, gaming, vr, mod, configuration",
    license="MIT",
    include_package_data=True,
    zip_safe=False,
)