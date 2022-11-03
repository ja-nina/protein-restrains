import numpy as np
import pandas as pd
from scipy.stats import stats


def mad_mask(df: pd.DataFrame, column: str, threshold: float):
    med = np.median(df[column])
    mad = np.abs(stats.median_abs_deviation(df[column]))
    return (df[column] - med) / mad < threshold


def remove_outliers(df: pd.DataFrame, column: str, mad_threshold=3.0):
    return df[mad_mask(df, column, mad_threshold)]


def get_outliers(df: pd.DataFrame, column: str, mad_threshold=3.0):
    return df[np.logical_not(mad_mask(df, column, mad_threshold))]


if __name__ == '__main__':
    df = pd.read_csv("data/search_results/leucine_3single_long_pdb_names.csv")
    df = get_outliers(df, "CA-CB")
    print(df)
