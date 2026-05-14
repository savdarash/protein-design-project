from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

from src.parse_mpnn_output import parse_fasta_sequences


def build_mutation_matrix(original_sequence, candidate_sequences):
    """
    Builds a binary mutation matrix.

    0 = same as original
    1 = mutated compared to original
    """

    rows = []

    for candidate_sequence in candidate_sequences:
        row = []

        for original_aa, candidate_aa in zip(original_sequence, candidate_sequence):
            if original_aa == candidate_aa:
                row.append(0)
            else:
                row.append(1)

        rows.append(row)

    columns = [
        f"{aa}{position}"
        for position, aa in enumerate(original_sequence, start=1)
    ]

    return pd.DataFrame(rows, columns=columns)


def plot_mutation_heatmap(
    matrix,
    candidate_labels,
    output_path="outputs/visualizations/mutation_heatmap.png",
):
    """
    Creates and saves a mutation heatmap.

    Columns show original amino acid + residue position.
    Rows show ProteinMPNN candidate sequences.
    """

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(18, 5))

    plt.imshow(matrix, aspect="auto")

    plt.xlabel("Original residue and position")
    plt.ylabel("ProteinMPNN candidate")
    plt.title("ProteinMPNN Mutation Heatmap")

    plt.xticks(
        ticks=range(len(matrix.columns)),
        labels=matrix.columns,
        rotation=90,
        fontsize=8,
    )

    plt.yticks(
        ticks=range(len(candidate_labels)),
        labels=candidate_labels,
    )

    plt.colorbar(label="0 = unchanged, 1 = mutated")

    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close()

    print(f"Saved heatmap to: {output_path}")


def extract_score_from_header(header):
    """
    Pulls the ProteinMPNN score from a FASTA header.

    Example header:
    T=0.1, sample=1, score=0.7497, global_score=0.7497
    """

    parts = header.split(",")

    for part in parts:
        part = part.strip()

        if part.startswith("score="):
            return part.replace("score=", "")

    return "NA"


if __name__ == "__main__":
    fasta_file = "data/mpnn_outputs/seqs/1crn.fa"

    sequences = parse_fasta_sequences(fasta_file)

    original_sequence = sequences[0]["sequence"]
    candidate_items = sequences[1:]

    candidate_sequences = [
        item["sequence"]
        for item in candidate_items
    ]

    matrix = build_mutation_matrix(
        original_sequence=original_sequence,
        candidate_sequences=candidate_sequences,
    )

    candidate_labels = []

    for i, item in enumerate(candidate_items, start=1):
        score = extract_score_from_header(item["header"])
        num_mutations = int(matrix.iloc[i - 1].sum())

        candidate_labels.append(
            f"Candidate {i} | score={score} | muts={num_mutations}"
        )

    plot_mutation_heatmap(
        matrix=matrix,
        candidate_labels=candidate_labels,
    )