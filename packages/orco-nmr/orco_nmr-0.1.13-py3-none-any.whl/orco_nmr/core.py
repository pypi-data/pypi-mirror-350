import math
from itertools import permutations

# ——————————— Configuration ———————————
SENTINEL      = 1e6
MANDATORY     = ("N", "CA", "CO")
OPTIONAL_DIMS = ("CB", "CG", "CD", "CE", "CGG", "CD1", "CD2", "CE1", "CE2")
CHI2_THRESH   = {
    3:  7.81,
    4:  9.49,
    5: 11.07,
    6: 12.59,
    7: 14.07,
}

# 1-letter ↔ 3-letter maps
ONE_TO_THREE = {
    "A": "ALA", "R": "ARG", "N": "ASN", "D": "ASP", "C": "CYS",
    "Q": "GLN", "E": "GLU", "G": "GLY", "H": "HIS", "I": "ILE",
    "L": "LEU", "K": "LYS", "M": "MET", "F": "PHE", "P": "PRO",
    "S": "SER", "T": "THR", "W": "TRP", "Y": "TYR", "V": "VAL",
}
THREE_TO_ONE = {v: k for k, v in ONE_TO_THREE.items()}


def assign_spin(spin, stats):
    """
    Prints a SS‐aware table (Res | Total | Coil | Helix | Sheet).
    Unchanged from before—only assign_spin_probs is used by tests.
    """
    extras = [x for x in spin.get("CX", []) if x != SENTINEL]
    m = len(extras)

    if any(spin[d] == SENTINEL for d in MANDATORY):
        print("ERROR: must supply N, CA and CO.")
        return

    if m > 4:
        extras = extras[:4]
        m = 4

    total_dims = 3 + m
    if total_dims not in CHI2_THRESH:
        print(f"ERROR: dims must be between 3 and 7 (you provided {total_dims}).")
        return

    χ2 = CHI2_THRESH[total_dims]

    results_debug = []
    for (res3, ss), ref in stats.items():
        # must have all backbone dims
        if not all(d in ref for d in MANDATORY):
            continue

        # drop any sentinel sidechains
        available = [d for d in OPTIONAL_DIMS if d in ref]
        real_extras = [x for x in spin.get("CX", []) if x != SENTINEL]
        m_real = len(real_extras)
        if m_real > len(available):
            continue

        best_ll = best_d2 = None
        best_dims = None

        # build dims list for each combo
        for combo in permutations(available, m_real):
            ll = d2 = 0.0
            try:
                # backbone dims
                for d in MANDATORY:
                    x = spin[d]
                    μ, σ = ref[d]
                    z = (x - μ) / σ
                    d2 += z*z
                    ll += -0.5*z*z - math.log(σ) - 0.5*math.log(2*math.pi)
                # sidechain dims
                for i, d in enumerate(combo):
                    x = real_extras[i]
                    μ, σ = ref[d]
                    z = (x - μ) / σ
                    d2 += z*z
                    ll += -0.5*z*z - math.log(σ) - 0.5*math.log(2*math.pi)
            except Exception:
                continue

            if best_ll is None or ll > best_ll:
                best_ll, best_d2, best_dims = ll, d2, combo

        if best_ll is not None:
            results_debug.append(((res3, ss), best_d2, best_ll, best_dims))

    # filter by χ² threshold
    kept = [((r, ss), ll) for ((r, ss), d2, ll, _) in results_debug if d2 <= χ2]
    if not kept:
        print("No candidates within threshold.\n\n🧠 Closest matches:")
        for (res, ss), d2, ll, dims in sorted(results_debug, key=lambda x: x[1])[:5]:
            print(f"{res:>4} {ss:>6} | d² = {d2:6.2f} | logL = {ll:8.2f} | dims = {dims}")
        return

    # softmax over {res,ss}
    M_ll = max(ll for (_, _), ll in kept)
    cloud = { (r, ss): math.exp(ll - M_ll) for (r, ss), ll in kept }
    Z = sum(cloud.values())

    # aggregate by residue & SS breakdown
    residue_tot = {}
    ss_break = {}
    for (r, ss), v in cloud.items():
        p = v / Z
        residue_tot[r] = residue_tot.get(r, 0.0) + p
        ss_break.setdefault(r, {})[ss] = ss_break[r].get(ss, 0.0) + p

    print(f"{'Res':4} {'Total':>6} {'Coil':>6} {'Helix':>6} {'Sheet':>6}")
    for r, tot in sorted(residue_tot.items(), key=lambda kv: -kv[1]):
        coil  = ss_break[r].get("Coil",  0.0)
        helix = ss_break[r].get("Helix", 0.0)
        sheet = ss_break[r].get("Sheet", 0.0)
        print(f"{r:4} {tot:6.4f} {coil:6.4f} {helix:6.4f} {sheet:6.4f}")


def assign_spin_probs(spin, stats):
    """
    Returns {1‐letter residue: probability} soft‐probabilities
    using only log‐likelihood + softmax. No SS breakdown or printing.
    """
    # drop sentinel extras
    extras = [x for x in spin.get("CX", []) if x != SENTINEL]
    if any(spin[d] == SENTINEL for d in MANDATORY):
        return {}

    # build dims list: backbone + real extras
    dims = list(MANDATORY)
    for i, x in enumerate(extras):
        dims.append(OPTIONAL_DIMS[i])

    # verify dims count for χ² threshold
    K = len(dims)
    if K not in CHI2_THRESH:
        return {}

    results = []
    for (res3, _), ref in stats.items():
        # must have all dims in ref
        if not all(d in ref for d in dims):
            continue

        best_ll = None
        for combo in permutations(dims[3:], len(extras)):  # only permute sidechains
            ll = 0.0
            try:
                for d in dims:
                    x = spin[d] if d in MANDATORY else extras[dims[3:].index(d)]
                    μ, σ = ref[d]
                    z = (x - μ) / σ
                    ll += -0.5*z*z - math.log(σ) - 0.5*math.log(2*math.pi)
            except Exception:
                continue

            if best_ll is None or ll > best_ll:
                best_ll = ll

        if best_ll is not None:
            results.append((res3, best_ll))

    if not results:
        return {}

    M_ll = max(ll for _, ll in results)
    scores = {res3: math.exp(ll - M_ll) for res3, ll in results}
    Z = sum(scores.values())

    return {
        THREE_TO_ONE.get(res3, res3[0]): score / Z
        for res3, score in scores.items()
    }
