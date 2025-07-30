# EODC SDK
![PyPI - Status](https://img.shields.io/pypi/status/eodc)
![PyPI](https://img.shields.io/pypi/v/eodc)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/eodc)

Python SDK for interacting with EODC services.

## Installation
Install the SDK with pip:

```
pip install eodc
```

## Usage
### Dask Clusters

```
from eodc import settings
from eodc.dask import EODCCluster

settings.DASK_URL = "<EODC dask gateway endpoint>"

cluster = EODCCluster()
```

### Function-as-a-Service (FaaS)
TODO


### Workspaces

A workspace is a an abstraction of a object storage container/bucket. It is used to store and retrieve data.

Workspaces are integrated with EODC products and services, such as the openEO EODC backend.

There is 2 basic types of workspaces which we distinguish between, EODC Workspaces and External Workspaces.

- External Workspaces: These are object-storage buckets/containers which the users has provisioned from a third-party or is hosting themselves. They can be registered at EODC services and used in much the same way as EODC Workspaces, just that the user retains full control over them.

- EODC (internal) Workspaces: These are object-storage buckets which the user has provisioned from specifically EODC. Below the abstraction of workspaces they are S3 Ceph buckets which the user has write/read/delete privileges on. EODC still owns these buckets, and they are basically leased storage space for the user to use with EODC services.

Workspace Adapters, the code for which can be found in the workspace module in this repository, are an easy for for interacting with workspaces, both external and internal.

They generalize across different object-storage providers/standards and are used across EODCs products for managing and linking workspaces to functionality.

The exact capabilities are outlined in the code.
