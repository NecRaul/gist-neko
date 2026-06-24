from importlib.metadata import PackageNotFoundError, version

try:
    __version__: str = version("gist_neko")
except PackageNotFoundError:
    __version__: str = "dev"
