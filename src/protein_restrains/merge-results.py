import os

import pandas as pd

RESULTS_PATH = 'data/serach_results/'

if __name__ == '__main__':
    dfs = [pd.read_csv(RESULTS_PATH + path, index_col=0) for path in os.listdir(RESULTS_PATH) if path.endswith('.csv')]
    merged = pd.concat(dfs)
    merged.to_csv(RESULTS_PATH + 'merged_results.csv', mode='x')
