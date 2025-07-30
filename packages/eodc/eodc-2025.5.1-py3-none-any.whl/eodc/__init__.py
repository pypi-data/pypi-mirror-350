import importlib.metadata

__version__ = importlib.metadata.version("eodc")

from eodc.settings import settings  # noqa

from . import auth, dask, faas, storage, visualisation, workspace  # noqa
