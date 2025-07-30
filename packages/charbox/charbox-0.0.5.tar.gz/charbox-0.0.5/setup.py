from setuptools import setup, find_packages

setup(
    name="charbox",
    version="0.0.5",
    author="Taireru LLC",
    author_email="tairerullc@gmail.com",
    description="CharBox is a Python library that generates random character attributes, including names, hair colors, and eye colors. It supports multiple name origins and offers standard and fancy variations for hair and eye colors.",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/TaireruLLC/charbox",
    packages=find_packages(),
    install_requires=[
        "altcolor>=0.0.5",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    license="MIT",
)
