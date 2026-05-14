import os
import requests
from pathlib import Path

from src.protein_design.fasta_parser import parse_fasta


API_URL = "https://api-inference.huggingface.co/models/facebook/esmfold_v1"


def predict_structure(sequence: str, hf_token: str) -> bytes:
    headers = {"Authorization": f"Bearer {hf_token}"}

    response = requests.post(
        API_URL,
        headers=headers,
        json={"inputs": sequence},
        timeout=300,
    )

    if response.status_code != 200:
        raise RuntimeError(
            f"Prediction failed: {response.status_code}\n{response.text}"
        )

    return response.content


if __name__ == "__main__":
    hf_token = os.getenv("HF_TOKEN")

    if not hf_token:
        raise ValueError("Missing HF_TOKEN. Set it before running this script.")

    proteins = parse_fasta("data/raw/proteins.fasta")

    first_valid = next(p for p in proteins if p["is_valid"])

    sequence = first_valid["sequence"]
    protein_name = first_valid["header"].split()[0].replace("|", "_")

    output_dir = Path("results/structures")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / f"{protein_name}.pdb"

    print(f"Predicting structure for: {protein_name}")
    print(f"Sequence length: {len(sequence)}")

    pdb_content = predict_structure(sequence, hf_token)

    with open(output_path, "wb") as f:
        f.write(pdb_content)

    print(f"Saved PDB to {output_path}")