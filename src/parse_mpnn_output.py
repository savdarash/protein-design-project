from pathlib import Path


def parse_fasta_sequences(fasta_path: str):
    """
    Parses ProteinMPNN FASTA output.

    Returns:
        List of dictionaries containing:
        - header
        - sequence
    """

    fasta_path = Path(fasta_path)

    if not fasta_path.exists():
        raise FileNotFoundError(f"File not found: {fasta_path}")

    sequences = []

    current_header = None
    current_sequence = []

    with open(fasta_path, "r") as file:
        for line in file:
            line = line.strip()

            if not line:
                continue

            if line.startswith(">"):

                # save previous sequence
                if current_header is not None:
                    sequences.append({
                        "header": current_header,
                        "sequence": "".join(current_sequence)
                    })

                current_header = line[1:]
                current_sequence = []

            else:
                current_sequence.append(line)

        # save final sequence
        if current_header is not None:
            sequences.append({
                "header": current_header,
                "sequence": "".join(current_sequence)
            })

    return sequences


if __name__ == "__main__":

    fasta_file = "data/mpnn_outputs/seqs/1crn.fa"

    sequences = parse_fasta_sequences(fasta_file)

    for i, seq_data in enumerate(sequences):

        print(f"\nSequence {i}")
        print("-" * 50)
        print(seq_data["header"])
        print(seq_data["sequence"])