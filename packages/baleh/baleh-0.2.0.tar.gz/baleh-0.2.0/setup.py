from setuptools import setup, find_packages

setup(
    name="baleh",
    version="0.2.0",
    packages=find_packages(),
    install_requires=[
        "aiohttp>=3.8.0",
        "requests>=2.25.0",
    ],
    author="Hamid Rashidi",
    author_email="spiderhamidman@gmail.com",
    description="An advanced Python library for Bale messenger bots, inspired by Telegram Bot API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/hamidrashidi98/baleh",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Communications :: Chat",
    ],
    python_requires=">=3.7",
)