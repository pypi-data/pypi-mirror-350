import pytest
from orco.core import assign_spin_probs

def make_equal_stats():
    """
    Build a stats dict where ALA and GLY have identical backbone stats.
    """
    common = {'N': (1.0, 1.0), 'CA': (2.0, 1.0), 'CO': (3.0, 1.0)}
    return {
        ('ALA', ''): common,
        ('GLY', ''): common,
    }

def test_single_residue_probability():
    # If there's only one residue in stats, it should get probability 1.0
    stats = {('ALA', ''): {'N': (1.0, 1.0), 'CA': (2.0, 1.0), 'CO': (3.0, 1.0)}}
    spin = {'N': 1.0, 'CA': 2.0, 'CO': 3.0, 'CX': []}
    probs = assign_spin_probs(spin, stats)
    assert probs == {'A': 1.0}

def test_two_equal_residues_split_evenly():
    # ALA and GLY have identical stats, so both should get ~0.5
    stats = make_equal_stats()
    spin = {'N': 1.0, 'CA': 2.0, 'CO': 3.0, 'CX': []}
    probs = assign_spin_probs(spin, stats)
    assert pytest.approx(probs['A'], rel=1e-6) == 0.5
    assert pytest.approx(probs['G'], rel=1e-6) == 0.5

def test_missing_mandatory_atom_returns_empty():
    # If any of N/CA/CO is sentinel, we bail out and return {}
    stats = make_equal_stats()
    spin = {'N': 1e6, 'CA': 2.0, 'CO': 3.0, 'CX': []}
    probs = assign_spin_probs(spin, stats)
    assert probs == {}

def test_with_one_sidechain_dimension():
    # Add a single CX value and matching stats; still splits evenly
    stats = {
        ('ALA',''): {'N': (1.0,1.0), 'CA': (2.0,1.0), 'CO': (3.0,1.0), 'CB': (4.0,1.0)},
        ('GLY',''): {'N': (1.0,1.0), 'CA': (2.0,1.0), 'CO': (3.0,1.0), 'CB': (4.0,1.0)},
    }
    spin = {'N': 1.0, 'CA': 2.0, 'CO': 3.0, 'CX': [4.0]}
    probs = assign_spin_probs(spin, stats)
    assert pytest.approx(probs['A'], rel=1e-6) == 0.5
    assert pytest.approx(probs['G'], rel=1e-6) == 0.5
