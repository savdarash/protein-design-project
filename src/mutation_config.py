from dataclasses import dataclass
from pathlib import Path

from src.sequence_io import clean_sequence, validate_sequence


@dataclass
class MutationConfig:
    """
    Configuration for a sequence-only mutation generator run.
    """

    protein_name: str
    sequence: str
    mutation_mode: str = "auto"
    num_candidates: int = 10
    mutations_per_candidate: int = 1
    requested_mutation: str | None = None
    random_seed: int = 7
    scored_candidates_dir: str = "results/scored_candidates"
    visualizations_dir: str = "results/visualizations"

    def validate(self):
        self.sequence = clean_sequence(self.sequence)

        if not validate_sequence(self.sequence):
            raise ValueError(
                "Protein sequence must contain only valid amino acids: "
                "A C D E F G H I K L M N P Q R S T V W Y."
            )

        if self.mutation_mode not in {"auto", "single"}:
            raise ValueError("mutation_mode must be 'auto' or 'single'.")

        if self.num_candidates < 1:
            raise ValueError("num_candidates must be at least 1.")

        if self.mutations_per_candidate < 1:
            raise ValueError("mutations_per_candidate must be at least 1.")

        if self.mutations_per_candidate > len(self.sequence):
            raise ValueError("mutations_per_candidate cannot exceed sequence length.")

        if self.mutation_mode == "single" and not self.requested_mutation:
            raise ValueError("requested_mutation is required when mutation_mode is 'single'.")

        Path(self.scored_candidates_dir).mkdir(parents=True, exist_ok=True)
        Path(self.visualizations_dir).mkdir(parents=True, exist_ok=True)

        return True
