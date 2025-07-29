from abc import abstractmethod
from collections.abc import Iterable, Sequence
from typing import IO, Any, Protocol, Self, runtime_checkable


@runtime_checkable
class Comparable(Protocol):  # noqa: PLW1641
    """
    Based on https://github.com/python/typing/issues/59
    """

    @abstractmethod
    def __eq__(self, other: object, /) -> bool:
        ...

    @abstractmethod
    def __lt__(self, other: Self, /) -> bool:
        ...

    def __gt__(self, other: Self, /) -> bool:
        return (not self < other) and self != other

    def __le__(self, other: Self, /) -> bool:
        return self < other or self == other

    def __ge__(self, other: Self, /) -> bool:
        return (not self < other)


@runtime_checkable
class PurePathLike(Comparable, Protocol):
    @property
    @abstractmethod
    def parts(self) -> Sequence[str]:
        ...

    @property
    @abstractmethod
    def parent(self) -> Self:
        ...

    @property
    @abstractmethod
    def parents(self) -> Sequence[Self]:
        ...

    @property
    @abstractmethod
    def name(self) -> str:
        ...

    @property
    @abstractmethod
    def suffix(self) -> str:
        ...

    @property
    @abstractmethod
    def suffixes(self) -> Sequence[str]:
        ...

    @property
    @abstractmethod
    def stem(self) -> str:
        ...

    @abstractmethod
    def is_absolute(self) -> bool:
        ...

    @abstractmethod
    def is_relative_to(self, other: Self, /) -> bool:
        ...

    @abstractmethod
    def relative_to(self, other: Self, /) -> Any:
        ...

    @abstractmethod
    def joinpath(self, *segments: Any) -> Self:
        ...

    @abstractmethod
    def full_match(self, pattern: str) -> bool:
        ...

    @abstractmethod
    def match(self, path_pattern: str) -> bool:
        ...

    @abstractmethod
    def with_name(self, name: str) -> Self:
        ...

    @abstractmethod
    def with_suffix(self, suffix: str) -> Self:
        ...

    @abstractmethod
    def with_stem(self, stem: str) -> Self:
        ...

    @abstractmethod
    def with_segments(self, *segments: Any) -> Self:
        ...

    def __truediv__(self, key: Any, /) -> Self:
        return self.with_segments(self, key)

    @abstractmethod
    def __rtruediv__(self, key: Any, /) -> Any:
        ...

    @abstractmethod
    def __fspath__(self) -> str:
        ...


@runtime_checkable
class PathLike(PurePathLike, Protocol):
    @classmethod
    @abstractmethod
    def from_uri(cls, uri: str) -> Self:
        ...

    @abstractmethod
    def as_uri(self) -> str:
        ...

    @abstractmethod
    def stat(self) -> Any:
        ...

    @abstractmethod
    def open(self) -> IO[Any]:
        ...

    @abstractmethod
    def read_bytes(self) -> bytes:
        ...

    @abstractmethod
    def write_bytes(self, data: bytes) -> Any:
        ...

    @abstractmethod
    def read_text(self) -> str:
        ...

    @abstractmethod
    def write_text(self, data: str) -> Any:
        ...

    @abstractmethod
    def iterdir(self) -> Iterable[Self]:
        ...

    @abstractmethod
    def glob(self, pattern: str) -> Iterable[Self]:
        ...

    @abstractmethod
    def rglob(self, pattern: str) -> Iterable[Self]:
        ...

    @abstractmethod
    def walk(self, top_down: bool = True) -> Iterable[tuple[Self, Sequence[str], Sequence[str]]]:
        ...

    @abstractmethod
    def absolute(self) -> Self:
        ...

    @abstractmethod
    def resolve(self) -> Self:
        ...

    @abstractmethod
    def exists(self) -> bool:
        ...

    @abstractmethod
    def is_dir(self) -> bool:
        ...

    @abstractmethod
    def is_file(self) -> bool:
        ...

    @abstractmethod
    def samefile(self, other_path: str | Self) -> bool:
        ...

    @abstractmethod
    def touch(self, *, exist_ok: bool = True) -> None:
        ...

    @abstractmethod
    def mkdir(self, *, parents: bool = False, exist_ok: bool = False) -> None:
        ...

    @abstractmethod
    def unlink(self, *, missing_ok=False) -> None:
        ...

    @abstractmethod
    def rmdir(self) -> None:
        ...

    @abstractmethod
    def rename(self, target: Self) -> Self:
        ...

    @abstractmethod
    def replace(self, target: Self) -> Self:
        ...
