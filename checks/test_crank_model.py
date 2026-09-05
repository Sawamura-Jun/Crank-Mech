"""形状、運動、ねじの掛かり、STEPの再読込を検証する。"""

import math
from pathlib import Path

import cadquery as cq
import pytest

from crank_model import (BASE_TOP, CRANK_TOP, CRANK_Z, GUIDE_TOP, JOINT_TOP,
                         MAIN_TOP, ROD_Z, Parameters, build_parts,
                         collision_pairs, export_design, instances, kinematics)


@pytest.fixture(scope="session")
def params():
    return Parameters()


@pytest.fixture(scope="session")
def parts(params):
    return build_parts(params)


@pytest.mark.parametrize("name", [
    "P01_base", "P02_guide_rail", "P03_end_stop", "P04_crank_disk", "P05_connecting_rod",
    "P06_slider", "P07_main_post", "P08_joint_post", "P09_grip_post", "P10_main_bush",
    "P11_link_bush", "P12_hand_grip", "P13_retainer_M6", "P14_retainer_M5",
    "H_M6x40", "H_M5x30", "H_M5x12", "H_M5x25", "H_M5x50"])
def test_valid_single_solid(parts, name):
    shape = parts[name].shape.val()
    assert shape.isValid()
    assert len(shape.Solids()) == 1
    assert shape.Volume() > 1


def test_full_revolution_kinematics(params):
    # 1度ごとに連接棒の軸間と案内範囲を確認する。
    positions = []
    for angle in range(361):
        px, py, sx, _ = kinematics(params, angle)
        assert math.hypot(sx - px, py) == pytest.approx(120)
        assert sx - 16 >= 65
        assert sx + 16 <= 175
        positions.append(sx)
    assert max(positions) == pytest.approx(150)
    assert min(positions) == pytest.approx(90)
    assert max(positions) - min(positions) == pytest.approx(60)


@pytest.mark.parametrize("angle", range(0, 360, 15))
def test_no_solid_interference(parts, params, angle):
    assert collision_pairs(parts, params, angle, moving_only=angle != 0) == []


def test_bearing_and_fastener_stack(params):
    assert ROD_Z - (MAIN_TOP + 1.6 + 6) == pytest.approx(1.4)
    assert ROD_Z > GUIDE_TOP
    # ボルト先端が部品底面を突き抜けず、実用的なねじ掛かりを持つ。
    for top, length, surface, bottom, min_engagement in [
        (MAIN_TOP + 1.6, 40, BASE_TOP, 0, 9),
        (BASE_TOP + 19.8, 30, BASE_TOP, 0, 7.5),
        (BASE_TOP + 2.5, 12, BASE_TOP, 0, 7.5),
        (JOINT_TOP + 1, 25, CRANK_TOP, BASE_TOP, 7.5),
        (JOINT_TOP + 26.3, 50, CRANK_TOP, CRANK_Z, 7.5),
    ]:
        tip = top - length
        assert tip >= bottom
        assert surface - tip >= min_engagement
    assert len(instances(params)) == 33


@pytest.mark.parametrize("params", [Parameters(10, 120), Parameters(36, 120),
                                    Parameters(30, 10), Parameters(30, 110),
                                    Parameters(30, 130), Parameters(float("nan")),
                                    Parameters(angle_deg=float("inf"))])
def test_invalid_parameters(params):
    with pytest.raises(ValueError):
        params.validate()


@pytest.mark.parametrize("radius,length", [(24, 120), (35, 120), (30, 114), (30, 126)])
def test_alternative_dimensions(radius, length):
    p = Parameters(radius, length)
    p.validate()
    assert kinematics(p, 0)[2] - kinematics(p, 180)[2] == pytest.approx(2 * radius)


def test_step_roundtrip(parts, params, tmp_path: Path):
    # STEPを実際に書き出し、体積・外形・ソリッド数の保存を検証する。
    (tmp_path / "motion_check.json").write_text('{"old_result": true}', encoding="utf-8")
    manifest = export_design(tmp_path, params, parts)
    assert not (tmp_path / "motion_check.json").exists()
    assert len(manifest["parts"]) == 19
    for row in manifest["parts"]:
        imported = cq.importers.importStep(str(tmp_path / row["step"])).val()
        assert imported.isValid()
        assert len(imported.Solids()) == 1
        assert imported.Volume() == pytest.approx(row["volume_mm3"], rel=1e-7)
        bb = imported.BoundingBox()
        assert [bb.xlen, bb.ylen, bb.zlen] == pytest.approx(row["bbox_mm"], abs=1e-6)
    assembly = cq.importers.importStep(str(tmp_path / "assembly.step")).val()
    assert assembly.isValid()
    assert len(assembly.Solids()) == 33
    expected = sum(row["volume_mm3"] * row["quantity"] for row in manifest["parts"])
    assert assembly.Volume() == pytest.approx(expected, rel=1e-7)
