from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="apklisparser",
    version="1.1.0",
    packages=["apklisparser"],
    author="Rafael Mendoza",
    author_email="ralexm14@gmail.com",
    description="Apklis apk parser",
    url="https://github.com/ramendoza/apklisparser",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=["androguard","wand"],
    python_requires='>=3.9',
)
