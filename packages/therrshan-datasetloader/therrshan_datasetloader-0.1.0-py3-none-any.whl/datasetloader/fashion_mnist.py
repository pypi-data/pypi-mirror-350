from .mnist import UByteLoader

class FashionMNISTLoader(UByteLoader):
    def __init__(self, **kwargs):
        super().__init__(data_dir="data/fashion_mnist", **kwargs)
