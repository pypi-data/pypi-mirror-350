# open_ksa/__init__.py
from setuptools_scm import get_version

try:
    # Attempt to get the version from the SCM metadata
    __version__ = get_version()
except LookupError:
    # Fallback to a default version if SCM metadata is not available
    __version__ = "0.0.0"
    
from urllib.parse import urlparse, quote
from .download_file import download_file
from open_ksa.get_dataset_resource import get_dataset_resource
from open_ksa.get_dataset_resources import get_dataset_resources
from open_ksa.get_org_resources import get_org_resources
from open_ksa.ssl_adapter import SSLAdapter, SingletonSession
from open_ksa.organizations import organizations