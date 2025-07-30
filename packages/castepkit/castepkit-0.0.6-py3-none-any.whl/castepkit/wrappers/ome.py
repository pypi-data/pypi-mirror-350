import argparse

from castepkit.utils import check_files_exist, run_program

__all__ = ["run_ome"]


def run_ome(
    prefix: str,
    orbital_suffix: str = "cutatom_check",
) -> None:
    """
    Run calculate_ome_impi_XTIPC on the given CASTEP prefix.

    Parameters
    ----------
    prefix : str
        The prefix of the CASTEP calculation files.
    orbital_suffix : str
        Extension suffix of the orbital file (e.g., "cutatom_check").
    """
    required_inputs = [
        f"{prefix}.cell",
        f"{prefix}.param",
        f"{prefix}.{orbital_suffix}",
        # "Ga_00.recpot",
        # "As_00.recpot",
    ]
    check_files_exist(required_inputs, label="required ome input files")

    input_str = f"{orbital_suffix}\n"

    stdout, stderr = run_program("ome", input_str, [prefix])

    print("=== ome STDOUT ===")
    print(stdout)
    if stderr:
        print("=== ome STDERR ===")
        print(stderr)

    expected_outputs = [
        f"{prefix}.cst_ome",
        f"{prefix}.castep",
    ]
    check_files_exist(expected_outputs, label="ome output files")


def main():
    parser = argparse.ArgumentParser(description="Wrapper for calculate_ome_impi_XTIPC")
    parser.add_argument("prefix", help="Prefix of the CASTEP calculation")
    parser.add_argument(
        "--orbital_suffix",
        default="cutatom_check",
        help="Suffix of the orbital file (default: %(default)s)",
    )

    args = parser.parse_args()

    run_ome(
        prefix=args.prefix,
        orbital_suffix=args.orbital_suffix,
    )


if __name__ == "__main__":
    main()
