import os
from typing import Optional, Iterable, List

import ccdc.search
import pandas as pd


def _convert_temp(temp: str) -> Optional[float]:
    if temp is None:
        return None

    fix = 0
    if 'deg.C' in temp:
        fix = 273.15

    return float(''.join(c for c in temp if c.isdigit() or c == '.' or c == '-')) + fix


def _convert_r_factor(r_factor: float) -> float:
    return round(r_factor / 100, 2)


def _round_measurements(measurements: Iterable[float], digits: Optional[int]) -> List[float]:
    if digits is None:
        return list(measurements)
    return [round(m, digits) for m in measurements]


def search_with_con(con_path: str, max_r_factor: float,
                    no_disorder: bool = True,
                    no_metals: bool = True,
                    no_errors: bool = True,
                    round_measurements: Optional[int] = None) -> pd.DataFrame:
    con_substructure = ccdc.search.ConnserSubstructure(con_path)

    substructure_search = ccdc.search.SubstructureSearch()
    substructure_search.add_substructure(con_substructure)

    substructure_search.settings.max_r_factor = max_r_factor
    substructure_search.settings.no_disorder = no_disorder
    substructure_search.settings.no_metals = no_metals
    substructure_search.settings.no_errors = no_errors

    hits = substructure_search.search()

    data = [[h.entry.chemical_name,
             _convert_r_factor(h.entry.r_factor),
             _convert_temp(h.entry.temperature),
             h.entry.radiation_source,
             *_round_measurements(h.measurements.values(), round_measurements)] for h in hits]
    index = [h.identifier + f'_{i}' for i, h in enumerate(hits)]
    columns = ["chemical_name", "r_factor", "temperature", "method", *hits[0].measurements.keys()]

    df = pd.DataFrame(data, index=index, columns=columns)
    df.index.name = 'id'
    return df


QUERIES_PATH = "data/search_queries/"
RESULTS_PATH = "data/search_results/"

if __name__ == '__main__':
    for path in os.listdir(QUERIES_PATH):
        if path.endswith(".con"):
            # r_factor is passed as percentage here
            # '< 0.1' is fair resolution, '< 0.09' is average, '< 0.07' is good
            query_results = search_with_con(QUERIES_PATH + path, max_r_factor=10, round_measurements=2)
            query_results.to_csv(RESULTS_PATH + path.replace(".con", ".csv"))
