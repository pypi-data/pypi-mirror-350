from __future__ import annotations

from collections.abc import Callable, Iterable, Iterator, Mapping, MutableMapping
from typing import Any


class TrieDict[VT: Any](MutableMapping[str, VT]):
    def __init__(
        self,
        initial_data: Mapping[str, VT] | Iterable[tuple[str, VT]] | None = None,
    ) -> None:
        self.root: dict[str, Any] = {}

        self.__len: int = 0

        if initial_data:
            for key, value in (
                initial_data.items() if isinstance(initial_data, Mapping)
                else initial_data
            ):
                self.__setitem__(key, value)

    def __len__(self) -> int:
        return self.__len

    def __find(self, s: str, func: Callable[[dict[str, Any], str], Any]) -> Any:
        node: dict[str, Any] = self.root

        while True:
            c: str = s[0] if s else ""
            rest: str = s[1:] if s else ""

            next_node: dict[str, Any] | tuple[str, VT] | None = node.get(c)
            if next_node is None:
                raise KeyError

            if isinstance(next_node, dict):
                node = next_node
                s = rest
                continue

            if rest == next_node[0]:
                return func(node, c)

            raise KeyError

    def __delitem__(self, s: str) -> None:
        def delitem(node: dict[str, Any], c: str) -> None:
            del node[c]
            self.__len -= 1

        return self.__find(s, delitem)

    def __getitem__(self, s: str) -> VT:
        def getitem(node: dict[str, Any], c: str) -> VT:
            return node[c][1]

        return self.__find(s, getitem)

    def __setitem__(self, s: str, v: VT) -> None:
        self.__set(s, v, self.root, is_new=True)

    def __set(self, s: str, v: VT, node: dict[str, Any], *, is_new: bool) -> None:
        if not s:
            is_new = is_new and "" not in node
            node[""] = ("", v)
            if is_new:
                self.__len += 1

            return

        c: str = s[0]
        rest: str = s[1:]

        next_node: dict[str, Any] | tuple[str, VT] | None = node.get(c)
        if next_node is None:
            node[c] = (rest, v)
            if is_new:
                self.__len += 1
        elif isinstance(next_node, dict):
            self.__set(rest, v, next_node, is_new=is_new)
        else:
            other_rest: str
            other_value: VT
            other_rest, other_value = next_node

            if rest == other_rest:
                node[c] = (rest, v)
                return

            next_node = node[c] = {}

            self.__set(other_rest, other_value, next_node, is_new=False)
            self.__set(rest, v, next_node, is_new=is_new)

    def __iter__(self) -> Iterator[str]:
        for _, value in self.__prefixes("", self.root):
            yield value

    def prefixes(self) -> Iterator[tuple[str, str]]:
        yield from self.__prefixes("", self.root)

    def __prefixes(self, prefix: str, node: dict[str, Any]) -> Iterator[tuple[str, str]]:
        for key, next_node in node.items():
            new_prefix = prefix + key
            if isinstance(next_node, dict):
                yield from self.__prefixes(new_prefix, next_node)
            else:
                yield (new_prefix, new_prefix + next_node[0])

    def match(self, prefix: str) -> Iterator[str]:
        node: dict[str, Any] = self.root
        s: str = prefix

        matched: str = ""

        while s:
            c: str = s[0]
            rest: str = s[1:]
            matched += c

            next_node: dict[str, Any] | tuple[str, VT] | None = node.get(c)
            if next_node is None:
                return

            if isinstance(next_node, dict):
                node = next_node
                s = rest
                continue

            other_rest: str = next_node[0]
            if other_rest.startswith(rest):
                yield matched + other_rest

            return

        for _, value in self.__prefixes(prefix, node):
            yield value
