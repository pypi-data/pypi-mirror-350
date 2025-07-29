import modeler
import itertools
import random
import networkx as nx
import matplotlib.pyplot as plt

def encode(G):
    enc = modeler.Modeler()
    for i in range(len(G)):
        enc.add_var(f"x_{i}")
        
    for triple in itertools.combinations(range(len(G)), 3):
        i, j, k = triple
        if G[i][j] and G[j][k] and G[i][k]:
            enc.add_clause([f"x_{i}", f"x_{j}", f"x_{k}"])
        if not G[i][j] and not G[j][k] and not G[i][k]:
            enc.add_clause([f"-x_{i}", f"-x_{j}", f"-x_{k}"])
        
    return enc


def random_graph(n, p):
    adj = [[False for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            if random.random() < p:
                adj[i][j] = True
                adj[j][i] = True
    return adj
                
def decode(model):
    n = len(model)
    ans = []
    for i in range(n):
        if model[f"x_{i}"]:
            ans.append(i)
    # print(ans)
    return ans
            
                
graphs = [random_graph(100, 0.5) for _ in range(10)]

uns = 0
for graph in graphs:
    encoding = encode(graph)
    ans = encoding.solve()
    
    if ans.is_UNSAT():
        # print("UNSAT")
        # print(graph)
        uns += 1
        print(f"unsat percentage: {uns} / {len(graphs)}")
        
        # # Convert adjacency matrix to NetworkX graph
        # G_nx = nx.Graph()
        # for i in range(len(graph)):
        #     G_nx.add_node(i)
        # for i in range(len(graph)):
        #     for j in range(i+1, len(graph)):
        #         if graph[i][j]:
        #             G_nx.add_edge(i, j)

        # # Plot the graph
        # plt.figure(figsize=(10, 8))
        # pos = nx.circular_layout(G_nx)
        # nx.draw(G_nx, pos, with_labels=True, node_color='lightblue', 
        #         node_size=500, edge_color='gray', width=1, alpha=0.7)
        # plt.title("UNSAT Graph Visualization")
        # plt.savefig("unsat_graph.png")
        # plt.show()
        # break
    
# encoding.serialize(f"formulas/clique-is-k-6.cnf")
