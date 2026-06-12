import random
import re

from src.sequence_io import VALID_AMINO_ACIDS, clean_sequence


MUTATION_PATTERN = re.compile(r"^([ACDEFGHIKLMNPQRSTVWY])([1-9][0-9]*)([ACDEFGHIKLMNPQRSTVWY])$")


def parse_mutation_label(mutation_label: str):
    mutation_label = clean_sequence(mutation_label)
    match = MUTATION_PATTERN.match(mutation_label)

    if not match:
        raise ValueError("Mutation must use format A10V: original amino acid, 1-indexed position, new amino acid.")

    original_aa, position, candidate_aa = match.groups()
    return original_aa, int(position), candidate_aa


def apply_mutation(sequence: str, mutation_label: str):
    sequence = clean_sequence(sequence)
    original_aa, position, candidate_aa = parse_mutation_label(mutation_label)

    if position > len(sequence):
        raise ValueError(f"Mutation position {position} exceeds sequence length {len(sequence)}.")

    current_aa = sequence[position - 1]

    if current_aa != original_aa:
        raise ValueError(
            f"Requested mutation expects {original_aa} at position {position}, "
            f"but sequence contains {current_aa}."
        )

    if original_aa == candidate_aa:
        raise ValueError("Requested mutation must change the amino acid.")

    return sequence[:position - 1] + candidate_aa + sequence[position:]


def generate_random_candidates(
    sequence: str,
    num_candidates: int,
    mutations_per_candidate: int = 1,
    random_seed: int = 7,
):
    sequence = clean_sequence(sequence)
    rng = random.Random(random_seed)
    amino_acids = sorted(VALID_AMINO_ACIDS)
    candidates = []
    seen_sequences = set()
    max_attempts = max(num_candidates * 50, 100)
    attempts = 0

    while len(candidates) < num_candidates and attempts < max_attempts:
        attempts += 1
        candidate = list(sequence)
        positions = rng.sample(range(len(sequence)), mutations_per_candidate)
        mutation_labels = []

        for position in sorted(positions):
            original_aa = candidate[position]
            choices = [aa for aa in amino_acids if aa != original_aa]
            candidate_aa = rng.choice(choices)
            candidate[position] = candidate_aa
            mutation_labels.append(f"{original_aa}{position + 1}{candidate_aa}")

        candidate_sequence = "".join(candidate)

        if candidate_sequence in seen_sequences:
            continue

        seen_sequences.add(candidate_sequence)
        candidates.append({
            "header": (
                f"candidate={len(candidates) + 1}, mode=auto, "
                f"mutations={';'.join(mutation_labels)}"
            ),
            "sequence": candidate_sequence,
        })

    if len(candidates) < num_candidates:
        raise RuntimeError("Could not generate the requested number of unique candidates.")

    return candidates


def generate_single_mutation_candidate(sequence: str, mutation_label: str):
    candidate_sequence = apply_mutation(sequence, mutation_label)

    return {
        "header": f"candidate=1, mode=single, mutation={clean_sequence(mutation_label)}",
        "sequence": candidate_sequence,
    }
