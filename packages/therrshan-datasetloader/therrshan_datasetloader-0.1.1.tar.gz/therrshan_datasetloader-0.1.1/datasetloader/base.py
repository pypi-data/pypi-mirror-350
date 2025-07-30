import numpy as np
import pandas as pd

class DatasetLoader:
    def __init__(self, normalize=False, as_dataframe=False):
        self.normalize = normalize
        self.as_dataframe = as_dataframe

    def _normalize(self, array):
        return array / 255.0 if array.dtype in [np.uint8, np.int32, np.float32, np.float64] else array

    def _to_format(self, X, y=None, feature_columns=None, label_column="label"):
        if self.as_dataframe:
            df_X = pd.DataFrame(X, columns=feature_columns if feature_columns else None)
            if y is not None:
                df_y = pd.DataFrame(y, columns=[label_column])
                return df_X, df_y
            return df_X
        return np.array(X), np.array(y) if y is not None else None
