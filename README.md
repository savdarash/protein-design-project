# Protein Mutation Sandbox

Project 4: Protein Mutation Sandbox is a small sequence-first tool for generating and analyzing protein mutations.

The current MVP does not route through AlphaFold and does not run a full ProteinMPNN redesign workflow. It starts with a protein sequence, creates mutation candidates, and writes mutation-analysis artifacts that are easy to inspect.

## Workflow

```text
Protein sequence
   ↓
Amino-acid validation
   ↓
Mutation mode
   ├─ automatic candidate generation
   └─ one requested mutation
   ↓
Candidate FASTA
   ↓
Mutation analysis
   ├─ candidate summary
   ├─ mutation frequency
   ├─ property transitions
   └─ mutation heatmap
```

## Outputs

The pipeline writes only under `results/`:

- `results/scored_candidates/`
  - `<protein_name>_candidates.fasta`
  - `<protein_name>_candidate_summary.csv`
  - `<protein_name>_mutation_frequency.csv`
  - `<protein_name>_property_transitions.csv`
- `results/visualizations/`
  - `<protein_name>_mutation_heatmap.png`

## Run The Pipeline

Automatic mutation generation:

```bash
python3 -m src.mutation_pipeline \
  --protein-name sandbox \
  --sequence TTCCPSIVARSNFNVCRLPGTPEAICATYTGCIIIPGATCPGDYAN \
  --mode auto \
  --num-candidates 10 \
  --mutations-per-candidate 2 \
  --seed 7
```

One requested mutation:

```bash
python3 -m src.mutation_pipeline \
  --protein-name sandbox_single \
  --sequence TTCCPSIVARSNFNVCRLPGTPEAICATYTGCIIIPGATCPGDYAN \
  --mode single \
  --mutation R10K
```

Mutation labels use the format `A10V`: original amino acid, 1-indexed residue position, and new amino acid.

## Current Code Map

- `src/mutation_pipeline.py` is the main entry point.
- `src/mutation_config.py` validates pipeline configuration.
- `src/mutation_generator.py` generates automatic candidates or applies one requested mutation.
- `src/sequence_io.py` validates sequences and reads/writes FASTA records.
- `src/mutation_parser.py` finds sequence differences.
- `src/candidate_summary.py` writes per-candidate mutation summaries.
- `src/mutation_frequency.py` writes mutation-frequency tables.
- `src/property_transition_analysis.py` summarizes amino-acid property changes.
- `src/mutation_heatmap.py` writes mutation heatmaps.
- `src/amino_acid_properties.py` contains simple amino-acid property labels.

