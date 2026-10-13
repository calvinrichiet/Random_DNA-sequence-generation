#!/usr/bin/env python3
# Generate random DNA sequences and write them to a FASTA file.

import random    # standard library module for random number generation
import sys       # used for exiting with an error code
from pathlib import Path  # build paths that work across operating systems

# Find the project folder relative to this script's location.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
# Add the project folder so modules can be imported when this script is run directly.
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Import the command-line parser and FASTA writer from their sections.
from modules.argument_parsing import parse_arguments
from modules.fasta_output import write_fasta

# Coordinate argument parsing, sequence writing, and the success message.
def main():
    args = parse_arguments()  # read and validate the command-line options

    if args.seed is not None:  # only set a seed when one was provided
        random.seed(args.seed)  # make this run's random sequences reproducible

    try:
        actual_length = write_fasta(args.num_seqs, args.length, args.output)  # generate and save the records
    except OSError as err:  # handle file and path errors cleanly
        sys.exit(f"Error writing to {args.output}: {err}")  # show the error and exit unsuccessfully

    # Confirm the number, length, and destination after a successful write.
    print(f"Wrote {args.num_seqs} sequence(s) of length {actual_length} to {args.output}")


if __name__ == "__main__":  # run main() only when executed as a script, not when imported
    main()