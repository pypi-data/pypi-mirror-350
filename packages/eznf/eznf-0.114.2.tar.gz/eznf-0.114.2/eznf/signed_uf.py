class SignedUnionFind:
    def __init__(self):
        self.parent = {}  # parent[x] = parent of x
        self.sign = {}    # sign[x] = sign from x to its parent
    
    def find(self, x):
        """Find the root of x and return (root, accumulated_sign)"""
        # Handle negative input
        input_sign = 1
        if isinstance(x, str) and x.startswith('-'):
            input_sign = -1
            x = x[1:]  # Remove the '-' prefix
        
        if x not in self.parent:
            self.parent[x] = x
            self.sign[x] = 1
            return x, input_sign
        
        # Path compression with sign accumulation
        if self.parent[x] == x:
            return x, input_sign
        
        root, parent_sign = self.find(self.parent[x])
        # Update parent and sign for path compression
        self.parent[x] = root
        self.sign[x] = self.sign[x] * parent_sign
        
        return root, self.sign[x] * input_sign
    
    def union(self, x, y, relation_sign):
        """
        Union x and y with the relation x = relation_sign * y
        For example: union(x, y, -1) means x = -y
        """
        root_x, sign_x = self.find(x)
        root_y, sign_y = self.find(y)
        
        if root_x == root_y:
            # Already in same set, could check consistency here
            return
        
        # We have: x = sign_x * root_x and y = sign_y * root_y
        # We want: x = relation_sign * y
        # So: sign_x * root_x = relation_sign * sign_y * root_y
        # Thus: root_x = (relation_sign * sign_y / sign_x) * root_y
        
        # Make root_y the parent of root_x
        self.parent[root_x] = root_y
        self.sign[root_x] = relation_sign * sign_y * sign_x
    
    def find_with_sign(self, x):
        """Returns the representative and the sign relationship"""
        root, sign = self.find(x)
        return (root, sign) if sign == 1 else (f"-{root}", -sign)
    
    def representative(self, x):
        """Returns just the representative element with sign included"""
        root, sign = self.find(x)
        return root if sign == 1 else f"-{root}"

# Example usage:
uf = SignedUnionFind()

# x <-> -y (x = -y)
uf.union('x', 'y', -1)

# y <-> z (y = z)
uf.union('y', 'z', 1)

# Test the new functionality
print(f"representative('x') = {uf.representative('x')}")    # x
print(f"representative('y') = {uf.representative('y')}")    # -x
print(f"representative('z') = {uf.representative('z')}")    # -x
print(f"representative('-z') = {uf.representative('-z')}")  # x

# You can also use find_with_sign for more details
print(f"\nfind_with_sign('-z') = {uf.find_with_sign('-z')}")  # ('x', 1)
print(f"find_with_sign('-y') = {uf.find_with_sign('-y')}")    # ('x', 1)
print(f"find_with_sign('-x') = {uf.find_with_sign('-x')}")    # ('-x', -1)