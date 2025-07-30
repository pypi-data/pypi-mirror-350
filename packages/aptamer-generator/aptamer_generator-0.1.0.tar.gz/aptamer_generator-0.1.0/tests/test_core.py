import pytest
from aptamer_generator import AptamerGenerator

@pytest.fixture
def generator():
    """Provides a generator with fixed seed for reproducible tests."""
    return AptamerGenerator(seed=42)

def test_generation_basic(generator):
    seqs = generator.generate_candidates(num=5, length=30)
    
    # Test quantity
    assert len(seqs) == 5
    
    # Test length
    assert all(len(s) == 30 for s in seqs)
    
    # Test valid characters
    valid_chars = {'A', 'T', 'C', 'G'}
    assert all(set(s).issubset(valid_chars) for s in seqs)

def test_gc_constraints(generator):
    seqs = generator.generate_candidates(gc_range=(0.5, 0.6))
    
    for seq in seqs:
        gc = (seq.count('G') + seq.count('C')) / len(seq)
        assert 0.5 <= gc <= 0.6

def test_reproducibility():
    gen1 = AptamerGenerator(seed=42)
    gen2 = AptamerGenerator(seed=42)
    
    assert gen1.generate_candidates() == gen2.generate_candidates()
