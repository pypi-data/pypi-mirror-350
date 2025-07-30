from setuptools import setup, find_packages

setup(
    name="pg-mypip",
    version="0.1.0",
    description="A simple pip wrapper for virtualenv management",
    author="Swetank Mishra",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "my_pip=pg.my_pip:cli",
        ],
    },
    python_requires=">=3.6",
)