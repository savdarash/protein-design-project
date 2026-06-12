import pytest

from src.mutation_generator import (
    apply_mutation,
    generate_random_candidates,
    generate_single_mutation_candidate,
)


def test_apply_requested_mutation():
    assert apply_mutation("ACDE", "C2V") == "AVDE"


def test_apply_requested_mutation_rejects_wrong_original():
    with pytest.raises(ValueError, match="expects A"):
        apply_mutation("ACDE", "A2V")


def test_generate_random_candidates_are_valid_unique_mutants():
    candidates = generate_random_candidates(
        sequence="ACDEFG",
        num_candidates=4,
        mutations_per_candidate=2,
        random_seed=1,
    )

    sequences = [candidate["sequence"] for candidate in candidates]

    assert len(sequences) == 4
    assert len(set(sequences)) == 4
    assert all(len(sequence) == 6 for sequence in sequences)
    assert all(sequence != "ACDEFG" for sequence in sequences)


def test_generate_single_mutation_candidate_header():
    candidate = generate_single_mutation_candidate("ACDE", "C2V")

    assert candidate["sequence"] == "AVDE"
    assert "mode=single" in candidate["header"]
