import argparse

from castepkit.utils import check_files_exist, run_program

__all__ = ["run_atom_cutting"]


def run_atom_cutting(
    prefix: str,
    input_type: int = 2,  # 1 for .charge, 2 for .orbitals
) -> None:
    """
    Run atom_cutting_impi_XTIPC on a specified CASTEP prefix.

    Parameters
    ----------
    prefix : str
        The prefix of the CASTEP calculation files.
    input_type : int
        Type of wavefunction input: 1 = *.charge, 2 = *.orbitals (default).
    """
    required_inputs = [
        # TODO: write a script to genreate switch file.
        f"{prefix}.switch",
        f"{prefix}.cell",
        f"{prefix}.bands",
        f"{prefix}.param",
        f"{prefix}.orbitals" if input_type == 2 else f"{prefix}.charge",
        # TODO: check which recpot do we need
        # "Ga_00.recpot",
        # "As_00.recpot",
    ]
    check_files_exist(required_inputs, label="required atom-cutting input files")

    # Prepare stdin input string
    input_str = f"{input_type}\n"

    # Run the program
    stdout, stderr = run_program("atom_cutting", input_str, [prefix])

    print("=== atom_cutting STDOUT ===")
    print(stdout)
    if stderr:
        print("=== atom_cutting STDERR ===")
        print(stderr)

    expected_outputs = [
        f"{prefix}.cutatom_check",
        f"{prefix}_den.grd",
        f"{prefix}.castep",
        f"{prefix}.castep_bin",
    ]
    check_files_exist(expected_outputs, label="atom-cutting output files")


def main():
    parser = argparse.ArgumentParser(description="Wrapper for atom_cutting_impi_XTIPC")
    parser.add_argument("prefix", help="Prefix of the CASTEP calculation")
    parser.add_argument(
        "--input_type",
        type=int,
        choices=[1, 2],
        default=2,
        help="Input file type: 1 = *.charge, 2 = *.orbitals (default: %(default)s)",
    )

    args = parser.parse_args()

    run_atom_cutting(
        prefix=args.prefix,
        input_type=args.input_type,
    )


if __name__ == "__main__":
    main()
