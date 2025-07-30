#!/usr/bin/env python3

import argparse

from .utils import check_files_exist, run_program

__all__ = ["run_shg"]


def run_shg(
    calc_name: str,
    scissors: float = 0.0,
    direction: str = "123",
    band_resolved: int = 1,
    rank_number: int = 0,
    unit: int = 0,
    output_level: int = 0,
    is_metal: int = 2,
    energy_range: int = 0,
) -> None:
    """
    Run the NewSHG_ZY-XTIPC.x program for computing second harmonic generation (SHG).

    Parameters
    ----------
    calc_name : str
        Prefix of the CASTEP calculation.
    scissors : float
        Scissors correction (in eV).
    direction : str
        Direction index, e.g., '123'.
    band_resolved : int
        Whether to do band-resolved analysis (0/1).
    rank_number : int
        Number of ranked contributions to output.
    unit : int
        Output unit: 0 = pm/V, 1 = esu.
    output_level : int
        Verbosity level.
    is_metal : int
        Whether the system is metallic (1 = Yes, 2 = No).
    energy_range : int
        Energy range option: 0, 1, or 2.
    """
    # Check CASTEP files exist
    required_inputs = [
        f"{calc_name}.bands",
        f"{calc_name}.cell",
        f"{calc_name}.ome_bin",
        # TODO: here we need the element symbol
        # f"As_00.recpot",
        # f"Ga_00.recpot",
    ]

    check_files_exist(required_inputs, label="required input files")

    # Prepare input string for the SHG executable
    input_lines = [
        scissors,
        direction,
        band_resolved,
        rank_number,
        unit,
        output_level,
        is_metal,
        energy_range,
    ]
    input_str = "\n".join(str(x) for x in input_lines) + "\n"

    # Run the executable
    stdout, stderr = run_program("NewSHG_ZY-XTIPC.x", input_str, [calc_name])

    print("=== SHG STDOUT ===")
    print(stdout)
    if stderr:
        print("=== SHG STDERR ===")
        print(stderr)

    # Check expected outputs
    expected_outputs = [
        # TODO
    ]
    check_files_exist(expected_outputs, label="SHG output files")


def main():
    parser = argparse.ArgumentParser(
        description="Wrapper for SHG calculation using NewSHG_ZY-XTIPC.x"
    )
    parser.add_argument("calc_name", help="Prefix of the CASTEP calculation")
    parser.add_argument("--direction", default="123", help="Direction index (e.g., 111, 123)")
    parser.add_argument("--scissors", type=float, default=0.0, help="Scissors correction in eV")
    parser.add_argument(
        "--band_resolved",
        type=int,
        choices=[0, 1],
        default=1,
        help="Band resolved analysis (0/1)",
    )
    parser.add_argument(
        "--rank_number",
        type=int,
        default=0,
        help="Number of ranked contributions to print",
    )
    parser.add_argument(
        "--unit", type=int, choices=[0, 1], default=0, help="Output unit: 0=pm/V, 1=esu"
    )
    parser.add_argument(
        "--output_level",
        type=int,
        choices=[0, 1],
        default=0,
        help="Output verbosity level",
    )
    parser.add_argument(
        "--is_metal",
        type=int,
        choices=[1, 2],
        default=2,
        help="Is the system metallic? 1=Yes, 2=No",
    )
    parser.add_argument(
        "--energy_range",
        type=int,
        choices=[0, 1, 2],
        default=0,
        help="Energy range mode",
    )

    args = parser.parse_args()

    run_shg(
        calc_name=args.calc_name,
        scissors=args.scissors,
        direction=args.direction,
        band_resolved=args.band_resolved,
        rank_number=args.rank_number,
        unit=args.unit,
        output_level=args.output_level,
        is_metal=args.is_metal,
        energy_range=args.energy_range,
    )


if __name__ == "__main__":
    main()
