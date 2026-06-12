import argparse
from pathlib import Path

from src.candidate_summary import create_candidate_summary
from src.mutation_config import MutationConfig
from src.mutation_frequency import create_mutation_frequency_table
from src.mutation_generator import (
    generate_random_candidates,
    generate_single_mutation_candidate,
)
from src.mutation_heatmap import build_mutation_matrix, plot_mutation_heatmap
from src.property_transition_analysis import create_property_transition_table
from src.sequence_io import write_fasta


def build_candidate_records(config: MutationConfig):
    config.validate()

    records = [{
        "header": f"{config.protein_name} original",
        "sequence": config.sequence,
    }]

    if config.mutation_mode == "single":
        records.append(
            generate_single_mutation_candidate(
                config.sequence,
                config.requested_mutation,
            )
        )
    else:
        records.extend(
            generate_random_candidates(
                sequence=config.sequence,
                num_candidates=config.num_candidates,
                mutations_per_candidate=config.mutations_per_candidate,
                random_seed=config.random_seed,
            )
        )

    return records


def run_mutation_pipeline(config: MutationConfig):
    """
    Generate mutation candidates from a protein sequence and analyze them.
    """

    records = build_candidate_records(config)
    protein_name = config.protein_name
    scored_dir = Path(config.scored_candidates_dir)
    visualizations_dir = Path(config.visualizations_dir)

    fasta_path = scored_dir / f"{protein_name}_candidates.fasta"
    write_fasta(records, fasta_path)

    original_sequence = records[0]["sequence"]
    candidate_records = records[1:]
    candidate_sequences = [record["sequence"] for record in candidate_records]

    matrix = build_mutation_matrix(original_sequence, candidate_sequences)
    candidate_labels = [
        f"Candidate {index} | muts={int(matrix.iloc[index - 1].sum())}"
        for index in range(1, len(candidate_records) + 1)
    ]

    heatmap_path = visualizations_dir / f"{protein_name}_mutation_heatmap.png"
    plot_mutation_heatmap(
        matrix=matrix,
        candidate_labels=candidate_labels,
        output_path=heatmap_path,
    )

    summary_path = scored_dir / f"{protein_name}_candidate_summary.csv"
    frequency_path = scored_dir / f"{protein_name}_mutation_frequency.csv"
    transitions_path = scored_dir / f"{protein_name}_property_transitions.csv"

    create_candidate_summary(fasta_path=str(fasta_path), output_path=str(summary_path))
    create_mutation_frequency_table(fasta_path=str(fasta_path), output_path=str(frequency_path))
    create_property_transition_table(fasta_path=str(fasta_path), output_path=str(transitions_path))

    return {
        "fasta": fasta_path,
        "candidate_summary": summary_path,
        "mutation_frequency": frequency_path,
        "property_transitions": transitions_path,
        "heatmap": heatmap_path,
    }


def parse_args():
    parser = argparse.ArgumentParser(description="Protein Mutation Sandbox pipeline")
    parser.add_argument("--protein-name", default="sandbox")
    parser.add_argument("--sequence", required=True)
    parser.add_argument("--mode", choices=["auto", "single"], default="auto")
    parser.add_argument("--num-candidates", type=int, default=10)
    parser.add_argument("--mutations-per-candidate", type=int, default=1)
    parser.add_argument("--mutation", dest="requested_mutation")
    parser.add_argument("--seed", type=int, default=7)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    outputs = run_mutation_pipeline(
        MutationConfig(
            protein_name=args.protein_name,
            sequence=args.sequence,
            mutation_mode=args.mode,
            num_candidates=args.num_candidates,
            mutations_per_candidate=args.mutations_per_candidate,
            requested_mutation=args.requested_mutation,
            random_seed=args.seed,
        )
    )

    print("Mutation pipeline complete.")
    for name, path in outputs.items():
        print(f"{name}: {path}")
