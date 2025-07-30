"""Utility to generate a random UUID"""

import random as _py_random
import uuid as _uuid
from hashlib import sha512
from typing import Any, Dict, Hashable, Type, TypeVar

from typing_extensions import deprecated


class NoPreviouslyCreatedInstanceError(Exception):
    """No previously created instance error"""


T = TypeVar("T")


class CacheLast(type):
    """Metaclass that caches the last created instance"""

    # _last_created_instance is a heterogeneous collection of type dict[Type[T], T] for
    # the different T's that use this metaclass
    _last_created_instance: Dict[Any, Any] = {}

    def __call__(cls, *args, **kwargs):
        # Create an instance
        instance = super(CacheLast, cls).__call__(*args, **kwargs)

        # Cache the instance
        CacheLast._last_created_instance[cls] = instance

        return instance

    def get_last_created(cls: Type[T]) -> T:
        """Get the last created instance"""
        if cls not in CacheLast._last_created_instance:
            raise NoPreviouslyCreatedInstanceError()

        # Promise to the type system that we are fetching a T (which we are)
        instance: T = CacheLast._last_created_instance[cls]

        return instance


class TSRandom:
    """
    Generate random values that are not available from Python 3.7's random module.
    """

    def __init__(self, *seed: Hashable):
        self._is_seeded = False
        self._random = _py_random.Random()

        if len(seed) > 0:
            self.seed(*seed)

    def seed(self, *content: Hashable) -> None:
        """
        Seed the random number generator.
        """
        content = (
            (
                part.encode()
                if isinstance(part, str)
                else str(hash(part)).encode()
                if not isinstance(part, bytes)
                else part
            )
            for part in content
        )

        try:
            hash_ = sha512(next(content))
        except StopIteration:
            return

        for part in content:
            hash_.update(part)
        rng_seed = hash_.digest()
        self._random.seed(rng_seed)
        self._is_seeded = True

    def randbytes(self, n_bytes: int) -> bytes:
        """Generate n random bytes."""
        if hasattr(self._random, "randbytes"):
            return self._random.randbytes(n_bytes)

        # Adapted from the Python 3.9+ random.randbytes method.
        return self._random.getrandbits(n_bytes * 8).to_bytes(n_bytes, "little")

    @deprecated(
        """This way of generating UUIDs is deprecated. Instead use:
- task_script_utils.uuid.uuid() for UUID generation
- mock_uuid_generator (fixture from ts-lib-pytest) for mocking UUID generation in tests
Note: ts-lib-pytest is a private TetraScience GitHub repository.
Please contact TetraScience if you want to use it or you can create your own UUID mocker)"""
    )
    def uuid(self) -> _uuid.UUID:
        """Create a pseudo random UUID"""
        return _uuid.UUID(bytes=self.randbytes(16))


class TaskScriptUUIDGenerator(TSRandom, metaclass=CacheLast):
    """UUID generator for use in Task Scripts"""

    def __init__(self, task_script_identifier: str, file_identifier: Hashable):
        super().__init__(task_script_identifier, file_identifier)

    @classmethod
    def from_task_script_identifier_parts(
        cls: Type[T], namespace: str, slug: str, version: str, file_identifier: Hashable
    ) -> T:
        """
        A convenience method that takes the parts of a task script identifier (namespace, slug, and version) and an
        identifier for the file (e.g. file location, file contents), then returns an instance of the generator class.
        """
        return cls(f"{namespace}/{slug}:{version}", file_identifier)
