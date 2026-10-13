# Random DNA Sequence Generator

A small Python command-line project for generating random DNA sequences and
writing them to a FASTA file. Each generated sequence contains a coding
sequence validated against Biopython's standard genetic code, with a start
codon and stop codon, followed by any requested trailing bases.

## What it does

For each requested record, the program:

1. Generates a DNA sequence made from the bases `A`, `C`, `G`, and `T`.
2. Starts its coding region with `ATG`.
3. Fills the middle of the coding region with randomly selected codons that
   encode amino acids (stop codons are not used in this region).
4. Ends the coding region with one of the standard stop codons: `TAA`, `TAG`,
   or `TGA`.
5. Uses Biopython to validate that this coding region is a complete
   protein-coding sequence under the standard genetic code.
6. Adds any leftover bases after the stop codon so that the total sequence
   length is exactly the requested length.
7. Writes the records in FASTA format, wrapping sequence lines at 80 bases.

The requested length must be at least 6 bases, enough room for the 3-base
start and stop codons. The coding portion is rounded down to a multiple of
three; when the requested length is not divisible by three, the remaining one
or two bases are appended after the stop codon. For example, a requested
length of 151 produces a 150-base coding portion followed by one trailing
base. Consequently, those trailing bases are not part of the validated
coding sequence.

Internal codons are selected randomly from the standard genetic code's
amino-acid codons. This is a simple random generator, not a model of organism-
specific codon usage, GC content, gene structure, or biological sequence
variation.

## Requirements

- Python 3
- Biopython

The code imports Biopython's codon table and sequence translation modules.
NumPy may be installed automatically as a Biopython dependency; this project
does not use NumPy directly.

## Setup

Run these commands from the project directory. A virtual environment keeps
the project dependencies separate from system Python:

```bash
python3 -m venv .venv
```

Activate the environment:

```bash
# Linux or macOS
source .venv/bin/activate

# Windows PowerShell
.venv\Scripts\Activate.ps1
```

Install Biopython:

```bash
python -m pip install biopython
```

If your system does not provide the `python3` command, use the Python 3
interpreter command available on your system to create and activate the
environment. Once set up, run the program with the environment's Python, or
activate the environment first as shown above.

## Run the program

The command-line entry point is `Scripts/main.py`. From the project root:

```bash
python Scripts/main.py --num_seqs 10 --length 150 --output results/random.fasta
```

This generates 10 sequences of 150 bases and writes them to
`results/random.fasta`. The destination directory must already exist.

Short option names are also available:

```bash
python Scripts/main.py -n 10 -l 150 -o results/random.fasta
```

To see all options and their descriptions:

```bash
python Scripts/main.py --help
```

### Command-line options

| Option | Required | Description |
|---|---:|---|
| `-n`, `--num_seqs` | Yes | Number of sequences to generate; must be a positive integer. |
| `-l`, `--length` | Yes | Total length of each sequence in bases; must be a positive integer and at least 6. |
| `-o`, `--output` | Yes | Output FASTA filename or path. Existing files at that path are overwritten. |
| `-s`, `--seed` | No | Integer random seed. Supplying the same seed and arguments makes the run reproducible with the same Python and Biopython behavior. |
| `-h`, `--help` | No | Show the command-line help. |

The length check in the current command-line parser accepts positive integers.
Lengths below 6 are rejected by the sequence generator, so use a length of 6
or greater.

### Reproducible output

Provide an integer seed to make repeated runs reproducible:

```bash
python Scripts/main.py -n 5 -l 120 -o results/repeatable.fasta --seed 42
```

Re-running the same command in the same environment produces the same output.
Changing the seed changes the random sequences. The program uses Python's
standard `random` module; do not use this seed as a source of cryptographic
randomness.

## FASTA output

Each record has a header containing its record number and length, followed by
the DNA sequence on one or more lines:

```text
>seq1 length=12
ATGAAACCGTAA
>seq2 length=12
ATGCCCGGGTAG
```

The example illustrates the file layout; the bases are random. Headers are
numbered from `seq1` for each run. Sequence lines are at most 80 characters
long. FASTA readers such as Biopython can parse the output.

