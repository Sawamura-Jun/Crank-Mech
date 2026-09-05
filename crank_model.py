"""金属加工用の教育用スライダ・クランク機構。単位は mm、角度は度。"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import asdict, dataclass
import json
import math
from pathlib import Path

import cadquery as cq


@dataclass(frozen=True)
class Parameters:
    """ベースとガイドを共用できる範囲で軸間寸法を変更する。"""

    crank_radius: float = 30.0
    rod_length: float = 120.0
    angle_deg: float = 45.0

    def validate(self) -> None:
        if not all(math.isfinite(v) for v in asdict(self).values()):
            raise ValueError("パラメータは有限の数値にしてください。")
        if not 24 <= self.crank_radius <= 35:
            raise ValueError("クランク半径は24～35 mmにしてください。")
        if self.rod_length <= self.crank_radius:
            raise ValueError("連接棒の軸間はクランク半径より長くしてください。")
        if self.rod_length - self.crank_radius < 84:
            raise ValueError("内死点でスライダがガイド端に近すぎます。")
        if self.rod_length + self.crank_radius > 156:
            raise ValueError("外死点でスライダがガイド端に近すぎます。")


# 軸方向寸法を一か所にまとめ、積み上げの関係を明示する。
BASE_TOP = 14.0
MAIN_FLANGE_H = 14.2
CRANK_T = 10.0
AXIAL_PLAY = 0.30
CRANK_Z = BASE_TOP + MAIN_FLANGE_H + AXIAL_PLAY / 2
CRANK_TOP = CRANK_Z + CRANK_T
JOINT_FLANGE_H = 9.0
ROD_T = 6.0
ROD_Z = CRANK_TOP + JOINT_FLANGE_H + AXIAL_PLAY / 2
JOINT_TOP = CRANK_TOP + JOINT_FLANGE_H + ROD_T + AXIAL_PLAY
GUIDE_TOP = 39.3
SLIDER_Z = BASE_TOP
SLIDER_H = CRANK_TOP - SLIDER_Z
MAIN_TOP = BASE_TOP + MAIN_FLANGE_H + CRANK_T + AXIAL_PLAY
RAIL_HOLES = [(x, y) for x in (80.0, 120.0, 160.0) for y in (-22.1, 22.1)]
STOP_HOLES = [(x, y) for x in (59.0, 181.0) for y in (-22.0, 22.0)]


@dataclass
class Part:
    name: str
    label: str
    shape: cq.Workplane
    material: str
    color: tuple[float, float, float]
    process: str
    purchased: bool = False


@dataclass(frozen=True)
class Instance:
    name: str
    part: str
    position: tuple[float, float, float]
    angle: float = 0.0
    motion: str = "fixed"

    def location(self) -> cq.Location:
        return cq.Location(cq.Vector(*self.position), cq.Vector(0, 0, 1), self.angle)


def block(x: float, y: float, z: float, dx: float, dy: float, dz: float) -> cq.Workplane:
    return cq.Workplane("XY").box(dx, dy, dz, centered=(False, False, False)).translate((x, y, z))


def cylinder(d: float, h: float, x: float = 0, y: float = 0, z: float = 0) -> cq.Workplane:
    return cq.Workplane("XY").circle(d / 2).extrude(h).translate((x, y, z))


def drill(shape: cq.Workplane, points: list[tuple[float, float]], d: float,
          z: float, depth: float) -> cq.Workplane:
    for x, y in points:
        shape = shape.cut(cylinder(d, depth, x, y, z))
    return shape


def ring(outer: float, inner: float, height: float) -> cq.Workplane:
    return cq.Workplane("XY").circle(outer / 2).circle(inner / 2).extrude(height)


def shoulder(flange_d: float, flange_h: float, shaft_d: float,
             shaft_h: float, bore_d: float) -> cq.Workplane:
    # 肩に座金を当てることで、ねじを締めても回転部品を挟み込まない。
    shape = cylinder(flange_d, flange_h).union(cylinder(shaft_d, shaft_h, z=flange_h))
    return drill(shape, [(0, 0)], bore_d, -1, flange_h + shaft_h + 2)


def socket_screw(d: float, length: float) -> cq.Workplane:
    # 市販ねじの配置確認用。ねじ山は省略し、呼び径の円筒で表す。
    head_d, head_h, socket_af = (8.5, 5.0, 4.0) if d == 5 else (10.0, 6.0, 5.0)
    sh = cylinder(d, length, z=-length).union(cylinder(head_d, head_h))
    socket = (cq.Workplane("XY").polygon(6, socket_af / math.cos(math.pi / 6))
              .extrude(head_h / 2 + 1).translate((0, 0, head_h / 2)))
    return sh.cut(socket)


def build_parts(p: Parameters) -> dict[str, Part]:
    p.validate()
    alu = (0.68, 0.74, 0.79)
    blue = (0.12, 0.39, 0.65)
    brass = (0.79, 0.61, 0.25)
    steel = (0.37, 0.41, 0.45)
    parts: dict[str, Part] = {}

    def add(name, label, shape, material, color, process, purchased=False):
        parts[name] = Part(name, label, shape, material, color, process, purchased)

    base = block(-55, -60, 0, 250, 120, BASE_TOP).edges("|Z").fillet(5)
    base = drill(base, [(-45, -50), (-45, 50), (185, -50), (185, 50)], 6.6, -1, 16)
    # タップは呼び径で簡略化。下穴径・ねじ呼びは加工指示書を優先する。
    base = drill(base, [(0, 0)], 6, -1, 16)
    base = drill(base, RAIL_HOLES + STOP_HOLES, 5, -1, 16)
    add("P01_base", "ベース", base, "A6061-T6", alu, "フライス・穴あけ・M5/M6タップ")

    # 同一のL形ガイドを180度回転して左右に使用する。
    rail = block(-55, 0, 0, 110, 17, GUIDE_TOP - BASE_TOP)
    rail = rail.cut(block(-56, -1, -1, 112, 6, 21.3))
    rail = drill(rail, [(-40, 12), (0, 12), (40, 12)], 5.5, -1, 28)
    rail = drill(rail, [(-40, 12), (0, 12), (40, 12)], 9, 19.8, 7)
    add("P02_guide_rail", "押さえ付きガイド", rail, "A6061-T6", alu, "フライス・段加工・座ぐり")

    stop = block(-6, -28, 0, 12, 56, 8).edges("|Z").fillet(1)
    stop = drill(stop, [(0, -22), (0, 22)], 5.5, -1, 10)
    stop = drill(stop, [(0, -22), (0, 22)], 9, 2.5, 7)
    add("P03_end_stop", "抜け止め", stop, "A6061-T6", alu, "フライス・穴あけ・座ぐり")

    disk = cylinder(86, CRANK_T).edges().chamfer(0.5)
    disk = drill(disk, [(0, 0)], 16, -1, CRANK_T + 2)
    disk = drill(disk, [(p.crank_radius, 0)], 5, -1, CRANK_T + 2)
    # 軽量化穴は回転半径の反対側に設け、クランク位置を視認しやすくする。
    disk = drill(disk, [(-24, 0)], 18, -1, CRANK_T + 2)
    add("P04_crank_disk", "クランク円板", disk, "A6061-T6", blue, "旋削・フライス・M5タップ")

    rod = (cq.Workplane("XY").center(p.rod_length / 2, 0)
           .slot2D(p.rod_length + 20, 20).extrude(ROD_T))
    rod = drill(rod, [(0, 0), (p.rod_length, 0)], 12, -1, ROD_T + 2)
    add("P05_connecting_rod", "連接棒", rod, "A6061-T6", blue, "フライス・ブッシュ穴仕上げ")

    slider = block(-16, -15, 0, 32, 30, 20).union(block(-16, -10, 20, 32, 20, SLIDER_H - 20))
    slider = slider.edges("|Z").chamfer(0.5)
    slider = drill(slider, [(0, 0)], 5, -1, SLIDER_H + 2)
    add("P06_slider", "スライダ", slider, "黄銅", brass, "フライス・摺動面仕上げ・M5タップ")

    add("P07_main_post", "固定中心軸", shoulder(22, MAIN_FLANGE_H, 12, 10.3, 6.6),
        "S45C", steel, "旋削・軸径仕上げ・貫通穴")
    add("P08_joint_post", "連接棒用段付き軸", shoulder(16, 9, 8, 6.3, 5.5),
        "S45C", steel, "旋削・軸径仕上げ・貫通穴")
    add("P09_grip_post", "握り用段付き軸", shoulder(12, 1, 8, 23.3, 5.5),
        "S45C", steel, "旋削・軸径仕上げ・貫通穴")
    add("P10_main_bush", "中心軸ブッシュ", ring(16, 12.04, 10),
        "黄銅", brass, "旋削・圧入後内径仕上げ")
    add("P11_link_bush", "連接棒ブッシュ", ring(12, 8.04, 6),
        "黄銅", brass, "旋削・圧入後内径仕上げ")
    grip = ring(20, 8.04, 23).edges().chamfer(0.5)
    add("P12_hand_grip", "回転握り", grip, "黄銅", brass, "旋削・内径仕上げ・端面C0.5")
    add("P13_retainer_M6", "中心軸押さえ座金", ring(18, 6.6, 1.6),
        "鋼", steel, "旋削・厚さ仕上げ")
    add("P14_retainer_M5", "小軸押さえ座金", ring(15, 5.5, 1),
        "鋼", steel, "旋削・厚さ仕上げ")
    for d, length in ((6, 40), (5, 30), (5, 12), (5, 25), (5, 50)):
        add(f"H_M{d}x{length}", f"六角穴付きボルト M{d}×{length}", socket_screw(d, length),
            "鋼・市販品", steel, "購入（ねじ山省略の参考形状）", True)
    return parts


def kinematics(p: Parameters, angle: float) -> tuple[float, float, float, float]:
    p.validate()
    if not math.isfinite(angle):
        raise ValueError("角度は有限の数値にしてください。")
    a = math.radians(angle)
    px, py = p.crank_radius * math.cos(a), p.crank_radius * math.sin(a)
    sx = px + math.sqrt(p.rod_length ** 2 - py ** 2)
    rod_angle = math.degrees(math.atan2(-py, sx - px))
    return px, py, sx, rod_angle


def instances(p: Parameters, angle: float | None = None) -> list[Instance]:
    angle = p.angle_deg if angle is None else angle
    px, py, sx, rod_angle = kinematics(p, angle)
    items: list[Instance] = []

    def put(name, part, x=0, y=0, z=0, a=0, motion="fixed"):
        items.append(Instance(name, part, (x, y, z), a, motion))

    put("base", "P01_base")
    put("rail_left", "P02_guide_rail", 120, 10.1, BASE_TOP)
    put("rail_right", "P02_guide_rail", 120, -10.1, BASE_TOP, 180)
    for x, tag in ((59, "inner"), (181, "outer")):
        put(f"stop_{tag}", "P03_end_stop", x, 0, BASE_TOP)
    put("main_post", "P07_main_post", z=BASE_TOP)
    put("main_retainer", "P13_retainer_M6", z=MAIN_TOP)
    put("main_screw", "H_M6x40", z=MAIN_TOP + 1.6)
    put("crank", "P04_crank_disk", z=CRANK_Z, a=angle, motion="crank")
    put("main_bush", "P10_main_bush", z=CRANK_Z, a=angle, motion="crank")
    put("slider", "P06_slider", sx, 0, SLIDER_Z, motion="slider")
    put("rod", "P05_connecting_rod", px, py, ROD_Z, rod_angle, "rod")
    for tag, x, y, motion in (("crank", px, py, "pin"), ("slider", sx, 0, "slider")):
        put(f"bush_{tag}", "P11_link_bush", x, y, ROD_Z, rod_angle, motion)
        put(f"post_{tag}", "P08_joint_post", x, y, CRANK_TOP, motion=motion)
        put(f"retainer_{tag}", "P14_retainer_M5", x, y, JOINT_TOP, motion=motion)
    put("slider_screw", "H_M5x25", sx, 0, JOINT_TOP + 1, motion="slider")
    put("grip_post", "P09_grip_post", px, py, JOINT_TOP + 1, motion="pin")
    put("grip", "P12_hand_grip", px, py, JOINT_TOP + 2.15, motion="pin")
    put("grip_retainer", "P14_retainer_M5", px, py, JOINT_TOP + 25.3, motion="pin")
    put("grip_screw", "H_M5x50", px, py, JOINT_TOP + 26.3, motion="pin")
    for i, (x, y) in enumerate(RAIL_HOLES, 1):
        put(f"rail_screw_{i}", "H_M5x30", x, y, BASE_TOP + 19.8)
    for i, (x, y) in enumerate(STOP_HOLES, 1):
        put(f"stop_screw_{i}", "H_M5x12", x, y, BASE_TOP + 2.5)
    return items


def make_assembly(parts: dict[str, Part], p: Parameters, angle: float | None = None) -> cq.Assembly:
    assembly = cq.Assembly(name="Educational_slider_crank_mm")
    for item in instances(p, angle):
        part = parts[item.part]
        assembly.add(part.shape, name=item.name, loc=item.location(), color=cq.Color(*part.color))
    return assembly


def collision_pairs(parts: dict[str, Part], p: Parameters, angle: float,
                    *, moving_only: bool = False) -> list[dict]:
    """包絡箱で候補を絞り、実ソリッドの共通体積で干渉を判定する。"""
    shapes = [(item, parts[item.part].shape.val().located(item.location())) for item in instances(p, angle)]
    bounds = [s.BoundingBox() for _, s in shapes]
    collisions = []
    for i, (a, sa) in enumerate(shapes):
        for j in range(i + 1, len(shapes)):
            b, sb = shapes[j]
            if moving_only and a.motion == b.motion == "fixed":
                continue
            ba, bb = bounds[i], bounds[j]
            # 面接触は干渉に数えない。圧入部はCAD上では公称径の面接触とする。
            if any(min(getattr(ba, ax + "max"), getattr(bb, ax + "max")) -
                   max(getattr(ba, ax + "min"), getattr(bb, ax + "min")) <= 1e-7 for ax in "xyz"):
                continue
            volume = sa.intersect(sb).Volume()
            if volume > 1e-5:
                collisions.append({"a": a.name, "b": b.name, "volume_mm3": volume})
    return collisions


def export_design(output: Path, p: Parameters, parts: dict[str, Part] | None = None) -> dict:
    p.validate()
    parts = build_parts(p) if parts is None else parts
    output.mkdir(parents=True, exist_ok=True)
    # 寸法を変更して再生成した際に、以前の干渉結果を残さない。
    (output / "motion_check.json").unlink(missing_ok=True)
    quantities = Counter(item.part for item in instances(p))
    manifest = {"units": "mm", "parameters": asdict(p), "stroke_mm": 2 * p.crank_radius,
                "assembly": "assembly.step", "parts": []}
    for name, part in parts.items():
        folder = output / ("hardware_reference" if part.purchased else "parts")
        folder.mkdir(exist_ok=True)
        path = folder / f"{name}.step"
        shape = part.shape.val()
        if len(shape.Solids()) != 1 or not shape.isValid() or shape.Volume() <= 0:
            raise RuntimeError(f"部品形状が不正です: {name}")
        cq.exporters.export(part.shape, str(path))
        bb = shape.BoundingBox()
        manifest["parts"].append({"id": name, "name_ja": part.label, "quantity": quantities[name],
                                  "material": part.material, "process": part.process,
                                  "purchased": part.purchased, "step": path.relative_to(output).as_posix(),
                                  "bbox_mm": [bb.xlen, bb.ylen, bb.zlen], "volume_mm3": shape.Volume()})
    make_assembly(parts, p).export(str(output / "assembly.step"))
    (output / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    bom = ["# 部品表", "", "単位：mm。市販ねじ形状は配置確認用。製作品の加工指示は ../DESIGN.md を参照。", "",
           "| ID | 部品名 | 数量 | 材料 | 加工・調達 |", "|---|---|---:|---|---|"]
    bom += [f"| {r['id']} | {r['name_ja']} | {r['quantity']} | {r['material']} | {r['process']} |"
            for r in manifest["parts"]]
    (output / "BOM.md").write_text("\n".join(bom) + "\n", encoding="utf-8")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path(__file__).parent / "output")
    parser.add_argument("--angle", type=float, default=45)
    parser.add_argument("--radius", type=float, default=30)
    parser.add_argument("--rod-length", type=float, default=120)
    parser.add_argument("--check-motion", action="store_true", help="15度間隔の実体干渉を検証")
    args = parser.parse_args()
    p = Parameters(args.radius, args.rod_length, args.angle)
    parts = build_parts(p)
    manifest = export_design(args.output, p, parts)
    from preview import export_preview
    export_preview(args.output, p, parts)
    print(f"STEP出力: {args.output.resolve()} / {len(manifest['parts'])}種類", flush=True)
    if args.check_motion:
        report = {"parameters": asdict(p), "method": "BRep common volume > 1e-5 mm3; nominal geometry", "angles_deg": list(range(0, 360, 15)),
                  "collisions": [], "continuous_collision_proof": False}
        for angle in report["angles_deg"]:
            hits = collision_pairs(parts, p, angle, moving_only=angle != 0)
            report["collisions"] += [{"angle_deg": angle, **h} for h in hits]
            print(f"干渉確認 {angle:3} deg: {len(hits)}件", flush=True)
        (args.output / "motion_check.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
        if report["collisions"]:
            raise RuntimeError("部品干渉があります。motion_check.jsonを確認してください。")


if __name__ == "__main__":
    main()
