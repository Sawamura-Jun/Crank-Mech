"""CadQueryの実形状から、外部通信不要の3D確認画面を生成する。"""

from __future__ import annotations

from dataclasses import asdict
import json
from pathlib import Path

from crank_model import Parameters, Part, instances


# プレビューだけを英語化し、日本語の部品表用ラベルは保持する。
PART_LABELS_EN = {
    "P01_base": "Base",
    "P02_guide_rail": "Guide rail with hold-down",
    "P03_end_stop": "End stop",
    "P04_crank_disk": "Crank disk",
    "P05_connecting_rod": "Connecting rod",
    "P06_slider": "Slider",
    "P07_main_post": "Fixed main shaft",
    "P08_joint_post": "Stepped shaft for connecting rod",
    "P09_grip_post": "Stepped shaft for hand grip",
    "P10_main_bush": "Main shaft bushing",
    "P11_link_bush": "Connecting rod bushing",
    "P12_hand_grip": "Revolving hand grip",
    "P13_retainer_M6": "Main shaft retaining washer",
    "P14_retainer_M5": "Small shaft retaining washer",
    "H_M6x40": "Hexagon socket head cap screw M6×40",
    "H_M5x30": "Hexagon socket head cap screw M5×30",
    "H_M5x12": "Hexagon socket head cap screw M5×12",
    "H_M5x25": "Hexagon socket head cap screw M5×25",
    "H_M5x50": "Hexagon socket head cap screw M5×50",
}


def export_preview(output: Path, p: Parameters, parts: dict[str, Part]) -> None:
    meshes = {}
    for name, part in parts.items():
        vertices, triangles = part.shape.val().tessellate(0.15, 0.20)
        # WebGLの面法線を面ごとに持たせ、平面の稜線を保持する。
        positions, normals = [], []
        for a, b, c in triangles:
            va, vb, vc = vertices[a], vertices[b], vertices[c]
            normal = (vb - va).cross(vc - va)
            if normal.Length < 1e-12:
                continue
            normal = normal.normalized()
            for v in (va, vb, vc):
                positions.extend(round(k, 5) for k in v.toTuple())
                normals.extend(round(k, 5) for k in normal.toTuple())
        meshes[name] = {"positions": positions, "normals": normals,
                        "color": part.color, "label": PART_LABELS_EN[name]}
    # インスタンスは角度0度の位置を基準に、ブラウザー側で剛体変換する。
    payload = {"parameters": asdict(p), "meshes": meshes,
               "instances": [asdict(item) for item in instances(p, 0)]}
    template_path = Path(__file__).parent / "templates" / "preview.html"
    template = template_path.read_text(encoding="utf-8")
    html = template.replace("__MODEL_DATA__", json.dumps(payload, ensure_ascii=False, separators=(",", ":")))
    (output / "preview.html").write_text(html, encoding="utf-8")
