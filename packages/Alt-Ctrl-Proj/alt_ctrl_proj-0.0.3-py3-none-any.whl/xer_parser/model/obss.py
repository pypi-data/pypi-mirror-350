from xer_parser.model.classes.obs import OBS

__all__ = ["OBSs"]


class OBSs:
    def __init__(self) -> None:
        self.index = 0
        self._obss = []

    def add(self, params):
        self._obss.append(OBS(params))

    def find_by_id(self, id) -> OBS:
        obj = list(filter(lambda x: x.actv_code_type_id == id, self._obss))
        if len(obj) > 0:
            return obj[0]
        return obj

    def get_tsv(self):
        if len(self._obss) > 0:
            tsv = []
            tsv.append(["%T", "OBS"])
            tsv.append(
                [
                    "%F",
                    "obs_id",
                    "parent_obs_id",
                    "guid",
                    "seq_num",
                    "obs_name",
                    "obs_descr",
                ]
            )
            for obs in self._obss:
                tsv.append(obs.get_tsv())
            return tsv
        return []

    @property
    def count(self):
        return len(self._obss)

    def __len__(self) -> int:
        return len(self._obss)

    def __iter__(self) -> "OBSs":
        return self

    def __next__(self) -> OBS:
        if self.index >= len(self._obss):
            raise StopIteration
        idx = self.index
        self.index += 1
        return self._obss[idx]
