from setuptools import setup, find_packages

VERSION = "0.1"
DESCRIPTION = ""
LONG_DESCRIPTION = ""
AUTHOR = "NecRaul"

setup(
    name="gist_neko",
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author=AUTHOR,
    packages=find_packages(),
    install_requires=["requests"],
    keywords=[],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Internet :: WWW/HTTP"
    ],
    py_modules=["download"],
    entry_points={
        "console_scripts": [
            "gist-neko = gist_neko.__init__:main",
        ],
    },
)