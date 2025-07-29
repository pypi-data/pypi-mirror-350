from setuptools import setup, find_packages

# Read the README.md file
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="minaki-apt",
    version="0.1.1",
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
    long_description=long_description,
    long_description_content_type="text/markdown",  # 💡 Tells PyPI to render markdown
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
