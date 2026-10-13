# Parse and validate command-line arguments for the sequence generator.

import argparse


# Parse a positive integer or raise an argparse validation error.
def positive_int(value):
    try:
        number = int(value)  # convert the command-line text to an integer
    except (TypeError, ValueError):
        # Let argparse display this as a command-line input error.
        raise argparse.ArgumentTypeError(
            f"{value} is not a positive integer, please try again"
        )

    if number < 1:
        # Reject zero and negative values for counts and sequence lengths.
        raise argparse.ArgumentTypeError(
            f"{value} is not a positive integer, please try again"
        )
    return number  # give argparse the validated integer value


# Parse CLI arguments, optionally using an explicit argument list.
def parse_arguments(argv=None):
    # Configure the usage message shown by --help.
    parser = argparse.ArgumentParser(
        description="Generate random DNA sequences in FASTA format."
    )
    # Require a positive number of sequences.
    parser.add_argument(
        "-n", "--num_seqs", type=positive_int, required=True,
        help="number of sequences to generate",
    )
    # Require a positive nucleotide length for every sequence.
    parser.add_argument(
        "-l", "--length", type=positive_int, required=True,
        help="length of each sequence (in nucleotides)",
    )
    # Require the destination FASTA filename or path.
    parser.add_argument(
        "-o", "--output", required=True,
        help="output FASTA file name",
    )
    # Accept an optional integer seed for repeatable random output.
    parser.add_argument(
        "-s", "--seed", type=int, default=None,
        help="optional random seed for reproducibility",
    )
    return parser.parse_args(argv)  # parse argv, or use the command line by default