from typing import Any

from xer_parser.model.classes.rcattype import RCatType

__all__ = ["RCatTypes"]


class RCatTypes:
    def __init__(self) -> None:
        self.index: int = 0
        self._rcattypes: list[RCatType] = []

    def add(self, params: dict[str, Any]) -> None:
        self._rcattypes.append(RCatType(params))

    def get_tsv(self) -> list[list[str | int | None]]:
        if len(self._rcattypes) > 0:
            tsv: list[list[str | int | None]] = []
            tsv.append(["%T", "RCATTYPE"])
            tsv.append(
                [
                    "%F",
                    "rsrc_catg_type_id",
                    "seq_num",
                    "rsrc_catg_short_len",
                    "rsrc_catg_type",
                ]
            )
            for rcat in self._rcattypes:
                tsv.append(rcat.get_tsv())
            return tsv
        return []

    def find_by_id(self, id: int) -> RCatType | list[RCatType]:
        obj = [
            x for x in self._rcattypes if getattr(x, "rsrc_catg_type_id", None) == id
        ]
        if len(obj) > 0:
            return obj[0]
        return obj

    @property
    def count(self) -> int:
        return len(self._rcattypes)

    def __len__(self) -> int:
        return len(self._rcattypes)

    def __iter__(self) -> "RCatTypes":
        return self

    def __next__(self) -> RCatType:
        if self.index >= len(self._rcattypes):
            raise StopIteration
        idx = self.index
        self.index += 1
        return self._rcattypes[idx]
