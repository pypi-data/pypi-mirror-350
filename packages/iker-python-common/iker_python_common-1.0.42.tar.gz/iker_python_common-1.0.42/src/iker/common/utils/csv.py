import os
from collections.abc import Callable, Generator, Iterable, Mapping, Sequence
from typing import Any

__all__ = [
    "CSVColumn",
    "CSVView",
    "column",
    "view",
]


class CSVColumn(object):
    def __init__(
        self,
        name: str,
        loader: Callable[[str], Any] = str,
        dumper: Callable[[Any], str] = str,
        null_str: str = "",
    ):
        self.name = name
        self.loader = loader
        self.dumper = dumper
        self.null_str = null_str


class CSVView(object):
    def __init__(self, schema: Sequence[CSVColumn], *, row_delim: str = "\n", col_delim: str = ","):
        self.schema = schema
        self.row_delim = row_delim
        self.col_delim = col_delim

    def load_lines(
        self,
        lines: Iterable[str],
        has_header: bool = True,
        ret_dict: bool = False,
    ) -> Generator[list[Any] | dict[str, Any], None, None]:
        rows_iter = iter(lines)
        if has_header:
            header_row = next(rows_iter)
            header_cols = header_row.split(self.col_delim)
            if len(self.schema) != len(header_cols):
                raise ValueError("size of the schema is not identical to size of the columns")
            for c, header_col in zip(self.schema, header_cols):
                if c.name != header_col:
                    raise ValueError("name of the schema is not equal to the name of the columns")
        for row in rows_iter:
            cols = row.split(self.col_delim)
            if len(self.schema) != len(cols):
                continue
            if ret_dict:
                yield {c.name: None if col == c.null_str else c.loader(col) for c, col in zip(self.schema, cols)}
            else:
                yield [None if col == c.null_str else c.loader(col) for c, col in zip(self.schema, cols)]

    def dump_lines(
        self,
        data: Iterable[Sequence[Any] | Mapping[str, Any]],
        has_header: bool = True,
    ) -> Generator[str, None, None]:
        if has_header:
            yield self.col_delim.join(c.name for c in self.schema)
        for cols in data:
            if isinstance(cols, Sequence):
                if len(self.schema) != len(cols):
                    raise ValueError("size of the schema is not identical to size of the columns")
                yield self.col_delim.join(c.null_str if col is None else c.dumper(col)
                                          for c, col in zip(self.schema, cols))
            if isinstance(cols, Mapping):
                yield self.col_delim.join(c.null_str if cols.get(c.name) is None else c.dumper(cols.get(c.name))
                                          for c in self.schema)

    def load_file(
        self,
        file_path: os.PathLike | str,
        has_header: bool = True,
        ret_dict: bool = False,
        **kwargs,
    ) -> Generator[list[Any] | dict[str, Any], None, None]:
        with open(file_path, mode="r", **kwargs) as fh:
            lines = fh.read().split(self.row_delim)
            yield from self.load_lines(lines, has_header, ret_dict)

    def dump_file(
        self,
        data: Iterable[Sequence[Any] | Mapping[str, Any]],
        file_path: os.PathLike | str,
        has_header: bool = True,
        **kwargs,
    ) -> None:
        with open(file_path, mode="w", **kwargs) as fh:
            for line in self.dump_lines(data, has_header):
                fh.write(line)
                fh.write(self.row_delim)


column = CSVColumn
view = CSVView
