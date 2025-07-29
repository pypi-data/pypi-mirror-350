class StringQueries:
    def __init__(self, T):
        """
        Initialize the class with string T and precompute hashes
        Using rolling hash with prime modulo to avoid collisions
        """
        self.T = T
        self.n = len(T)
        self.p = 31  # prime number for hash calculation
        self.m = 10**9 + 9  # large prime modulo
        
        # Precompute powers of p
        self.p_pow = [1] * (self.n + 1)
        for i in range(1, self.n + 1):
            self.p_pow[i] = (self.p_pow[i-1] * self.p) % self.m
        
        # Precompute prefix hashes
        self.prefix_hash = [0] * (self.n + 1)
        for i in range(self.n):
            self.prefix_hash[i + 1] = (self.prefix_hash[i] + 
                                     ord(self.T[i]) * self.p_pow[i]) % self.m
                                     
        self.MEMO = {}
    
    def get_substring_hash(self, start, end):
        """Calculate hash of T[start:end]"""
        curr_hash = (self.prefix_hash[end] - self.prefix_hash[start]) % self.m
        return (curr_hash * pow(self.p_pow[start], self.m - 2, self.m)) % self.m
    
    def are_substrings_equal(self, i1, j1, i2, j2):
        """
        Check if T[i1:j1] == T[i2:j2]
        First check lengths, then compare hashes
        """
        if j1 - i1 != j2 - i2:
            return False
        
        # For very short strings, direct comparison might be faster
        if j1 - i1 <= 3:
            return self.T[i1:j1] == self.T[i2:j2]
            
        return self.get_substring_hash(i1, j1) == self.get_substring_hash(i2, j2)
    
    def find_substring_after(self, i1, j1):
        """
        Check if T[i1:j1] appears in T[j1:]
        Returns True if found, False otherwise
        Using rolling hash for efficient search
        """
        if j1 >= self.n:
            return False
            
        pattern_len = j1 - i1
        if pattern_len == 0:
            return True
            
        if (i1, j1) in self.MEMO:
            return self.MEMO[(i1, j1)]
        
        # Get hash of the pattern we're looking for
        pattern_hash = self.get_substring_hash(i1, j1)
        
        # Check each possible position after j1
        for i in range(j1, self.n - pattern_len + 1):
            curr_hash = self.get_substring_hash(i, i + pattern_len)
            if curr_hash == pattern_hash:
                # Double check with actual string comparison to handle any hash collisions
                if self.T[i:i + pattern_len] == self.T[i1:j1]:
                    self.MEMO[(i1, j1)] = True
                    return True
        self.MEMO[(i1, j1)] = False
        return False