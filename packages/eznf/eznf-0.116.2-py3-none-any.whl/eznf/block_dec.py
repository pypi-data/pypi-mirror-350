from eznf import modeler
import math


def encode_npo(N: int, encoder=None, ivars=None, verbose=False):
    """
    Implements the square-root decomposition encoding for the No-Partial-Overlap (NPO) property
    as described in the paper. Uses O(N^(8/3)) clauses.
    
    Args:
        N: The size of the universe
        verbose: Whether to print progress information
    """
    if encoder is None:
        enc = modeler.Modeler()
    else:
        enc = encoder
    
    # Calculate block parameters as per paper
    # n = N^(2/3), b = N^(1/3)
    n = int(math.ceil(N ** (2/3)))
    b = int(math.ceil(N ** (1/3)))
    
    if verbose:
        print(f"Using n={n}, b={b} for N={N}")
        print("Creating variables...")
    
    # Create original x variables
    
    if ivars is None:
        ivars = {}
        for i in range(N):
            for l in range(1, N - i + 1):
                enc.add_var(f"x_{i}_{l}")
                ivars[(i, l)] = f"x_{i}_{l}"
                
            
    # Create auxiliary variables
    # y_L,R variables
    for L in range(1, n + 1):
        for R in range(L, n + 1):
            enc.add_var(f"y_{L}_{R}")
            
    # e_i,R variables
    for i in range(N):
        for R in range(math.ceil((i+1)/b), n + 1):
            enc.add_var(f"e_{i}_{R}")
            
    # s_L,j variables
    for L in range(1, n + 1):
        for j in range(b * (L - 1), N):
            enc.add_var(f"s_{L}_{j}")
            
    if verbose:
        print("Adding constraints...")
        
    # Constraint (1): Link x variables to y variables
    for i in range(N):
        for l in range(b, N - i + 1):
            L = 1 + math.ceil(i/b)
            R = math.floor((i + l)/b) # 0,1 2,3, 4,5
            if L <= R:
                if (i, l) not in ivars:
                    continue
                enc.add_clause(["-" + ivars[(i, l)], f"y_{L}_{R}"])
            
    # Constraint (2): Link x variables to e variables
    for i in range(N):
        for l in range(1, N - i + 1):
            R = math.ceil((i + l)/b)
            if (i, l) not in ivars:
                continue
            enc.add_clause(["-" + ivars[(i, l)], f"e_{i}_{R}"])
            
    # Constraint (3): Link x variables to s variables
    for i in range(N):
        for l in range(1, N - i + 1):
            L = math.ceil((i+1)/b)
            if (i, l) not in ivars:
                continue
            enc.add_clause(["-" + ivars[(i, l)], f"s_{L}_{i+l-1}"])
            
    # Constraint (4): Block overlap based on block sequences
    for L1 in range(1, n + 1):
        for R1 in range(L1, n + 1):
            for L2 in range(L1 + 1, R1 + 1):
                for R2 in range(R1 + 1, n + 1):
                    enc.add_clause([f"-y_{L1}_{R1}", f"-y_{L2}_{R2}"])
                    
                    
    # Overlap := i1 i2 j1 j2
                    
    # Constraint (5): Handle intervals that start in the same block and end in the same block
    for i in range(1, n+1):
        block1_start = (i-1) * b
        block1_end = min(i*b -1, N-1)
        for j in range(i, n+1):
            block2_start = (j-1) * b
            block2_end = min(j*b -1, N-1)
            for i1 in range(block1_start, block1_end+1):
                for i2 in range(i1+1, block1_end+1):
                    for j1 in range(max(block2_start, i2), block2_end+1):
                        for j2 in range(j1+1, block2_end+1):
                            if (i1, i2-i1+1) not in ivars or (j1, j2-j1+1) not in ivars:
                                continue
                            enc.add_clause(["-" + ivars[(i1, i2-i1+1)], "-" + ivars[(j1, j2-j1+1)]])
        
        
                            
    # Constraint (6): Mixed case with e variables
    for i1 in range(N):
        block1 = math.ceil((i1+1)/b)
        for i2 in range(i1 + 1, min(block1*b -1, N)):
            for R1 in range(block1, n + 1):
                for R2 in range(R1 + 1, n + 1):
                    enc.add_clause([f"-e_{i1}_{R1}", f"-e_{i2}_{R2}"])
                        
    # Mixed case with s variables
    for L1 in range(1, n + 1):
        for L2 in range(L1 + 1, n + 1):
            for b3 in range(L2, n + 1):
                block_start = (b3-1) * b
                block_end = min(b3*b -1, N-1)
                for j1 in range(block_start, block_end+1):
                    for j2 in range(j1+1, block_end+1):
                        enc.add_clause([f"-s_{L1}_{j1}", f"-s_{L2}_{j2}"])

    
    if verbose:
        print("Encoding complete")
    
    return enc

def decode(model, N):
    """Decodes a solution into a list of intervals."""
    intervals = []
    for i in range(N):
        for l in range(1, N - i + 1):
            if model[f"x_{i}_{l}"]:
                print(f"Interval: [{i}, {i + l - 1}]")
                intervals.append((i, i + l - 1))
    return intervals

def main():
    # Example usage
    N = 16  # As in paper example
    enc = encode_npo(N, verbose=True)
    enc.at_most_k([f"x_{i}_{l}" for i in range(N) for l in range(1, N - i + 1)], 10)
    enc.at_least_k([f"x_{i}_{l}" for i in range(N) for l in range(1, N - i + 1)], 10)
    
    
    enc.solve_and_decode(lambda model: decode(model, N))
    
    # if solution:
    #     print("Found solution with intervals:", solution)
    # else:
    #     print("No solution found")

if __name__ == "__main__":
    main()