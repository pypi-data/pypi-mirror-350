from setuptools import setup, find_packages

setup(
    name="docipy",
    version="2.1.0",
    packages=find_packages(),
    install_requires=[
        "clight",
        "markdown"
    ],
    entry_points={
        "console_scripts": [
            "docipy=docipy.main:main",  # Entry point of the app
        ],
    },
    package_data={
        "docipy": [
            "main.py",
            "__init__.py",
            ".system/imports.py",
            ".system/index.py",
            ".system/modules/-placeholder",
            ".system/sources/author.png",
            ".system/sources/bootstrap-icons.woff",
            ".system/sources/bootstrap-icons.woff2",
            ".system/sources/bootstrap.icons.css",
            ".system/sources/clight.json",
            ".system/sources/docipy.js",
            ".system/sources/docipy.scss",
            ".system/sources/highlight.js",
            ".system/sources/logo.ico",
            ".system/sources/robots.txt",
            ".system/sources/sitemap.xml",
            ".system/sources/template.html",
            ".system/sources/lng/ge.yaml",
            ".system/sources/lng/ru.yaml"
        ],
    },
    include_package_data=True,
    author="Irakli Gzirishvili",
    author_email="gziraklirex@gmail.com",
    description="DociPy is designed to easily generate impressive static HTML documentations",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/IG-onGit/DociPy",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
