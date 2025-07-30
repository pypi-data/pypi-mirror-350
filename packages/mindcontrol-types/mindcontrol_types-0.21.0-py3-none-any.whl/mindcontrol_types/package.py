from typing import Union, Literal, Dict, Optional
from typing_extensions import Annotated
from pydantic import Field
from genotype import Model


PackageNpmDependencies = Dict[str, str]
"""npm package dependencies."""


class PackageNpm(Model):
    """npm package."""

    type: Literal["npm"]
    """Package type."""
    name: str
    """Package name."""
    version: str
    """Package version."""
    shasum: str
    """SHA1 checksum."""
    tarball: str
    """Tarball URL."""
    tag: str
    """Tag name."""
    time: int
    """Unix timestamp in milliseconds."""
    dependencies: PackageNpmDependencies
    """Package dependencies."""


class PackagePip(Model):
    """Pip package."""

    type: Literal["pip"]
    """Package type."""
    name: str
    """Package name."""
    version: str
    """Package version."""
    sha256: str
    """SHA-256 checksum."""
    wheel: str
    """Wheel file URL."""


Package = Annotated[Union[PackageNpm, PackagePip], Field(json_schema_extra={'discriminator': 'type'})]
"""Collection package."""


PackageSettingTransformCase = Union[Literal["never"], Literal["shallow"], Literal["everything"]]
"""Transform case setting."""


class PackageBaseSettings(Model):
    enabled: Optional[bool] = None
    """If the package is enabled. Toggling this setting does not trigger
    major version bump."""
    transform_case: Optional[PackageSettingTransformCase] = None
    """Transfor case setting. Changing this setting triggers major version
    bump."""
    client_prerelease: Optional[bool] = None
    """Use prerelease client version. Changing this setting triggers major version
    bump."""


PackageNpmClientVersion = Union[Literal[0], Literal[1]]
"""Npm package client version."""


class PackageNpmSettings(PackageBaseSettings, Model):
    """Npm package settings."""

    client_version: Optional[PackageNpmClientVersion] = None
    """Npm package client version. Changing the client version triggers major
    version bump."""


PackagePipClientVersion = Union[Literal[0], Literal[1]]
"""Pip package client version."""


class PackagePipSettings(PackageBaseSettings, Model):
    """Pip package settings."""

    client_version: Optional[PackagePipClientVersion] = None
    """Pip package client version. Changing the client version triggers major
    version bump."""


class PackagesSettings(Model):
    """Package settings."""

    npm: Optional[PackageNpmSettings] = None
    """Npm package settings."""
    pip: Optional[PackagePipSettings] = None
    """Pip package settings."""


PackageStatus = Union[Literal["pending"], Literal["building"], Literal["errored"], Literal["published"]]
"""Status of the package."""


class PackageTrigger(Model):
    """Package trigger message."""

    id: int
    """Package id."""
