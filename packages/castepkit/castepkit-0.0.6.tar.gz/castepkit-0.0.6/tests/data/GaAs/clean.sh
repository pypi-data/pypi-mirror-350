#!/bin/bash

# Get the name of this script
script_name=$(basename "$0")

# List of files to keep (relative to current directory)
keep_files=(
    "$script_name"
    # for SHG
    "GaAs_Optics.bands"
    "GaAs_Optics.cell"
    "GaAs_Optics.ome_bin"
    "As_00.recpot"
    "Ga_00.recpot"
    # for weighted_dens
    "GaAs_Optics.orbitals"
    "GaAs_Optics.check"
    "run.log"
)

# Build the find expression to exclude kept files
exclude_expr=()
for file in "${keep_files[@]}"; do
    exclude_expr+=(! -name "$file")
done

# Dry-run preview (uncomment below to test without deleting)
# echo "Would delete:"
# find . -maxdepth 1 -type f "${exclude_expr[@]}" -print

# Actual deletion
find . -maxdepth 1 -type f "${exclude_expr[@]}" -exec rm -v {} +
