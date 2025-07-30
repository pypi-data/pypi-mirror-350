from orco.stats import load_stats
from orco.core import assign_spin, SENTINEL

def main():
    stats = load_stats()  # uses bundled stats_refdb_bmrb1.csv
    prompt = "Enter N CA CO CX1 CX2 CX3 CX4 [more optional CX…] (blank to quit): "
    while True:
        line = input(prompt).strip()
        if not line:
            print("Goodbye.")
            return

        toks = line.split()
        vals = []
        for t in toks[:7]:
            try:
                vals.append(float(t))
            except:
                vals.append(SENTINEL)
        # pad/truncate to exactly 7 values
        vals = (vals + [SENTINEL]*7)[:7]

        spin = {
            "N": vals[0],
            "CA": vals[1],
            "CO": vals[2],
            "CX": vals[3:7],
        }

        assign_spin(spin, stats)

        again = input("\nAssign another? [Y/n]: ").strip().lower()
        if again and not again.startswith("y"):
            print("Done.")
            return
