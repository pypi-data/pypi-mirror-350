#!/usr/bin/env python3

import argparse
from pathlib import Path

from .utils import check_files_exist, run_program

__all__ = ["run_weighted_den"]


def run_weighted_den(calc_name: str, weight_file: str, suffix: str, output_format: int) -> Path:
    """
    Run weighted_den.x on a specific input and rename the output file.

    Returns the final renamed Path.
    """
    # Check input exists
    check_files_exist([weight_file], label=f"input weight file ({suffix})")

    # Write input control file
    tmp_input_path = Path(f"{calc_name}.wden_in")
    tmp_input_path.write_text(weight_file)

    # Run program
    stdout, stderr = run_program("weighted_den.x", f"{output_format}\n", [calc_name])
    print(f"[weighted_den.x STDOUT ({suffix})]")
    print(stdout)
    if stderr:
        print(f"[weighted_den.x STDERR ({suffix})]")
        print(stderr)

    # Determine expected output file and rename
    ext_map = {1: "pot", 2: "check", 3: "grd"}
    ext = ext_map.get(output_format, "grd")

    output_file = Path(f"{calc_name}_wden.{ext}")
    target_file = Path(f"{calc_name}_{suffix}.{ext}")

    # Check output before renaming
    if not check_files_exist([output_file], label=f"raw output ({output_file})"):
        raise FileNotFoundError(f"Expected output file not found: {output_file}")

    output_file.rename(target_file)
    check_files_exist([target_file], label=f"final renamed output ({suffix})")

    return target_file


def main_single():
    parser = argparse.ArgumentParser(description="Run weighted_den.x for a single input file")
    parser.add_argument("calc_name", help="Prefix of CASTEP calculation files")
    parser.add_argument(
        "--input_file_suffix",
        default="shg_weight_veocc",
        help="Input file containing weighted density data (e.g., shg_weight_veocc)",
    )
    parser.add_argument(
        "--suffix",
        default="veocc",
        help="Suffix for the output file (e.g., 'veocc')",
    )
    parser.add_argument(
        "--wden_format",
        type=int,
        choices=[1, 2, 3],
        default=3,
        help="Output format: 1=.pot, 2=.check, 3=.grd",
    )

    args = parser.parse_args()

    run_weighted_den(
        args.calc_name,
        f"{args.calc_name}.{args.input_file_suffix}",
        args.suffix,
        args.wden_format,
    )


def main_both():
    parser = argparse.ArgumentParser(description="Run weighted_den.x for CASTEP outputs")
    parser.add_argument("calc_name", help="Prefix of CASTEP calculation files")
    parser.add_argument(
        "--wden_format",
        type=int,
        choices=[1, 2, 3],
        default=3,
        help="Output format: 1=.pot, 2=.check, 3=.grd",
    )

    args = parser.parse_args()

    input_cases = {
        "veocc": f"{args.calc_name}.shg_weight_veocc",
        "veunocc": f"{args.calc_name}.shg_weight_veunocc",
    }

    for suffix, input_file in input_cases.items():
        run_weighted_den(args.calc_name, input_file, suffix, args.wden_format)


def main_all():
    parser = argparse.ArgumentParser(description="Automate SHG and weighted_den.x workflow")
    parser.add_argument("calc_name", help="Calculation name prefix")
    parser.add_argument("--direction", default="123", help="Direction index (e.g. 111, 123)")
    parser.add_argument("--scissors", type=float, default=0.0, help="Scissors correction in eV")
    # parser.add_argument(
    #     "--band_resolved",
    #     type=int,
    #     choices=[0, 1],
    #     default=1,
    #     help="Band resolved analysis (0/1)",
    # )
    parser.add_argument("--rank_number", type=int, default=0, help="Number of ranked contributions")
    parser.add_argument(
        "--unit", type=int, choices=[0, 1], default=0, help="Output unit: 0=pm/V, 1=esu"
    )
    parser.add_argument(
        "--output_level",
        type=int,
        choices=range(4),
        default=0,
        help="Output verbosity level (0–3)",
    )
    parser.add_argument(
        "--is_metal",
        type=int,
        choices=[1, 2],
        default=2,
        help="Metallic system? 1=Yes, 2=No",
    )
    parser.add_argument(
        "--energy_range",
        type=int,
        choices=[0, 1, 2],
        default=0,
        help="Set energy range? 0/1/2",
    )
    parser.add_argument(
        "--wden_format",
        type=int,
        choices=[1, 2, 3],
        default=3,
        help="weighted_den.x output format",
    )

    args = parser.parse_args()

    _inputs = [
        args.scissors,
        args.direction,
        # args.band_resolved,
        1,
        args.rank_number,
        args.unit,
        args.output_level,
        args.is_metal,
        args.energy_range,
    ]
    shg_inputs = "\n".join([str(_inp) for _inp in _inputs]) + "\n"

    stdout, stderr = run_program("NewSHG_ZY-XTIPC.x", shg_inputs, [args.calc_name])
    print("=== SHG STDOUT ===")
    print(stdout)
    if stderr:
        print("=== SHG STDERR ===")
        print(stderr)

    outputs = [
        f"{args.calc_name}.chi{args.direction}",
        f"{args.calc_name}.shg_br_ve_{args.direction}",
        f"{args.calc_name}.shg_br_vh_{args.direction}",
        f"{args.calc_name}.shg_weight_veocc",
        f"{args.calc_name}.shg_weight_veunocc",
        f"{args.calc_name}.shg_weight_vhocc",
        f"{args.calc_name}.shg_weight_vhunocc",
    ]
    print("\n=== Output File Check ===")
    check_files_exist(outputs)

    # run_weighted_den(
    #     args.calc_name, f"{args.calc_name}.shg_weight_veocc", "veocc", args.wden_format
    # )
    # run_weighted_den(
    #     args.calc_name,
    #     f"{args.calc_name}.shg_weight_veunocc",
    #     "veunocc",
    #     args.wden_format,
    # )

    input_cases = {
        "veocc": f"{args.calc_name}.shg_weight_veocc",
        "veunocc": f"{args.calc_name}.shg_weight_veunocc",
    }

    for suffix, input_file in input_cases.items():
        run_weighted_den(args.calc_name, input_file, suffix, args.wden_format)


if __name__ == "__main__":
    main_both()
