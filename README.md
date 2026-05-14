# Protein Design Project

## Vision

Modern protein engineering increasingly relies on AI systems that combine:

- geometric reasoning
- sequence generation
- mutation ranking
- structural analysis
- stability prediction

This project explores how lightweight, modular AI pipelines can be built around pretrained protein models without requiring massive training infrastructure.

Rather than training frontier-scale protein models from scratch, the goal is to orchestrate existing open-source models into a practical redesign workflow for:

- mutation exploration
- stability-oriented redesign
- sequence optimization
- protein engineering research
- educational visualization

The system is intentionally designed to be modular, interpretable, and runnable on consumer hardware.

A modular protein redesign pipeline using ProteinMPNN for sequence generation, mutation parsing, and mutation visualization.

## Project Goal

This project explores how pretrained protein design models can be used as practical components in a protein engineering workflow.

The current version focuses on:

1. Running ProteinMPNN on an input PDB structure
2. Generating redesigned protein sequences
3. Comparing redesigned sequences against the original sequence
4. Extracting mutations
5. Visualizing mutation patterns with a heatmap

## Current Pipeline

```text
Input PDB
   ↓
ProteinMPNN inference
   ↓
Generated candidate sequences
   ↓
Mutation parser
   ↓
Mutation heatmap
