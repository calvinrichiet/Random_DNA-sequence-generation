# Write generated DNA sequences in FASTA format.

from ..sequence_generation import random_dna
from ..sequence_wrapping import wrap_sequence


# Generate sequences and write them to a FASTA file.
def write_fasta(num_seqs, seq_length, output_file):
    # Open the destination for writing; this replaces any existing contents.
    with open(output_file, "w") as handle:
        # Number records from 1 through the requested sequence count.
        for index in range(1, num_seqs + 1):
            sequence = random_dna(seq_length)  # generate this record's DNA bases
            # Write a FASTA header with the record number and sequence length.
            handle.write(f">seq{index} length={seq_length}\n")
            # Wrap the bases and write each sequence line with a newline.
            for line in wrap_sequence(sequence):
                handle.write(line + "\n")