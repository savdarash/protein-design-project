from pathlib import Path
from src.protein_design.fasta_parser import parse_fasta

if __name__ == "__main__":
    proteins = parse_fasta("data/raw/proteins.fasta")
    first_valid = next(p for p in proteins if p["is_valid"])

    output_path = Path("data/processed/one_sequence.fasta")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w") as f:
        f.write(f">{first_valid['header']}\n")
        f.write(first_valid["sequence"] + "\n")

    print(f"Saved: {output_path}")
    print(first_valid["header"])
    print(first_valid["sequence"])