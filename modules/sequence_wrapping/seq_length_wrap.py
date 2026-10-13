# Wrap sequences into lines suitable for FASTA output.

line_length = 80  # maximum FASTA sequence characters written on each line


# Split a sequence into chunks no longer than width.
def wrap_sequence(sequence, width=line_length):
    # Slice the sequence into consecutive chunks no longer than width.
    return [sequence[index:index + width] for index in range(0, len(sequence), width)]