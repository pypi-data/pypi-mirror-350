from setuptools import setup, find_packages

setup(
    name="armut",
    version="0.0.2",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "armut-ye = karpuz:hello"
        ]
    }
)