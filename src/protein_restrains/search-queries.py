import os

import ccdc.search
import pandas as pd


def search_with_con(con_path: str, max_r_factor: float,
                    no_disorder: bool = True,
                    no_metals: bool = True,
                    no_errors: bool = True) -> pd.DataFrame:
    con_substructure = ccdc.search.ConnserSubstructure(con_path)

    substructure_search = ccdc.search.SubstructureSearch()
    substructure_search.add_substructure(con_substructure)

    substructure_search.settings.max_r_factor = max_r_factor
    substructure_search.settings.no_disorder = no_disorder
    substructure_search.settings.no_metals = no_metals
    substructure_search.settings.no_errors = no_errors

    hits = substructure_search.search()

    return pd.DataFrame([h.measurements for h in hits],
                        index=list([h.identifier + f"_{i}" for i, h in enumerate(hits)]))


def enrich_search_results(df: pd.DataFrame, query_name: str) -> pd.DataFrame:
    df.index.name = "name"
    df.insert(0, "data_source", "CSD")
    df.insert(1, "query_name", query_name)
    return df


QUERIES_PATH = "data/search_queries/"
RESULTS_PATH = "data/serach_results/"

if __name__ == '__main__':
    for path in os.listdir(QUERIES_PATH):
        if path.endswith(".con"):
            query_results = search_with_con(QUERIES_PATH + path, max_r_factor=10)
            query_results = enrich_search_results(query_results, path.replace(".con", ""))
            query_results.to_csv(RESULTS_PATH + path.replace(".con", ".csv"))
