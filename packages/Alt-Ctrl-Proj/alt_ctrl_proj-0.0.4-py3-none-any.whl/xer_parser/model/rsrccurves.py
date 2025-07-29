from xer_parser.model.classes.rsrccurv import ResourceCurve

__all__ = ["ResourceCurves"]


class ResourceCurves:
    def __init__(self) -> None:
        self.index = 0
        self._resourcecurves = []

    def add(self, params):
        self._resourcecurves.append(ResourceCurve(params))

    def find_by_id(self, id) -> ResourceCurve:
        obj = list(filter(lambda x: x.actv_code_type_id == id, self._resourcecurves))
        if len(obj) > 0:
            return obj[0]
        return obj

    def get_tsv(self):
        tsv = []
        if len(self._resourcecurves) > 0:
            tsv.append(["%T", "RSRCCURVDATA"])
            tsv.append(
                [
                    "%F",
                    "curv_id",
                    "curv_name",
                    "default_flag",
                    "pct_usage_0",
                    "pct_usage_1",
                    "pct_usage_2",
                    "pct_usage_3",
                    "pct_usage_4",
                    "pct_usage_5",
                    "pct_usage_6",
                    "pct_usage_7",
                    "pct_usage_8",
                    "pct_usage_9",
                    "pct_usage_10",
                    "pct_usage_11",
                    "pct_usage_12",
                    "pct_usage_13",
                    "pct_usage_14",
                    "pct_usage_15",
                    "pct_usage_16",
                    "pct_usage_17",
                    "pct_usage_18",
                    "pct_usage_19",
                    "pct_usage_20",
                ]
            )
            for rcurv in self._resourcecurves:
                tsv.append(rcurv.get_tsv())
        return tsv

    @property
    def count(self):
        return len(self._resourcecurves)

    def __len__(self) -> int:
        return len(self._resourcecurves)

    def __iter__(self) -> "ResourceCurves":
        return self

    def __next__(self) -> ResourceCurve:
        if self.index >= len(self._resourcecurves):
            raise StopIteration
        idx = self.index
        self.index += 1
        return self._resourcecurves[idx]
