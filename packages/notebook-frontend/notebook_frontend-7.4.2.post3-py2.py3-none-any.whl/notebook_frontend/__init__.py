import importlib.metadata


try:
    __version__ = importlib.metadata.version("notebook_frontend")
except importlib.metadata.PackageNotFoundError:
    __version__ = "unknown"

