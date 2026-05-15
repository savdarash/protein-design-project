import subprocess
from pathlib import Path
from src.redesign_config import RedesignConfig
from src.fixed_position_generator import generate_fixed_positions
from src.parse_mpnn_output import parse_fasta_sequences
from src.mutation_heatmap import build_mutation_matrix, plot_mutation_heatmap, extract_score_from_header


def run_proteinmpnn(config: RedesignConfig):
    """
    Runs ProteinMPNN using our RedesignConfig.
    """

    config.validate()

    proteinmpnn_script = Path("external/ProteinMPNN/protein_mpnn_run.py")

    if not proteinmpnn_script.exists():
        raise FileNotFoundError(
            "ProteinMPNN script not found. Expected external/ProteinMPNN/protein_mpnn_run.py"
        )

    output_dir = Path(config.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    fixed_positions_path = generate_fixed_positions(config)
    command = [
        "python",
        str(proteinmpnn_script),
        "--pdb_path",
        config.pdb_path,
        "--out_folder",
        config.output_dir,
        "--num_seq_per_target",
        str(config.num_candidates),
        "--sampling_temp",
        config.sampling_temp,
    ]
    if fixed_positions_path is not None:
    	command.extend([
        	"--fixed_positions_jsonl",
        	fixed_positions_path,
    ])
    print("Running redesign pipeline")
    print(f"Mode: {config.redesign_mode}")
    print(" ".join(command))

    subprocess.run(command, check=True)

    return output_dir

def create_pipeline_outputs(config: RedesignConfig):
    """
    Parses ProteinMPNN outputs and creates mutation heatmap.
    """

    fasta_path = Path(config.output_dir) / "seqs" / f"{config.protein_name}.fa"

    sequences = parse_fasta_sequences(fasta_path)

    original_sequence = sequences[0]["sequence"]
    candidate_items = sequences[1:]

    candidate_sequences = [item["sequence"] for item in candidate_items]

    matrix = build_mutation_matrix(
        original_sequence=original_sequence,
        candidate_sequences=candidate_sequences,
    )

    candidate_labels = []

    for i, item in enumerate(candidate_items, start=1):
        score = extract_score_from_header(item["header"])
        num_mutations = int(matrix.iloc[i - 1].sum())
        candidate_labels.append(f"Candidate {i} | score={score} | muts={num_mutations}")

    plot_mutation_heatmap(
        matrix=matrix,
        candidate_labels=candidate_labels,
        output_path=f"outputs/visualizations/{config.protein_name}_mutation_heatmap.png",
    )

    print("Pipeline outputs created.")

if __name__ == "__main__":
    config = RedesignConfig(
        protein_name="1crn",
        pdb_path="data/pdbs/1crn.pdb",
        output_dir="data/mpnn_outputs",
        num_candidates=5,
        sampling_temp="0.1",
        design_positions=[10, 11, 12],
    )

    run_proteinmpnn(config)
    create_pipeline_outputs(config)