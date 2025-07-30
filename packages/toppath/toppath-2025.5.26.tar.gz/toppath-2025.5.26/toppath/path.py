#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import pathlib
from typing import Any

from path import Path as pathPath


class Path(pathPath):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    @property
    def pp(self) -> pathlib.Path:
        return pathlib.Path(str(self))

    def __getattr__(self, name: str) -> Any:
        """
        Delegate all unknown attributes to the pathlib.Path object.
        the return value of the attribute is from pathlib.Path
        instead of this class object
        """
        return getattr(self.pp, name)

    def mkdirs(self, *args: Any, **kwargs: Any) -> Any:
        return self.makedirs(*args, **kwargs)

    def mkdirs_p(self, *args: Any, **kwargs: Any) -> Any:
        return self.makedirs_p(*args, **kwargs)

    def rm(self, *args: Any, **kwargs: Any) -> Any:
        return self.remove(*args, **kwargs)

    def rm_p(self, *args: Any, **kwargs: Any) -> Any:
        return self.remove_p(*args, **kwargs)

    def rmdirs(self, *args: Any, **kwargs: Any) -> Any:
        return self.removedirs(*args, **kwargs)

    def rmdirs_p(self, *args: Any, **kwargs: Any) -> Any:
        return self.removedirs_p(*args, **kwargs)

    def is_abs(self) -> bool:
        return self.isabs()

    def is_link(self) -> bool:
        return self.islink()

    def is_mount(self) -> bool:
        return self.ismount()

    def is_same_as(self, other: Any) -> bool:
        """check file content if same or not"""
        try:
            if self.samefile(other):
                return True

            return self.read_hexhash("sha256") == self.__class__(other).read_hexhash("sha256")
        except Exception:
            return False

    def abspath(self) -> Any:
        return self.absolute()

    def set_encoding_stuff(self, kwargs: dict) -> None:
        kwargs.setdefault("encoding", "utf-8")
        kwargs.setdefault("errors", "ignore")

    def read_lines(self, *args: Any, **kwargs: Any) -> list:
        self.set_encoding_stuff(kwargs)
        kwargs.setdefault("retain", False)
        return self.lines(*args, **kwargs)

    def write_lines(self, lines: list, *args: Any, **kwargs: Any) -> None:
        self.set_encoding_stuff(kwargs)
        kwargs.setdefault("linesep", None)
        return self.write_lines(lines, *args, **kwargs)

    def write_text(self, text: str, *args: Any, **kwargs: Any) -> None:
        self.set_encoding_stuff(kwargs)
        kwargs.setdefault("linesep", None)
        return self.write_text(text, *args, **kwargs)
