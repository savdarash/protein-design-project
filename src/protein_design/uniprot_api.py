import requests
from pathlib import Path

BASE_URL = "https://rest.uniprot.org/uniprotkb"


def fetch_fasta(accession: str) -> str:
    url = f"{BASE_URL}/{accession}.fasta"
    response = requests.get(url)

    if response.status_code != 200:
        raise ValueError(f"Failed to fetch {accession}")

    return response.text


def get_protein_ids(n=20):
    """
    Get n protein accession IDs from UniProt.
    Example: human proteins (reviewed Swiss-Prot entries)
    """
    url = (
        f"{BASE_URL}/search?"
        "query=organism_id:9606 AND reviewed:true"
        f"&format=json&size={n}"
    )

    response = requests.get(url)
    data = response.json()

    ids = [entry["primaryAccession"] for entry in data["results"]]
    return ids


if __name__ == "__main__":
    proteins = get_protein_ids(20)

    output_path = Path("data/raw/proteins.fasta")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w") as f:
        for protein_id in proteins:
            print(f"Downloading {protein_id}")
            fasta = fetch_fasta(protein_id)
            f.write(fasta + "\n")

    print(f"\nSaved {len(proteins)} proteins to {output_path}")