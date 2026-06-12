from pathlib import Path


VALID_AMINO_ACIDS = set("ACDEFGHIKLMNPQRSTVWY")


def clean_sequence(sequence: str) -> str:
    return "".join(sequence.split()).upper()


def validate_sequence(sequence: str) -> bool:
    sequence = clean_sequence(sequence)
    return len(sequence) > 0 and all(aa in VALID_AMINO_ACIDS for aa in sequence)


def parse_fasta_sequences(fasta_path: str | Path):
    """
    Parse FASTA records into dictionaries with header and sequence keys.
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
                if current_header is not None:
                    sequences.append({
                        "header": current_header,
                        "sequence": clean_sequence("".join(current_sequence)),
                    })

                current_header = line[1:]
                current_sequence = []
            else:
                current_sequence.append(line)

    if current_header is not None:
        sequences.append({
            "header": current_header,
            "sequence": clean_sequence("".join(current_sequence)),
        })

    return sequences


def write_fasta(records, output_path: str | Path):
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w") as file:
        for record in records:
            file.write(f">{record['header']}\n")
            file.write(f"{clean_sequence(record['sequence'])}\n")

    return output_path
