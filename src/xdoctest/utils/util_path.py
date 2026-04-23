"""
Utilities related to filesystem paths
"""

from __future__ import annotations

import os
import shutil
from os.path import exists, join, normpath


class TempDir:
    """
    Context for creating and cleaning up temporary files. Used in testing.

    Example:
        >>> with TempDir() as self:
        >>>     dpath = self.dpath
        >>>     assert exists(dpath)
        >>> assert not exists(dpath)

    Example:
        >>> self = TempDir()
        >>> dpath = self.ensure()
        >>> assert exists(dpath)
        >>> self.cleanup()
        >>> assert not exists(dpath)
    """

    def __init__(self, persist: bool = False) -> None:
        self.dpath: str | None = None
        self.persist = persist

    def __del__(self) -> None:
        self.cleanup()

    def ensure(self) -> str:
        pass

    def cleanup(self) -> None:
        pass

    def __enter__(self) -> TempDir:
        self.ensure()
        return self

    def __exit__(self, type_: object, value: object, trace: object) -> None:
        self.cleanup()


def ensuredir(
    dpath: str | tuple[str, ...] | list[str], mode: int = 0o1777
) -> str:
    """
    Ensures that directory will exist. creates new dir with sticky bits by
    default

    Args:
        dpath (str): dir to ensure. Can also be a tuple to send to join
        mode (int): octal mode of directory (default 0o1777)

    Returns:
        str: path - the ensured directory
    """
    if isinstance(dpath, (list, tuple)):  # nocover
        dpath = join(*dpath)
    if not exists(dpath):
        try:
            os.makedirs(normpath(dpath), mode=mode)
        except OSError:  # nocover
            raise
    return dpath
