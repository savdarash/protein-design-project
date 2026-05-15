import json
from pathlib import Path

from src.redesign_config import RedesignConfig


def generate_fixed_positions(config: RedesignConfig):
    """
    Generates a ProteinMPNN-compatible fixed_positions JSONL file.

    ProteinMPNN expects:
    fixed residues, NOT redesigned residues.

    So:
    - design_positions = residues we ALLOW to mutate
    - everything else becomes fixed
    """

    if config.design_positions is None:
        print("Whole protein redesign selected.")
        return None

    pdb_path = Path(config.pdb_path)

    residues = []

    with open(pdb_path, "r") as file:
        for line in file:

            if line.startswith("ATOM"):

                chain = line[21].strip()

                if chain != config.chain_id:
                    continue

                residue_number = int(line[22:26].strip())

                if residue_number not in residues:
                    residues.append(residue_number)

    fixed_positions = [
        residue
        for residue in residues
        if residue not in config.design_positions
    ]

    output_dir = Path("configs")
    output_dir.mkdir(exist_ok=True)

    output_path = output_dir / f"{config.protein_name}_fixed_positions.jsonl"

    fixed_dict = {
        config.protein_name: {
            config.chain_id: fixed_positions
        }
    }

    with open(output_path, "w") as file:
        file.write(json.dumps(fixed_dict) + "\n")

    print(f"Saved fixed positions file to: {output_path}")

    return str(output_path)


if __name__ == "__main__":

    config = RedesignConfig(
        protein_name="1crn",
        pdb_path="data/pdbs/1crn.pdb",
        design_positions=[10, 11, 12],
    )

    generate_fixed_positions(config)