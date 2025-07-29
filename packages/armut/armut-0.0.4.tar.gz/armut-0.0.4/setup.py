from setuptools import setup, find_packages

with open("README.md", "r") as f:
    description = f.read()

setup(
    name="armut",
    version="0.0.4",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "armut-ye = armut:hello"
        ]
    },
    long_description=description,
    long_description_content_type="text/markdown"
)