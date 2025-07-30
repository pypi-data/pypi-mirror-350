import csv
import math
import importlib.resources

def load_stats(path=None):
    """
    Load a RefDB/BMRB‐style CSV with columns:
      Residue, SS, Atom, Mean, StdDev
    Returns a dict { (res3, ss): { atom_id: (μ, σ), …}, … }.
    """
    if path:
        f = open(path, newline="")
    else:
        f = importlib.resources.open_text(__package__, "stats_refdb_bmrb1.csv")

    reader = csv.DictReader(f)
    stats = {}
    for row in reader:
        try:
            μ = float(row["Mean"])
            σ = float(row["StdDev"])
            if σ == 0 or math.isnan(μ) or math.isnan(σ):
                continue
            res = row["Residue"]
            ss  = row["SS"]
            atom= row["Atom"]
            stats.setdefault((res, ss), {})[atom] = (μ, σ)
        except (ValueError, KeyError):
            continue

    f.close()
    return stats
