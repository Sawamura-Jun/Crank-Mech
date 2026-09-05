"""CadQueryの組立をローカル画像へ描画し、形状確認に使用する。"""

from pathlib import Path

from cadquery.vis import show

from crank_model import Parameters, build_parts, make_assembly


def main() -> None:
    p = Parameters()
    assembly = make_assembly(build_parts(p), p)
    output = Path(__file__).parent / "output"
    output.mkdir(exist_ok=True)
    # GUI操作や外部サイトへの送信をせず、同じCAD形状を描画する。
    for name, position, up in [
        ("assembly_preview.png", (210, -320, 300), (0, 0, 1)),
        ("assembly_top.png", (70, 0, 400), (0, 1, 0)),
    ]:
        show(assembly, interact=False, screenshot=str(output / name),
             width=1400, height=900, trihedron=False, edges=False,
             bgcolor=(0.96, 0.975, 0.985), gradient=False,
             position=position, focus=(70, 0, 20), viewup=up,
             orthographic=True, zoom=0.01, roll=0, elevation=0, azimuth=0, fxaa=True)
        print(f"画像出力: {output / name}", flush=True)


if __name__ == "__main__":
    main()
