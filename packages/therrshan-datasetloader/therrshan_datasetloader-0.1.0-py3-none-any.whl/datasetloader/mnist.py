import os
import struct
import numpy as np
from .base import DatasetLoader

class UByteLoader(DatasetLoader):
    def __init__(self, data_dir, **kwargs):
        super().__init__(**kwargs)
        self.data_dir = data_dir

    def _read_images(self, path):
        with open(path, 'rb') as f:
            magic, num, rows, cols = struct.unpack(">IIII", f.read(16))
            data = np.frombuffer(f.read(), dtype=np.uint8).reshape(num, rows * cols)
        return data

    def _read_labels(self, path):
        with open(path, 'rb') as f:
            magic, num = struct.unpack(">II", f.read(8))
            labels = np.frombuffer(f.read(), dtype=np.uint8)
        return labels

    def load(self, split="train"):
        image_file = "train-images.idx3-ubyte" if split == "train" else "t10k-images.idx3-ubyte"
        label_file = "train-labels.idx1-ubyte" if split == "train" else "t10k-labels.idx1-ubyte"

        X = self._read_images(os.path.join(self.data_dir, image_file))
        y = self._read_labels(os.path.join(self.data_dir, label_file))

        if self.normalize:
            X = self._normalize(X)

        return self._to_format(X, y)

class MNISTLoader(UByteLoader):
    def __init__(self, **kwargs):
        super().__init__(data_dir="data/mnist", **kwargs)
