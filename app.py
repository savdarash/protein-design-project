from pathlib import Path
import re

import pandas as pd
import streamlit as st

from src.mutation_config import MutationConfig
from src.mutation_pipeline import run_mutation_pipeline
from src.sequence_io import VALID_AMINO_ACIDS, clean_sequence, validate_sequence


DEMO_SEQUENCE = "TTCCPSIVARSNFNVCRLPGTPEAICATYTGCIIIPGATCPGDYAN"


def safe_name(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9_-]+", "_", value)
    return value.strip("_") or "demo"


def parse_uploaded_fasta(uploaded_file):
    if uploaded_file is None:
        return None, ""

    text = uploaded_file.getvalue().decode("utf-8")
    header = uploaded_file.name.rsplit(".", 1)[0]
    sequence_lines = []

    for line in text.splitlines():
        line = line.strip()

        if not line:
            continue

        if line.startswith(">"):
            if not sequence_lines:
                header = line[1:].strip().split()[0] or header
            continue

        sequence_lines.append(line)

    return header, clean_sequence("".join(sequence_lines))


def invalid_characters(sequence: str):
    return sorted(set(clean_sequence(sequence)) - VALID_AMINO_ACIDS)


def download_button(label: str, path: Path, mime: str):
    with open(path, "rb") as file:
        st.download_button(
            label=label,
            data=file,
            file_name=path.name,
            mime=mime,
            use_container_width=True,
        )


st.set_page_config(
    page_title="Protein Mutation Generator",
    page_icon="PM",
    layout="wide",
)

st.title("Protein Mutation Generator")

uploaded_file = st.file_uploader("FASTA file", type=["fa", "fasta", "txt"])
uploaded_name, uploaded_sequence = parse_uploaded_fasta(uploaded_file)

default_name = safe_name(uploaded_name) if uploaded_name else "demo"
protein_name = st.text_input("Protein name", value=default_name)

sequence_input = st.text_area(
    "Protein sequence",
    value=uploaded_sequence or DEMO_SEQUENCE,
    height=160,
)

sequence = clean_sequence(sequence_input)
is_valid = validate_sequence(sequence)
bad_chars = invalid_characters(sequence)

metric_a, metric_b, metric_c = st.columns(3)
metric_a.metric("Length", len(sequence))
metric_b.metric("Status", "Valid" if is_valid else "Invalid")
metric_c.metric("Invalid characters", ", ".join(bad_chars) if bad_chars else "None")

left, right = st.columns([1, 1])

with left:
    mode_label = st.radio(
        "Mutation mode",
        ["Generate mutations automatically", "Apply one mutation"],
    )

with right:
    if mode_label == "Generate mutations automatically":
        num_candidates = st.number_input(
            "Candidates",
            min_value=1,
            max_value=200,
            value=10,
            step=1,
        )
        mutations_per_candidate = st.number_input(
            "Mutations per candidate",
            min_value=1,
            max_value=max(1, len(sequence)),
            value=2 if len(sequence) >= 2 else 1,
            step=1,
        )
        random_seed = st.number_input("Seed", min_value=0, value=7, step=1)
        requested_mutation = None
        mutation_mode = "auto"
    else:
        col_a, col_b, col_c = st.columns([1, 1, 1])
        original_aa = col_a.text_input("Original AA", value=sequence[9:10] or "A", max_chars=1)
        position = col_b.number_input(
            "Position",
            min_value=1,
            max_value=max(1, len(sequence)),
            value=min(10, max(1, len(sequence))),
            step=1,
        )
        new_aa = col_c.text_input("New AA", value="K", max_chars=1)
        requested_mutation = f"{clean_sequence(original_aa)}{position}{clean_sequence(new_aa)}"
        st.text_input("Mutation", value=requested_mutation, disabled=True)
        num_candidates = 1
        mutations_per_candidate = 1
        random_seed = 7
        mutation_mode = "single"

run_clicked = st.button(
    "Run mutation generator",
    type="primary",
    disabled=not is_valid,
    use_container_width=True,
)

if run_clicked:
    try:
        with st.spinner("Generating mutations"):
            outputs = run_mutation_pipeline(
                MutationConfig(
                    protein_name=safe_name(protein_name),
                    sequence=sequence,
                    mutation_mode=mutation_mode,
                    num_candidates=int(num_candidates),
                    mutations_per_candidate=int(mutations_per_candidate),
                    requested_mutation=requested_mutation,
                    random_seed=int(random_seed),
                )
            )

        st.session_state["outputs"] = outputs
        st.success("Mutation run complete")
    except Exception as exc:
        st.error(str(exc))

outputs = st.session_state.get("outputs")

if outputs:
    summary_tab, frequency_tab, transitions_tab, heatmap_tab, downloads_tab = st.tabs(
        [
            "Candidate Summary",
            "Mutation Frequency",
            "Property Transitions",
            "Heatmap",
            "Downloads",
        ]
    )

    with summary_tab:
        st.dataframe(
            pd.read_csv(outputs["candidate_summary"]),
            use_container_width=True,
            hide_index=True,
        )

    with frequency_tab:
        st.dataframe(
            pd.read_csv(outputs["mutation_frequency"]),
            use_container_width=True,
            hide_index=True,
        )

    with transitions_tab:
        st.dataframe(
            pd.read_csv(outputs["property_transitions"]),
            use_container_width=True,
            hide_index=True,
        )

    with heatmap_tab:
        st.image(str(outputs["heatmap"]), use_container_width=True)

    with downloads_tab:
        col_1, col_2, col_3, col_4, col_5 = st.columns(5)

        with col_1:
            download_button("FASTA", outputs["fasta"], "text/plain")
        with col_2:
            download_button("Summary CSV", outputs["candidate_summary"], "text/csv")
        with col_3:
            download_button("Frequency CSV", outputs["mutation_frequency"], "text/csv")
        with col_4:
            download_button("Transitions CSV", outputs["property_transitions"], "text/csv")
        with col_5:
            download_button("Heatmap PNG", outputs["heatmap"], "image/png")
