from pathlib import Path
import requests

from src.protein_design.fasta_parser import validate_sequence


def fetch_from_alphafold(uniprot_id: str, output_dir: Path):
    """
    Download a structure file from AlphaFold DB.

    Tries multiple AlphaFold file versions and both PDB/mmCIF formats.
    Returns the saved file path if successful, otherwise None.
    """

    uniprot_id = uniprot_id.strip().upper()

    possible_urls = []

    for version in ["v6", "v5", "v4", "v3", "v2", "v1"]:
        possible_urls.extend([
            f"https://alphafold.ebi.ac.uk/files/AF-{uniprot_id}-F1-model_{version}.pdb",
            f"https://alphafold.ebi.ac.uk/files/AF-{uniprot_id}-F1-model_{version}.cif",
            f"https://www.alphafold.ebi.ac.uk/files/AF-{uniprot_id}-F1-model_{version}.pdb",
            f"https://www.alphafold.ebi.ac.uk/files/AF-{uniprot_id}-F1-model_{version}.cif",
        ])

    for url in possible_urls:
        print(f"Trying: {url}")
        response = requests.get(url, timeout=60)

        if response.status_code == 200:
            suffix = ".cif" if url.endswith(".cif") else ".pdb"
            output_path = output_dir / f"{uniprot_id}{suffix}"

            with open(output_path, "wb") as f:
                f.write(response.content)

            print(f"\nDownloaded structure from:\n{url}")
            return output_path

    return None


def predict_structure(sequence=None, uniprot_id=None):
    output_dir = Path("results/alphafold")
    output_dir.mkdir(parents=True, exist_ok=True)

    if uniprot_id:
        result_path = fetch_from_alphafold(uniprot_id, output_dir)

        if result_path:
            print("\nUsed AlphaFold DB")
            return result_path

    if sequence:
        if not validate_sequence(sequence):
            raise ValueError("Invalid amino acid sequence")

    raise ValueError(
        "No structure found in AlphaFold DB.\n"
        "Live ColabFold / ESMFold prediction is not connected yet."
    )


if __name__ == "__main__":
    print("\n=== Protein Structure Pipeline ===\n")

    sequence = input(
        "Enter amino acid sequence (optional, press Enter to skip):\n"
    ).strip().upper()

    uniprot_id = input(
        "\nEnter UniProt ID. For demo, use Q8I3H7:\n"
    ).strip().upper()

    if sequence == "":
        sequence = None

    if uniprot_id == "":
        uniprot_id = None

    result = predict_structure(
        sequence=sequence,
        uniprot_id=uniprot_id
    )

    print(f"\nSaved structure to:\n{result}")