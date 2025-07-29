import modeler
import argparse
import itertools

argparser = argparse.ArgumentParser()
argparser.add_argument('-n', type=int, required=True, help="Number of vertices")
argparser.add_argument('-m', type=int, required=True, help="Number of edges")
argparser.add_argument('-k', type=int, required=True, help="edge uniformity")
argparser.add_argument('--knf', action='store_true', help="Output in knf format")
args = argparser.parse_args()

def encode(n, m, k, knf):
    enc = modeler.Modeler()
    assert n >= k
    possible_edges = list(itertools.combinations(range(n), k))
    for possible_edge in possible_edges:
        enc.add_var(f"e_{possible_edge}", f"{possible_edge} is a hyperedge")
        enc.add_clause([f"-e_{possible_edge}"])
        
    # enc.add_clause([f"e_{possible_edges[0]}"])
    # enc.add_clause([f"e_{possible_edges[1]}"])
    # enc.add_clause([f"e_{possible_edges[-1]}"])
    
    # if knf:
    #     enc.add_kconstraint(len(possible_edges)-m, [f"-e_{possible_edge}" for possible_edge in possible_edges])
    # else:
    #     enc.exactly_k([enc.v(f"e_{possible_edge}") for possible_edge in possible_edges], m)
        
    bicolorings = list(itertools.product(range(2), repeat=n))
    for bicoloring in bicolorings:
        if bicoloring[0]:
            continue
        clause = []
        for possible_edge in possible_edges:
            if all([bicoloring[vertex] for vertex in possible_edge]):
                clause.append(f"e_{possible_edge}")
            if all([not bicoloring[vertex] for vertex in possible_edge]):
                clause.append(f"e_{possible_edge}")
        enc.add_clause(clause)
    return enc
    
def decode(model, n, m, k):
    edges = []
    possible_edges = list(itertools.combinations(range(n), k))
    for possible_edge in possible_edges:
        if model[f"e_{possible_edge}"]:
            edges.append(possible_edge)
    for edge in edges:
        print(f"Hyperedge: {edge}")

encoding = encode(args.n, args.m, args.k, args.knf)
#encoding.solve_and_decode(lambda model: decode(model, args.n, args.m, args.k), solver="kcadical" if args.knf else "kissat")
encoding.serialize(f"h_{args.n}_{args.m}_{args.k}_{args.knf}.knf")

