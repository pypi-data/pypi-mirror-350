from setuptools import setup, find_packages

setup(
    name="minaki-apt",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests",
        "click",
    ],
    entry_points={
        "console_scripts": [
            "minaki-cli = minaki_cli.cli:cli",
            "minaki-apt = minaki_cli.cli:cli"

        ]
    },
    author="MinakiLabs",
    description="CLI tool to interact with Minaki APT Repo",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
