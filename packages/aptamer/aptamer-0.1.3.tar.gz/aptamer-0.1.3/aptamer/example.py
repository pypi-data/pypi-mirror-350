from selex import StableAptamerGenerator

generator = StableAptamerGenerator(
        pool_size=100,
        min_len=15,
        max_len=25,
        top_k=30,
        generations=15
)

final_pool = generator.run()

print("\nFinal top aptamers:")
for i, (seq, score) in enumerate(final_pool[:10], 1):
    print(f"{i}: Sequence: {seq} | Length: {len(seq)} | ΔG: {score:.2f}")