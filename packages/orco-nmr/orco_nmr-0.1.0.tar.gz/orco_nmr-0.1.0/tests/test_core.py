import orco
from orco import core, stats, cli

def test_version():
    assert hasattr(orco, "__version__")
    assert isinstance(orco.__version__, str)

def test_import_modules():
    assert callable(core.assign_spin)
    assert callable(core.assign_spin_probs)
    assert callable(stats.load_stats)
    assert callable(cli.main)
