from pathlib import Path
import pandas as pd

from src.amino_acid_properties import describe_amino_acid_change
from src.sequence_io import parse_fasta_sequences
from src.mutation_parser import find_mutations
from src.mutation_heatmap import extract_score_from_header


def create_candidate_summary(fasta_path: str, output_path: str):

    sequences = parse_fasta_sequences(fasta_path)

    original_sequence = sequences[0]["sequence"]
    candidate_items = sequences[1:]

    rows = []

    for i, candidate in enumerate(candidate_items, start=1):

        candidate_sequence = candidate["sequence"]

        mutations = find_mutations(
            original_sequence,
            candidate_sequence,
        )

        mutation_interpretations = []

        for mutation in mutations:

            original_aa = mutation[0]
            candidate_aa = mutation[-1]

            interpretation = describe_amino_acid_change(
                original_aa,
                candidate_aa,
            )

            mutation_interpretations.append(
                f"{mutation}: {interpretation}"
            )

        score = extract_score_from_header(candidate["header"])

        rows.append({
            "candidate_id": i,
            "score": score,
            "num_mutations": len(mutations),
            "mutations": ", ".join(mutations),
            "mutation_interpretations": " | ".join(mutation_interpretations),
            "sequence": candidate_sequence,
        })

    summary_df = pd.DataFrame(rows)

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    summary_df.to_csv(output_path, index=False)

    print(f"Saved candidate summary to: {output_path}")

    return summary_df


if __name__ == "__main__":

    create_candidate_summary(
        fasta_path="results/scored_candidates/sandbox_candidates.fasta",
        output_path="results/scored_candidates/sandbox_candidate_summary.csv",
    )
