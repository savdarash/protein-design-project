from pathlib import Path
import json

VALID_AMINO_ACIDS = set("ACDEFGHIKLMNPQRSTVWY")


def clean_sequence(sequence: str) -> str:
    return "".join(sequence.split()).upper()


def validate_sequence(sequence: str) -> bool:
    sequence = clean_sequence(sequence)
    return len(sequence) > 0 and all(aa in VALID_AMINO_ACIDS for aa in sequence)


def parse_fasta(file_path: str):
    records = []
    current_header = None
    current_sequence = []

    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()

            if not line:
                continue

            if line.startswith(">"):
                if current_header is not None:
                    sequence = clean_sequence("".join(current_sequence))
                    records.append({
                        "header": current_header,
                        "sequence": sequence,
                        "length": len(sequence),
                        "is_valid": validate_sequence(sequence),
                    })

                current_header = line[1:]
                current_sequence = []
            else:
                current_sequence.append(line)

    if current_header is not None:
        sequence = clean_sequence("".join(current_sequence))
        records.append({
            "header": current_header,
            "sequence": sequence,
            "length": len(sequence),
            "is_valid": validate_sequence(sequence),
        })

    return records


if __name__ == "__main__":
    fasta_path = "data/raw/proteins.fasta"
    proteins = parse_fasta(fasta_path)

    print(f"Parsed {len(proteins)} proteins")

    for protein in proteins:
        print(
            protein["header"].split()[0],
            protein["length"],
            protein["is_valid"]
        )
    output_path = Path("data/processed/parsed_proteins.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w") as f:
        json.dump(proteins, f, indent=2)

    print(f"Saved parsed proteins to {output_path}")