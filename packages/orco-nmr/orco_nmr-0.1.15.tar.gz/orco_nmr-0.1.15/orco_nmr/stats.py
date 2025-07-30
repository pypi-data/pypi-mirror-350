import csv
import math
import importlib.resources

def load_stats(path=None):
    """
    Load RefDB/BMRB-style CSV with columns:
      Residue, SS, Atom, Mean, StdDev
    Returns a nested dictionary:
      { (res3, ss): { atom_id: (μ, σ), ... }, ... }

    If `path` is None, loads the default packaged stats_refdb_bmrb1.csv.
    """
    if path:
        f = open(path, newline="")
    else:
        f = importlib.resources.files("orco_nmr").joinpath("stats_refdb_bmrb1.csv").open("r", encoding="utf-8")

    reader = csv.DictReader(f)
    stats = {}
    for row in reader:
        try:
            μ = float(row["Mean"])
            σ = float(row["StdDev"])
            if σ == 0 or math.isnan(μ) or math.isnan(σ):
                continue
            res = row["Residue"].strip().upper()
            ss  = row["SS"].strip().capitalize()
            atom = row["Atom"].strip().upper()
            stats.setdefault((res, ss), {})[atom] = (μ, σ)
        except (ValueError, KeyError):
            continue
    f.close()
    return stats
