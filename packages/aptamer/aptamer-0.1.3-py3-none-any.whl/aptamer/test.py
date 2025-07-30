import pytest
from selex import StableAptamerGenerator

def test_generate_random_aptamers():
    gen = StableAptamerGenerator(pool_size=10, min_len=8, max_len=8)
    pool = gen.generate_random_aptamers()
    assert len(pool) == 10
    for aptamer in pool:
        assert len(aptamer) == 8
        assert all(nt in gen.NUCLEOTIDES for nt in aptamer)

def test_mutate_aptamer_length_and_content():
    gen = StableAptamerGenerator()
    original = "AAAAAA"
    mutated = gen.mutate_aptamer(original, mutation_rate=1.0, indel_rate=0.5)
    assert all(nt in gen.NUCLEOTIDES for nt in mutated)
    assert mutated != original
    assert 5 <= len(mutated) <= 7  # considering possible deletion or insertion

def test_run_returns_sorted_pool():
    gen = StableAptamerGenerator(pool_size=20, top_k=5, generations=2, min_len=10, max_len=10)
    final_pool = gen.run()
    assert isinstance(final_pool, list)
    assert all(isinstance(item, tuple) and len(item) == 2 for item in final_pool)
    assert all(isinstance(item[1], float) for item in final_pool)
    # Check if sorted by ΔG ascending
    for i in range(1, len(final_pool)):
        assert final_pool[i - 1][1] <= final_pool[i][1]
