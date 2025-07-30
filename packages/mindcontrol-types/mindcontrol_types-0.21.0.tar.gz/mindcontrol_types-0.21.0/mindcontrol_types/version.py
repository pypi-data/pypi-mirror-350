from .package import PackagesSettings
from typing import Optional
from genotype import Model


class VersionSettings(Model):
    """Collection version settings. Unlike the payload settings, the version
    settings aren't needed for the runtime and aren't sent to the clients,
    however also affect the collection versioning."""

    packages: Optional[PackagesSettings] = None
    """Packages settings object."""
