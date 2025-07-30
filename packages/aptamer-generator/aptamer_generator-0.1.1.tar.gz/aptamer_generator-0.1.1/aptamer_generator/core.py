import numpy as np
from Bio.SeqUtils import gc_fraction

class AptamerGenerator:
    """
    Generates DNA aptamer candidates with controlled GC content.
    
    Parameters:
    seed : int, optional
        Seed for reproducible random number generation
    """
    
    def __init__(self, seed=None):
        self.rng = np.random.default_rng(seed)
        self.nucleotides = ['A', 'T', 'C', 'G']
        
    def generate_candidates(self, num=10, length=40, gc_range=(0.4, 0.6)):
        """
        Generate DNA sequences meeting GC content constraints.
        
        Args:
            num (int): Number of sequences to generate
            length (int): Length of each sequence
            gc_range (tuple): (min_gc, max_gc) as fractions (0.0-1.0)
            
        Returns:
            list: Valid DNA sequences
        """
        candidates = []
        
        for _ in range(num):
            while True:
                # Generate random sequence
                seq = ''.join(self.rng.choice(self.nucleotides, size=length))
                
                # Calculate GC content
                gc = gc_fraction(seq)
                
                if gc_range[0] <= gc <= gc_range[1]:
                    candidates.append(seq)
                    break
                    
        return candidates


