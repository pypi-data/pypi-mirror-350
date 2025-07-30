import random
import RNA

class StableAptamerGenerator:
    def __init__(self, pool_size=100, min_len=15, max_len=25, top_k=30, generations=15):
        self.NUCLEOTIDES = ['A', 'T', 'C', 'G']
        self.pool_size = pool_size
        self.min_len = min_len
        self.max_len = max_len
        self.top_k = top_k
        self.generations = generations

    def generate_random_aptamers(self):
        return [
            ''.join(random.choices(self.NUCLEOTIDES, k=random.randint(self.min_len, self.max_len)))
            for _ in range(self.pool_size)
        ]

    def evaluate_aptamer(self, sequence):
        seq = sequence.replace("T", "U")
        # RNAfold is meant for RNA sequences, so we replace T with U, stability is not accurate but gives a good estimate
        _, mfe = RNA.fold(seq)
        return mfe

    # Mutate to create new aptamers so that we dont limit ourselves to inital pool
    def mutate_aptamer(self, aptamer, mutation_rate=0.3, indel_rate=0.1, min_len=15, max_len=25):
        new_seq = []
        for nt in aptamer:
            if random.random() < mutation_rate:
                # Substitute nucleotide without changing length
                new_seq.append(random.choice(self.NUCLEOTIDES))
            else:
                new_seq.append(nt)

            # Deletion only if length > min_len
            if random.random() < indel_rate and len(new_seq) > min_len:
                new_seq.pop()

        # Insertion only if length < max_len
        if random.random() < indel_rate and len(new_seq) < max_len:
            insert_pos = random.randint(0, len(new_seq))
            new_seq.insert(insert_pos, random.choice(self.NUCLEOTIDES))

        return ''.join(new_seq) 

    def run(self):
        # Generate initial pool
        initial_seqs = self.generate_random_aptamers()
        aptamer_pool = [(seq, self.evaluate_aptamer(seq)) for seq in initial_seqs]
        aptamer_pool.sort(key=lambda x: x[1])  # Sort by ΔG (ascending as lower is better)

        for gen in range(self.generations):
            # 0th index is the best aptamer
            best_seq, best_score = aptamer_pool[0]
            print(f"Gen {gen+1}: Best aptamer = {best_seq} | Length = {len(best_seq)} | ΔG = {best_score}")

            # Select top k candidates
            top_aptamers = aptamer_pool[:self.top_k]
            lengths = [len(seq) for seq, _ in top_aptamers]
            # modify min and max lengths based on current pool
            min_len = max(min(lengths) - 1, self.min_len)
            max_len = min(max(lengths) + 1, self.max_len)

            new_aptamers = []
            for _ in range(self.pool_size - self.top_k):
                parent_seq = random.choice(top_aptamers)[0]
                mutant = self.mutate_aptamer(parent_seq, min_len=min_len, max_len=max_len)
                new_aptamers.append((mutant, self.evaluate_aptamer(mutant)))

            # Create new pool and sort
            aptamer_pool = top_aptamers + new_aptamers
            aptamer_pool.sort(key=lambda x: x[1])  # Always keep sorted

        return aptamer_pool