**Output files are replaced, not appended to.** Use a new output filename or
move an existing file before running if you need to preserve it.

## Project structure

```text
Random_DNA-sequence-generation/
├── README.md
├── Scripts/
│   └── main.py
├── modules/
│   ├── argument_parsing/
│   │   └── arg_parser.py
│   ├── fasta_output/
│   │   └── output_writer.py
│   ├── sequence_generation/
│   │   └── seq_gen.py
│   └── sequence_wrapping/
│       └── seq_length_wrap.py
└── results/
    └── trail*.fasta
```

- `Scripts/main.py` is the command-line entry point. It parses options, seeds
  the random generator when requested, calls the FASTA writer, and reports
  file-writing errors.
- `modules/argument_parsing/arg_parser.py` defines and validates CLI
  arguments.
- `modules/sequence_generation/seq_gen.py` generates the DNA and checks the
  coding portion using Biopython.
- `modules/sequence_wrapping/seq_length_wrap.py` wraps sequence text into
  lines no longer than 80 bases.
- `modules/fasta_output/output_writer.py` writes numbered FASTA records.
- `results/` contains example FASTA output files.

## Recreate the project and its output

To recreate the project from source:

1. Obtain or clone this repository from its hosting location.
2. Change into the `Random_DNA-sequence-generation` project directory.
3. Create and activate a Python virtual environment using the [setup
   instructions](#setup).
4. Install Biopython with `python -m pip install biopython`.
5. Run the command from [Run the program](#run-the-program).

For example, to create a reproducible output file:

```bash
python Scripts/main.py \
  --num_seqs 10 \
  --length 150 \
  --output results/recreated.fasta \
  --seed 42
```

The `results` directory must exist before running. The seed makes it possible
to reproduce a generated dataset under the same software environment; without
a seed, each run generally produces different sequences.

To recreate the source project manually, keep the package directories and
their `__init__.py` files, as well as the script and module files shown in
the project structure above. The Python modules import one another using the
`modules` package, so run `Scripts/main.py` from the project tree rather than
moving the entry point on its own.

## Troubleshooting

### `ModuleNotFoundError: No module named 'Bio'`

Biopython is missing from the Python environment running the script. Activate
the project's virtual environment and install it there:

```bash
source .venv/bin/activate
python -m pip install biopython
```

On Windows PowerShell, activate with `.venv\Scripts\Activate.ps1` first.
If multiple Python installations are present, make sure the `python` used for
installation is the same environment used to run `Scripts/main.py`.

### `externally-managed-environment` while installing

Some Linux distributions prevent installing packages into system Python.
Create and activate a virtual environment as described under [Setup](#setup),
then run `python -m pip install biopython` inside it. Avoid forcing a
system-wide pip installation.

### `Sequence length must be at least 6 bases`

The generator needs at least 6 bases for a start codon (`ATG`) and a stop
codon. Increase `--length` to 6 or more.

### Invalid positive-integer argument

`--num_seqs` and `--length` must be integers greater than zero. For example,
use `--num_seqs 10 --length 150`, not `--num_seqs 0`, a negative number, or a
decimal value.

### `Error writing to ...` or a file/path error

Check that the output path is valid and that its parent directory exists.
The program does not create missing directories. Also check that you have
permission to write there and that the destination is not a directory or
otherwise unavailable.

### The output file replaced older data

This is expected: the writer opens the destination in write mode. Choose a
different output path when the previous file needs to be kept.

### Import errors when running the script

Run the provided entry point from the project tree:

```bash
python Scripts/main.py ...
```

Check that the `modules/` directory and its package `__init__.py` files are
present. Running a module after separating it from the project folders can
prevent Python from finding the other project modules.

### Need to inspect or validate the output

Open the output file in a text editor or parse it with Biopython. Each record
should start with a `>` header; sequence data should contain only `A`, `C`,
`G`, and `T`; each record should have the requested total length; and sequence
lines should be no longer than 80 bases. The validated coding region starts
with `ATG` and ends with a standard stop codon before any trailing bases.
