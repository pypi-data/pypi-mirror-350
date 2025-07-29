#!/usr/bin/python3

import itertools
import sys
from typing import cast, Any, Generator


class Solution:
    basename: str

    def __init__(self) -> None:
        self.basename: str = sys.argv[0][:-3]

    def load(
        self,
        splitlines: bool = False,
        splitrecords: str | None = None,
        recordtype: list | tuple | type | None = None,
        *,
        lut: dict[str | None, Any] | None = None,
    ) -> list[str | int | list] | Any:
        variant: str = sys.argv[1] if len(sys.argv) > 1 else ""
        content: Any
        if lut:
            lut_content = lut[variant if variant else None]
            if not isinstance(lut_content, str):
                return lut_content
            content = cast(str, lut_content)
        else:
            fname: str = self.basename + variant + ".input"
            with open(fname, "r") as f:
                content = f.read()
        if splitlines:
            content = content.splitlines()
            if splitrecords is not None:
                for i, row in enumerate(content):
                    if splitrecords == "":
                        content[i] = list(row)
                    else:
                        content[i] = row.split(splitrecords)
                    if recordtype is not None:
                        content[i] = self.convert_records(content[i], recordtype)
            elif recordtype is not None:
                content = self.convert_records(content, recordtype)
        elif splitrecords is not None:
            content = content.splitlines()
            if splitrecords == "":
                content = list(content[0])
            else:
                content = content[0].split(splitrecords)
            if recordtype is not None:
                content = self.convert_records(content, recordtype)
        return content

    def variant(self) -> str | None:
        return sys.argv[1] if len(sys.argv) > 1 else None

    def convert_records(self, content, recordtype: list | tuple | type) -> list:
        if callable(recordtype):
            return [recordtype(e) for e in content]
        if type(recordtype) in (list, tuple):
            lastfunc: type | bool | None = False
            newcontent: list = []
            for data, func in itertools.zip_longest(content, recordtype):
                if func is None:
                    func = lastfunc
                else:
                    lastfunc = func
                newcontent.append(func(data))
        return newcontent

    def solve_more(self) -> Generator[int | str, None, None]:
        i: int = 1
        while hasattr(self, f"part{i}"):
            method = getattr(self, f"part{i}")
            yield method()
            i += 1

    def print_condensed(self, data: list[list[int | str]]):
        for row in data:
            print(*row, sep="")

    def print_csv(self, data: list[list[int | str]]):
        for row in data:
            print(*row, sep=",")

    def print_arranged(self, data: list[list[int | str]]):
        col_widths: list[int] = []
        for r, row in enumerate(data):
            for c, value in enumerate(row):
                data_width = len(str(value))
                if c >= len(col_widths):
                    col_widths.append(data_width)
                elif data_width > col_widths[c]:
                    col_widths[c] = data_width
        for r, row in enumerate(data):
            for c, value in enumerate(row):
                if c:
                    print(" ", end="")
                if type(value) == int:
                    print(str(value).rjust(col_widths[c]), end="")
                else:
                    print(str(value).ljust(col_widths[c]), end="")
            print("")

    def main(self) -> None:
        for i, result in enumerate(self.solve_more(), 1):
            print(f"{i}: {result}")
