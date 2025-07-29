from xer_parser.model.classes.rsrcrcat import ResourceCat

__all__ = ["ResourceCategories"]


class ResourceCategories:
    def __init__(self) -> None:
        self.index = 0
        self._rsrccat = []

    def get_tsv(self):
        tsv = []
        if len(self._rsrccat) > 0:
            tsv.append(["%T", "RSRCRCAT"])
            tsv.append(["%F", "rsrc_id", "rsrc_catg_type_id", "rsrc_catg_id"])
            for rc in self._rsrccat:
                tsv.append(rc.get_tsv())
        return tsv

    def add(self, params):
        self._rsrccat.append(ResourceCat(params))

    def find_by_id(self, id) -> ResourceCat:
        obj = list(filter(lambda x: x.actv_code_type_id == id, self._rsrccat))
        if len(obj) > 0:
            return obj[0]
        return obj

    @property
    def count(self):
        return len(self._rsrccat)

    def __len__(self) -> int:
        return len(self._rsrccat)

    def __iter__(self) -> "ResourceCategories":
        return self

    def __next__(self) -> ResourceCat:
        if self.index >= len(self._rsrccat):
            raise StopIteration
        idx = self.index
        self.index += 1
        return self._rsrccat[idx]
