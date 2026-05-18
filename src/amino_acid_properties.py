AMINO_ACID_PROPERTIES = {
    "A": "small hydrophobic",
    "V": "hydrophobic branched",
    "L": "hydrophobic bulky",
    "I": "hydrophobic branched",
    "M": "hydrophobic sulfur-containing",
    "F": "aromatic hydrophobic",
    "W": "aromatic bulky",
    "Y": "aromatic polar",
    "S": "polar small",
    "T": "polar small",
    "N": "polar amide",
    "Q": "polar amide",
    "C": "polar sulfur-containing",
    "G": "tiny flexible",
    "P": "rigid cyclic",
    "K": "positively charged",
    "R": "positively charged",
    "H": "positively charged / aromatic",
    "D": "negatively charged",
    "E": "negatively charged",
}


def describe_amino_acid_change(original_aa: str, candidate_aa: str):
    original_property = AMINO_ACID_PROPERTIES.get(original_aa, "unknown")
    candidate_property = AMINO_ACID_PROPERTIES.get(candidate_aa, "unknown")

    return f"{original_property} → {candidate_property}"


if __name__ == "__main__":
    print(describe_amino_acid_change("T", "V"))
