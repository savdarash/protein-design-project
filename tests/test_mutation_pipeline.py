from src.mutation_config import MutationConfig
from src.mutation_pipeline import run_mutation_pipeline


def test_run_mutation_pipeline_writes_expected_outputs(tmp_path):
    outputs = run_mutation_pipeline(
        MutationConfig(
            protein_name="test_protein",
            sequence="ACDEFGHIK",
            mutation_mode="auto",
            num_candidates=3,
            mutations_per_candidate=1,
            random_seed=2,
            scored_candidates_dir=str(tmp_path / "scored_candidates"),
            visualizations_dir=str(tmp_path / "visualizations"),
        )
    )

    for output_path in outputs.values():
        assert output_path.exists()

    assert outputs["fasta"].read_text().startswith(">test_protein original")
