from setuptools import setup, find_packages

VERSION = "1.4"
DESCRIPTION = "CLI for downloading all gists from a specified user."
LONG_DESCRIPTION = "Download specified user's all gists at once. You can also use environment variables if you don't want to pass through arguments everytime you want to download a gist. If you don't provide a public access token it will only download public gists."
AUTHOR = "NecRaul"

setup(
    name="gist_neko",
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author=AUTHOR,
    packages=find_packages(),
    install_requires=["requests"],
    keywords=["python", "gists downloader", "downloader", "gists", "gist-neko", "kuroneko"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Internet :: WWW/HTTP"
    ],
    py_modules=["download", "environment"],
    entry_points={
        "console_scripts": [
            "gist-neko = gist_neko.__init__:main",
        ],
    },
)