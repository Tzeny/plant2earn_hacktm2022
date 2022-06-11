import json
from functools import singledispatch
from json import JSONEncoder

import numpy as np


@singledispatch
def to_serializable(val):
    """Used by default."""
    return str(val)


@to_serializable.register(np.float32)
def ts_float32(val):
    """Used if *val* is an instance of numpy.float32."""
    return np.float64(val)


@to_serializable.register(np.ndarray)
def ts_ndarray(val):
    return val.tolist()


class SegmentationAnswer:
    def get_json(self):
        return json.dumps(self.__dict__, default=to_serializable).encode('utf8')

    def __init__(self, id, bbox_path, leaf_segmented_path):
        self.answer_type = 1
        self.id = id
        self.bbox_path = bbox_path
        self.leaf_segmented_path = leaf_segmented_path

    def __str__(self):
        return str(self.__dict__)

class TreeDetectionAnswer:
    def get_json(self):
        return json.dumps(self.__dict__, default=to_serializable).encode('utf8')

    def __init__(self, id, bbox_path, coord_om, coord_copac):
        self.answer_type = 2
        self.id = id
        self.bbox_path = bbox_path
        self.coord_om = coord_om
        self.coord_copac = coord_copac

    def __str__(self):
        return str(self.__dict__)
