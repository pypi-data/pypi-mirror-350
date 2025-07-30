import os
from .base import DatasetLoader

class TwentyNewsLoader(DatasetLoader):
    def __init__(self, data_dir="data/20ng", **kwargs):
        super().__init__(**kwargs)
        self.data_dir = data_dir

    def load(self, split="train"):
        split_path = os.path.join(self.data_dir, split)
        texts, labels = [], []

        for label in sorted(os.listdir(split_path)):
            class_path = os.path.join(split_path, label)
            if not os.path.isdir(class_path):
                continue
            for fname in os.listdir(class_path):
                file_path = os.path.join(class_path, fname)
                try:
                    with open(file_path, encoding="latin1") as f:
                        texts.append(f.read())
                        labels.append(label)
                except Exception as e:
                    print(f"Skipping {file_path}: {e}")

        return self._to_format(texts, labels, feature_columns=["text"], label_column="topic")
