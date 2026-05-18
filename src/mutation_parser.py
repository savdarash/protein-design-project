def find_mutations(original_sequence: str, candidate_sequence: str):
    """
    Compare original and candidate protein sequences.

    Returns mutation labels like:
    T10V = original T at position 10 changed to V.
    """

    if len(original_sequence) != len(candidate_sequence):
        raise ValueError("Sequences must be the same length.")

    mutations = []

    for position, (original_aa, candidate_aa) in enumerate(
        zip(original_sequence, candidate_sequence),
        start=1,
    ):
        if original_aa != candidate_aa:
            mutations.append(f"{original_aa}{position}{candidate_aa}")

    return mutations


if __name__ == "__main__":
    original = "TTCCPSIVARSNFNVCRLPGTPEAICATYTGCIIIPGATCPGDYAN"
    candidate = "TVCCPSEEAKKKYEECLKDGTPKEECAKATGCIIIEGTECPEDYPY"

    print(find_mutations(original, candidate))