import subprocess
from pathlib import Path

__all__ = ["run_program", "check_files_exist"]


def run_program(executable, input_str, args=None):
    """Run a program with stdin input and return stdout, stderr."""
    cmd = [executable] + (args or [])
    result = subprocess.run(
        cmd,
        input=input_str.encode(),
        capture_output=True,
    )
    return result.stdout.decode(), result.stderr.decode()


def check_files_exist(files, label="file(s)", must_exist=True):
    """
    Check if specified files exist (or do not exist).

    Parameters
    ----------
    files : list of str or Path
        File paths to check.
    label : str
        Description to show in log messages.
    must_exist : bool
        If True, checks files exist. If False, checks they do NOT exist.

    Returns
    -------
    bool
        True if all files satisfy the existence condition, False otherwise.
    """
    files = [Path(f) for f in files]
    if must_exist:
        missing = [f for f in files if not f.is_file()]
        if missing:
            print(f"❌ Missing {label}:")
            for f in missing:
                print(f"  - {f}")
            return False
        print(f"✅ All {label} exist.")
        return True
    else:
        present = [f for f in files if f.is_file()]
        if present:
            print(f"❌ Unexpected existing {label}:")
            for f in present:
                print(f"  - {f}")
            return False
        return True
