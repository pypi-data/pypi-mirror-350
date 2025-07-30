from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pgs_compare",
    version="0.2.2",
    author="Alexander Craig",
    description="Compare PGS across ancestry groups",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alex1craig/pgs-compare",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "pgs_compare": ["scripts/*.sh"],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pandas",
        "numpy",
        "matplotlib",
        "requests",
        "zstandard",
        "pgscatalog-utils",
        "scipy",
    ],
    entry_points={
        "console_scripts": [
            "pgs-compare=pgs_compare.cli:main",
        ],
    },
)
