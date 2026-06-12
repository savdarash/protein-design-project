from pathlib import Path
import pandas as pd

from src.sequence_io import parse_fasta_sequences


def create_mutation_frequency_table(fasta_path: str, output_path: str):
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
                rows.append({
                    "position": position,
                    "original_aa": original_aa,
                    "candidate_aa": candidate_aa,
                    "mutation": f"{original_aa}{position}{candidate_aa}",
                    "candidate_id": candidate_index,
                })

    mutation_df = pd.DataFrame(
        rows,
        columns=[
            "position",
            "original_aa",
            "candidate_aa",
            "mutation",
            "candidate_id",
        ],
    )

    if mutation_df.empty:
        frequency_df = pd.DataFrame(
            columns=[
                "position",
                "original_aa",
                "candidate_aa",
                "mutation",
                "frequency",
            ]
        )
    else:
        frequency_df = (
            mutation_df
            .groupby(["position", "original_aa", "candidate_aa", "mutation"])
            .size()
            .reset_index(name="frequency")
            .sort_values(["position", "frequency"], ascending=[True, False])
        )

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    frequency_df.to_csv(output_path, index=False)

    print(f"Saved mutation frequency table to: {output_path}")

    return frequency_df


if __name__ == "__main__":
    create_mutation_frequency_table(
        fasta_path="results/scored_candidates/sandbox_candidates.fasta",
        output_path="results/scored_candidates/sandbox_mutation_frequency.csv",
    )
