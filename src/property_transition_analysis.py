from pathlib import Path
import pandas as pd

from src.sequence_io import parse_fasta_sequences
from src.amino_acid_properties import describe_amino_acid_change


def create_property_transition_table(fasta_path: str, output_path: str):
    """
    Creates a table summarizing amino-acid property changes
    across all mutated candidate sequences.
    """

    sequences = parse_fasta_sequences(fasta_path)

    original_sequence = sequences[0]["sequence"]
    candidate_items = sequences[1:]

    rows = []

    for candidate_index, candidate in enumerate(candidate_items, start=1):

        candidate_sequence = candidate["sequence"]

        for position, (original_aa, candidate_aa) in enumerate(
            zip(original_sequence, candidate_sequence),
            start=1,
        ):
            if original_aa != candidate_aa:

                transition = describe_amino_acid_change(
                    original_aa,
                    candidate_aa,
                )

                rows.append({
                    "candidate_id": candidate_index,
                    "position": position,
                    "original_aa": original_aa,
                    "candidate_aa": candidate_aa,
                    "mutation": f"{original_aa}{position}{candidate_aa}",
                    "property_transition": transition,
                })

    transition_df = pd.DataFrame(
        rows,
        columns=[
            "candidate_id",
            "position",
            "original_aa",
            "candidate_aa",
            "mutation",
            "property_transition",
        ],
    )

    if transition_df.empty:
        summary_df = pd.DataFrame(
            columns=["property_transition", "frequency"]
        )
    else:
        summary_df = (
            transition_df
            .groupby("property_transition")
            .size()
            .reset_index(name="frequency")
            .sort_values("frequency", ascending=False)
        )

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    summary_df.to_csv(output_path, index=False)

    print(f"Saved property transition table to: {output_path}")

    return summary_df


if __name__ == "__main__":

    create_property_transition_table(
        fasta_path="results/scored_candidates/demo_candidates.fasta",
        output_path="results/scored_candidates/demo_property_transitions.csv",
    )
