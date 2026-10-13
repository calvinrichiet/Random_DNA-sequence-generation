# Generate random DNA sequences.

import random

# Import Biopython's standard genetic code and sequence translation tools.
from Bio.Data import CodonTable
from Bio.Seq import Seq

# Load the standard code, including amino-acid codons and stop codons.
STANDARD_CODE = CodonTable.unambiguous_dna_by_name["Standard"]
# Keep codons that encode amino acids for the internal coding region.
SENSE_CODONS = tuple(STANDARD_CODE.forward_table)
# Keep valid terminal codons that signal the end of translation.
STOP_CODONS = tuple(STANDARD_CODE.stop_codons)


# Return random coding DNA using the standard genetic code. Sequences start
# with ATG, end with a standard stop codon, and contain complete codons.
def random_dna(length):
    # A coding region needs at least a start codon and a stop codon.
    if length < 6:
        raise ValueError("Sequence length must be at least 6 bases")

    # Reserve complete codons for the coding region and trailing bases for after the stop.
    coding_length = length - length % 3
    noncoding_length = length - coding_length

    # Pick the remaining codons randomly, excluding stop codons from the body.
    internal_codons = random.choices(SENSE_CODONS, k=coding_length // 3 - 2)
    # Add the start codon, internal codons, and one standard stop codon.
    coding_sequence = "ATG" + "".join(internal_codons) + random.choice(STOP_CODONS)
    # Ask Biopython to verify the sequence is a complete standard-code CDS.
    Seq(coding_sequence).translate(table="Standard", cds=True)
    # Append random bases after the stop to preserve the requested total length.
    noncoding_sequence = "".join(random.choices("ACGT", k=noncoding_length))
    return coding_sequence + noncoding_sequence