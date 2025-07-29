import modeler
import argparse
from string_utils import StringQueries
import block_dec


def encode(T: str, verbose=False):
    enc = modeler.Modeler()
    n = len(T)
    S = StringQueries(T)

    if verbose:
        print("Start vars!")
    # f vars
    for i in range(n):
        for l in range(1, n - i + 1):
            enc.add_var(
                f"f_{i}_{l}", f"Whether {T[i:i+l]} is a factor of T in the grammar"
            )

    if verbose:
        print("f vars done")
    # p vars
    for i in range(n + 1):
        enc.add_var(f"p_{i}", f"{i} is the starting position of a factor")

    # ref vars
    for i in range(n):
        for l in range(2, n - i + 1):
            for i_prime in range(max(0, i - l + 1)):
                if S.are_substrings_equal(i_prime, i_prime + l, i, i + l):
                    enc.add_var(
                        f"ref_{i_prime}_{i}_{l}",
                        f"T[{i_prime}..{i_prime + l}] references T[{i}..{i + l}]",
                    )

    if verbose:
        print("ref vars done")

    # q vars
    interval_vars = {}
    for i_prime in range(n - 1):
        for l in range(2, n - i_prime + 2):
            if S.find_substring_after(i_prime, i_prime + l):
                enc.add_var(
                    f"q_{i_prime}_{l}",
                    f"T[{i_prime}..{i_prime + l}] is an internal node",
                )
                interval_vars[(i_prime, l)] = f"q_{i_prime}_{l}"
    if verbose:
        print("vars done")

    # p_1 = p_{n+1} = 1
    enc.add_clause([f"p_{0}"])
    enc.add_clause([f"p_{n}"])

    # Constraint (1)
    for i in range(n):
        for l in range(1, n - i + 1):
            enc.add_clause([f"-f_{i}_{l}", f"p_{i}"])
            for j in range(i + 1, i + l):
                enc.add_clause([f"-f_{i}_{l}", f"-p_{j}"])
            enc.add_clause([f"-f_{i}_{l}", f"p_{i + l}"])

            enc.add_clause(
                [f"-p_{i}"]
                + [f"p_{j}" for j in range(i + 1, i + l)]
                + [f"-p_{i + l}", f"f_{i}_{l}"]
            )
    if verbose:
        print("Constraint 1 done")
    # Constraint (2)
    for i in range(n - 1):
        for l in range(2, n - i + 1):
            if T[i : i + l] not in T[:i]:
                enc.add_clause([f"-f_{i}_{l}"])

    if verbose:
        print("Constraint 2 done")

    # Constraint (3)
    for i in range(n):
        for l in range(2, n - i + 1):
            if T[i : i + l] in T[:i]:
                clause = [f"-f_{i}_{l}"]
                for i_prime in range(i - l + 1):
                    if S.are_substrings_equal(i_prime, i_prime + l, i, i + l):
                        clause.append(f"ref_{i_prime}_{i}_{l}")
                enc.add_clause(clause)
    if verbose:
        print("Constraint 3 done")

    # Constraint (4)
    for i in range(n):
        for l in range(2, n - i + 1):
            refs = [
                f"ref_{i_prime}_{i}_{l}"
                for i_prime in range(i - l + 1)
                if S.are_substrings_equal(i_prime, i_prime + l, i, i + l)
            ]
            if refs:
                enc.at_most_one(refs)

    if verbose:
        print("Constraint 4 done")

    # Constraint (5)
    for i in range(n):
        for l in range(2, n - i + 1):
            for i_prime in range(i - l + 1):
                if S.are_substrings_equal(i_prime, i_prime + l, i, i + l):
                    enc.add_clause([f"-ref_{i_prime}_{i}_{l}", f"f_{i}_{l}"])
    if verbose:
        print("Constraint 5 done")

    # Constraint (6)
    for i_prime in range(n - 1):
        for l in range(2, n - i_prime + 1):
            if S.find_substring_after(i_prime, i_prime + l):
                clause = [f"-q_{i_prime}_{l}"]
                for i in range(i_prime + 1, n - l + 1):
                    if enc.has_var(f"ref_{i_prime}_{i}_{l}"):
                        clause.append(f"ref_{i_prime}_{i}_{l}")
                enc.add_clause(clause)
                enc.add_clause([f"-{ref}" for ref in clause[1:]] + [f"q_{i_prime}_{l}"])
    if verbose:
        print("Constraint 6 done")

    # Constraint (7)
    for i_prime in range(n - 1):
        for l in range(2, n - i_prime + 1):
            if S.find_substring_after(i_prime, i_prime + l):
                enc.add_clause([f"-q_{i_prime}_{l}", f"-f_{i_prime}_{l}"])
                enc.add_clause([f"-q_{i_prime}_{l}", f"p_{i_prime}"])
                enc.add_clause([f"-q_{i_prime}_{l}", f"p_{i_prime + l}"])
    if verbose:
        print("Constraint 7 done")

    print("# Interval vars:", len(interval_vars))
    enc = block_dec.encode_npo(len(T), enc, interval_vars)

    # at most:
    for i in range(1, n):
        enc.add_soft_clause([f"-p_{i}"])


    return enc


def decode(model, word):
    n = len(word)
    factors = []
    for i in range(n):
        for l in range(1, n - i + 1):
            if model[f"f_{i}_{l}"]:
                factors.append(word[i : i + l])
    print(factors)
    return factors



argparser = argparse.ArgumentParser()
argparser.add_argument("-f", "--file", type=str)
args = argparser.parse_args()
with open(args.file, "r", encoding="utf-8") as f:
    word = f.read().strip()
    print("Word:", word)
    print("Length:", len(word))
    
    encoding = encode(word)
    encoding.serialize("maxsat_slp.wcnf")