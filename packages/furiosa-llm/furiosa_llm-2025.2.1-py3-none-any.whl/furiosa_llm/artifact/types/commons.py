from abc import ABC, abstractmethod
import functools

from pydantic import BaseModel
from typing_extensions import Self


class ArtifactBase(BaseModel, ABC):
    """Abstract class for old version artifacts."""

    @classmethod
    @abstractmethod
    def from_previous_version(cls, previous_version_artifact) -> Self: ...


# NOTE: The following version identification is specific to `Artifact`.
# The version must be updated appropriately whenever any change,
# occurs in the format of `Artifact` or its related types.
# Version follows the format `X.Y` (where each X,Y represents major, minor versions)

# FIXME: A tentative policy is that each major version change should result in the creation
# of a new `ArtifactBase` class.


@functools.total_ordering
class SchemaVersion(BaseModel):
    major: int
    minor: int

    def __eq__(self, other):
        if not isinstance(other, SchemaVersion):
            return False
        return (self.major, self.minor) == (
            other.major,
            other.minor,
        )

    def __lt__(self, other):
        if not isinstance(other, SchemaVersion):
            return False
        return (self.major, self.minor) < (other.major, other.minor)
