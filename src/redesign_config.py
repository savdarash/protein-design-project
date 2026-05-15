from dataclasses import dataclass
from pathlib import Path


@dataclass
class RedesignConfig:
    """
    Configuration for a protein redesign run.

    design_positions:
        None means redesign the whole protein.
        A list like [10, 11, 12] means redesign only those residue positions.
    """

    protein_name: str
    pdb_path: str
    output_dir: str = "data/mpnn_outputs"
    num_candidates: int = 5
    sampling_temp: str = "0.1"
    chain_id: str = "A"
    design_positions: list[int] | None = None

    def validate(self):
        pdb_path = Path(self.pdb_path)

        if not pdb_path.exists():
            raise FileNotFoundError(f"PDB file not found: {pdb_path}")

        if self.num_candidates < 1:
            raise ValueError("num_candidates must be at least 1.")

        if self.design_positions is not None:
            if len(self.design_positions) == 0:
                self.design_positions = None

            elif any(pos < 1 for pos in self.design_positions):
                raise ValueError("Residue positions must be 1-indexed positive integers.")

        return True

    @property
    def redesign_mode(self):
        if self.design_positions is None:
            return "whole_protein"

        return "targeted_positions"


if __name__ == "__main__":
    config = RedesignConfig(
        protein_name="1crn",
        pdb_path="data/pdbs/1crn.pdb",
        num_candidates=5,
        design_positions=None,
    )

    config.validate()

    print(config)
    print(f"Redesign mode: {config.redesign_mode}")