import shutil
from pathlib import Path


def prepare_test_data(src_folder: Path, tmpdir, prefix: str) -> Path:
    """
    Copy files related to a given prefix from the source folder into tmpdir.

    Parameters
    ----------
    src_folder : Path
        Path to the directory containing test data files.
    tmpdir : Path
        Temporary directory to copy files into.
    prefix : str
        File prefix to match (e.g., 'GaAs' or 'GaAs_Optics').

    Returns
    -------
    Path
        The path to the new test directory with copied files.
    """
    tmp_path = Path(tmpdir)
    for file in src_folder.glob(f"{prefix}*"):
        shutil.copy(file, tmp_path / file.name)
    for file in src_folder.glob("*.recpot"):
        shutil.copy(file, tmp_path / file.name)
    return tmp_path
