#!/usr/bin/env python3

import argparse
from pathlib import Path

from castepkit.utils import check_files_exist, run_program
from castepkit.wrappers.shg import run_shg

__all__ = ["run_weighted_den"]


def run_weighted_den(prefix: str, weight_file: str, suffix: str, output_format: int) -> Path:
    """Run weighted_den.x on a specific input and rename the output file."""
    check_files_exist([weight_file], label=f"input weight file ({suffix})")
    Path(f"{prefix}.wden_in").write_text(weight_file)

    stdout, stderr = run_program("weighted_den", f"{output_format}\n", [prefix])
    # print(f"[weighted_den.x STDOUT ({suffix})]")
    print(stdout)
    if stderr:
        # print(f"[weighted_den.x STDERR ({suffix})]")
        print(stderr)

    ext_map = {1: "pot", 2: "check", 3: "grd"}
    ext = ext_map.get(output_format, "grd")

    output_file = Path(f"{prefix}_wden.{ext}")
    target_file = Path(f"{prefix}_{suffix}.{ext}")
    if not check_files_exist([output_file], label=f"raw output ({output_file})"):
        raise FileNotFoundError(f"Expected output file not found: {output_file}")

    output_file.rename(target_file)
    check_files_exist([target_file], label=f"final renamed output ({suffix})")

    return target_file


def main():
    parser = argparse.ArgumentParser(description="Unified CLI for SHG + weighted_den.x")
    subparsers = parser.add_subparsers(dest="mode", required=True)

    # === run ===
    p_run = subparsers.add_parser("run", help="Run weighted_den.x for a single file")
    p_run.add_argument("prefix", help="Prefix of CASTEP output files")
    p_run.add_argument(
        "--input_file_suffix",
        default="shg_weight_veocc",
        help="Suffix of input file (default: %(default)s)",
    )
    p_run.add_argument(
        "--suffix",
        default="veocc",
        help="Suffix for renamed output file (default: %(default)s)",
    )
    p_run.add_argument(
        "--wden_format",
        type=int,
        choices=[1, 2, 3],
        default=3,
        help="Output format: 1=.pot, 2=.check, 3=.grd (default: %(default)s)",
    )

    # === ve ===
    p_ve = subparsers.add_parser("ve", help="Run weighted_den.x for veocc and veunocc")
    p_ve.add_argument("prefix", help="Prefix of CASTEP output files")
    p_ve.add_argument(
        "--wden_format",
        type=int,
        choices=[1, 2, 3],
        default=3,
        help="Output format: 1=.pot, 2=.check, 3=.grd (default: %(default)s)",
    )

    # === shg ===
    p_shg = subparsers.add_parser("shg", help="Run SHG then weighted_den.x")
    p_shg.add_argument("prefix", help="Prefix of CASTEP output files")
    p_shg.add_argument(
        "--direction",
        default="123",
        help="SHG tensor direction index (default: %(default)s)",
    )
    p_shg.add_argument(
        "--scissors",
        type=float,
        default=0.0,
        help="Scissors correction in eV (default: %(default)s)",
    )
    # For shg density calculations, band_resolved should be always on.
    # p_shg.add_argument(
    #     "--band_resolved",
    #     type=int,
    #     choices=[0, 1],
    #     default=1,
    #     help="Band resolved analysis: 0=off, 1=on (default: %(default)s)",
    # )
    p_shg.add_argument(
        "--rank_number",
        type=int,
        default=0,
        help="Number of ranked contributions to print (default: %(default)s)",
    )
    p_shg.add_argument(
        "--unit",
        type=int,
        choices=[0, 1],
        default=0,
        help="Output unit: 0=pm/V, 1=esu (default: %(default)s)",
    )
    p_shg.add_argument(
        "--output_level",
        type=int,
        choices=[0, 1],
        default=0,
        help="Verbosity level (default: %(default)s)",
    )
    p_shg.add_argument(
        "--is_metal",
        type=int,
        choices=[1, 2],
        default=2,
        help="Is metallic? 1=yes, 2=no (default: %(default)s)",
    )
    p_shg.add_argument(
        "--energy_range",
        type=int,
        choices=[0, 1, 2],
        default=0,
        help="Energy range type: 0/1/2 (default: %(default)s)",
    )
    p_shg.add_argument(
        "--wden_format",
        type=int,
        choices=[1, 2, 3],
        default=3,
        help="weighted_den.x output format: 1=.pot, 2=.check, 3=.grd (default: %(default)s)",
    )

    args = parser.parse_args()

    if args.mode == "run":
        input_file = f"{args.prefix}.{args.input_file_suffix}"
        run_weighted_den(args.prefix, input_file, args.suffix, args.wden_format)

    elif args.mode == "ve":
        input_cases = {
            "veocc": f"{args.prefix}.shg_weight_veocc",
            "veunocc": f"{args.prefix}.shg_weight_veunocc",
        }
        for suffix, input_file in input_cases.items():
            run_weighted_den(args.prefix, input_file, suffix, args.wden_format)

    elif args.mode == "shg":
        run_shg(
            prefix=args.prefix,
            scissors=args.scissors,
            direction=args.direction,
            band_resolved=1,
            rank_number=args.rank_number,
            unit=args.unit,
            output_level=args.output_level,
            is_metal=args.is_metal,
            energy_range=args.energy_range,
        )

        input_cases = {
            "veocc": f"{args.prefix}.shg_weight_veocc",
            "veunocc": f"{args.prefix}.shg_weight_veunocc",
        }
        for suffix, input_file in input_cases.items():
            run_weighted_den(args.prefix, input_file, suffix, args.wden_format)


if __name__ == "__main__":
    main()
