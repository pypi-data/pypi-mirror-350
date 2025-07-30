import numpy as np


class Metric:
    def __init__(self, metrics: dict) -> None:
        self.num_class = metrics["num_class"]
        self.unique_classes = metrics["unique_classes"]

        self.all_ap = metrics["ap"]
        self.ar = metrics["ar"]
        self.tp = metrics["tp"]
        self.fp = metrics["fp"]
        self.fn = metrics["fn"]
        self.p = metrics["p"]
        self.r = metrics["r"]
        self.f1 = metrics["f1"]

    @property
    def ap50(self):
        return self.all_ap[:, 0] if len(self.all_ap) else []

    @property
    def ap75(self):
        return self.all_ap[:, 5] if len(self.all_ap) else []

    @property
    def ap(self):
        return self.all_ap.mean(1) if len(self.all_ap) else []

    @property
    def map50(self):
        return self.all_ap[:, 0].mean() if len(self.all_ap) else 0.0

    @property
    def map75(self):
        return self.all_ap[:, 5].mean() if len(self.all_ap) else 0.0

    @property
    def map(self):
        return self.all_ap.mean() if len(self.all_ap) else 0.0

    @property
    def maps(self):
        maps = np.zeros(self.num_class) + self.map
        for i, c in enumerate(self.ap_class_index):
            maps[c] = self.ap[i]
        return maps

    @property
    def mp(self):
        return self.p.mean() if len(self.p) else 0.0

    @property
    def mr(self):
        return self.r.mean() if len(self.r) else 0.0
