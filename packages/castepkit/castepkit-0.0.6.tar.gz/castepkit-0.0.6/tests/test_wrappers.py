from pathlib import Path

import pytest
from common import prepare_test_data

# from castepkit.wrappers.atom_cutting import run_atom_cutting
# from castepkit.wrappers.ome import run_ome
from castepkit.wrappers.shg import run_shg
from castepkit.wrappers.weighted_dens import run_weighted_den

TEST_DATA = Path(__file__).parent / "data" / "GaAs"


@pytest.fixture
def tmp_gaas_optics(tmp_path):
    return prepare_test_data(TEST_DATA, tmp_path, prefix="GaAs_Optics")


@pytest.mark.parametrize(
    "direction",
    [
        "111",
        "112",
        "113",
        "121",
        "122",
        "123",
        "211",
        "212",
        "213",
        "221",
        "222",
        "223",
        "231",
        "232",
        "233",
        "311",
        "312",
        "313",
        "321",
        "322",
        "323",
        "331",
        "332",
        "333",
    ],
)
def test_run_shg_direction(direction, tmp_gaas_optics, monkeypatch):
    monkeypatch.chdir(tmp_gaas_optics)
    run_shg(
        prefix="GaAs_Optics",
        scissors=0.0,
        direction=direction,
        band_resolved=0,
        rank_number=0,
        unit=0,
        output_level=0,
        is_metal=2,
        energy_range=0,
    )
    assert Path(f"GaAs_Optics.chi{direction}").exists()
    assert Path("GaAs_Optics.castep").exists()


def test_run_shg_all(tmp_gaas_optics, monkeypatch):
    monkeypatch.chdir(tmp_gaas_optics)
    run_shg(
        prefix="GaAs_Optics",
        scissors=0.0,
        direction="all",
        band_resolved=0,
        rank_number=0,
        unit=0,
        output_level=0,
        is_metal=2,
        energy_range=0,
    )
    assert Path("GaAs_Optics.chi_all").exists()
    assert Path("GaAs_Optics.castep").exists()


def test_run_weighted_den(tmp_gaas_optics, monkeypatch):
    monkeypatch.chdir(tmp_gaas_optics)
    run_shg(
        prefix="GaAs_Optics",
        scissors=0.0,
        direction="123",
        band_resolved=1,
        rank_number=0,
        unit=0,
        output_level=0,
        is_metal=2,
        energy_range=0,
    )

    run_weighted_den(
        prefix="GaAs_Optics",
        weight_file="GaAs_Optics.shg_weight_veocc",
        suffix="veocc",
        output_format=3,
    )
    assert Path("GaAs_Optics_veocc.grd").exists()


# def test_run_atom_cutting(tmp_gaas_optics):
#     run_atom_cutting(prefix="GaAs_Optics", input_type=2)
#     assert (tmp_gaas_optics / "GaAs_Optics.cutatom_check").exists()
#
#
# def test_run_ome(tmp_gaas_optics):
#     run_atom_cutting(prefix="GaAs_Optics", input_type=2)
#     assert (tmp_gaas_optics / "GaAs_Optics.cutatom_check").exists()
#     run_ome(prefix="GaAs_Optics", orbital_suffix="cutatom_check")
#     assert (tmp_gaas_optics / "GaAs_Optics.cst_ome").exists()
