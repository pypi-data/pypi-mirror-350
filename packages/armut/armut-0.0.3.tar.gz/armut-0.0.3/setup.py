from setuptools import setup, find_packages

setup(
    name="armut",
    version="0.0.3",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "armut-ye = armut:hello"
        ]
    }
)