#!/usr/bin/env python3
"""
Generate an annotated foot reference SVG with construction lines and joint labels.

Usage:
    python generate_foot_svg.py --pose standing --foot right --view medial --output foot_ref.svg

Poses: standing, walking, dangling, tiptoe
"""

import argparse
import math
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom

FOOT_JOINTS = {
    "standing": {
        "heel_posterior": (0.0, 0.0), "calcaneus_top": (0.3, 0.7), "talus_ankle": (0.7, 1.1),
        "medial_malleolus": (0.65, 1.3), "navicular": (1.0, 0.8), "cuneiform": (1.3, 0.6),
        "mt1_base": (1.5, 0.4), "mt1_head": (1.8, 0.1), "mt5_head": (1.6, 0.0),
        "big_toe_mcp": (2.0, 0.15), "big_toe_ip": (2.2, 0.25), "big_toe_tip": (2.4, 0.3),
        "toe2_tip": (2.35, 0.25), "toe3_tip": (2.25, 0.2), "toe4_tip": (2.15, 0.15), "toe5_tip": (2.05, 0.1),
    },
    "walking": {
        "heel_posterior": (0.0, 0.1), "calcaneus_top": (0.3, 0.8), "talus_ankle": (0.7, 1.2),
        "medial_malleolus": (0.65, 1.4), "navicular": (1.0, 0.9), "cuneiform": (1.3, 0.7),
        "mt1_base": (1.5, 0.5), "mt1_head": (1.8, 0.2), "mt5_head": (1.6, 0.1),
        "big_toe_mcp": (2.0, 0.25), "big_toe_ip": (2.2, 0.35), "big_toe_tip": (2.4, 0.4),
        "toe2_tip": (2.35, 0.35), "toe3_tip": (2.25, 0.3), "toe4_tip": (2.15, 0.25), "toe5_tip": (2.05, 0.2),
    },
    "dangling": {
        "heel_posterior": (0.0, 0.3), "calcaneus_top": (0.3, 0.9), "talus_ankle": (0.7, 1.3),
        "medial_malleolus": (0.65, 1.5), "navicular": (1.0, 1.0), "cuneiform": (1.3, 0.8),
        "mt1_base": (1.5, 0.7), "mt1_head": (1.8, 0.5), "mt5_head": (1.6, 0.4),
        "big_toe_mcp": (2.0, 0.55), "big_toe_ip": (2.2, 0.6), "big_toe_tip": (2.4, 0.65),
        "toe2_tip": (2.35, 0.6), "toe3_tip": (2.25, 0.55), "toe4_tip": (2.15, 0.5), "toe5_tip": (2.05, 0.45),
    },
    "tiptoe": {
        "heel_posterior": (0.0, 1.5), "calcaneus_top": (0.3, 1.8), "talus_ankle": (0.7, 2.0),
        "medial_malleolus": (0.65, 2.2), "navicular": (1.0, 1.5), "cuneiform": (1.3, 1.2),
        "mt1_base": (1.5, 1.0), "mt1_head": (1.8, 0.5), "mt5_head": (1.6, 0.45),
        "big_toe_mcp": (2.0, 0.4), "big_toe_ip": (2.2, 0.3), "big_toe_tip": (2.4, 0.2),
        "toe2_tip": (2.35, 0.25), "toe3_tip": (2.25, 0.3), "toe4_tip": (2.15, 0.35), "toe5_tip": (2.05, 0.4),
    },
}

BONE_CHAINS = {
    "arch": ["calcaneus_top", "talus_ankle", "navicular", "cuneiform", "mt1_base", "mt1_head"],
    "toe": ["mt1_head", "big_toe_mcp", "big_toe_ip", "big_toe_tip"],
}

ARCH_PTS = ["calcaneus_top", "talus_ankle", "navicular", "cuneiform", "mt1_head"]

LABELS = {
    "heel_posterior": None, "calcaneus_top": "Calcaneus", "talus_ankle": "Talus",
    "medial_malleolus": "Med.Malleolus", "navicular": "Navicular", "cuneiform": "Cuneiform",
    "mt1_base": "MT1 Base", "mt1_head": "MT1 Head", "mt5_head": "MT5 Head",
    "big_toe_mcp": "MCP", "big_toe_ip": "IP",
}


def prettify(elem):
    return minidom.parseString(tostring(elem, "utf-8")).toprettyxml(indent="  ")


def s(parent, tag, cls=None, **attrs):
    e = SubElement(parent, tag)
    if cls:
        e.set("class", cls)
    for k, v in attrs.items():
        e.set(k, str(v))
    return e


def create_svg(joints, foot_side, view, scale=80):
    padding = 40
    svg_w = int(scale * 4 + padding * 2)
    svg_h = int(scale * 3.5 + padding * 2)
    ox = svg_w * 0.15

    svg = Element("svg", xmlns="http://www.w3.org/2000/svg",
                  viewBox=f"0 0 {svg_w} {svg_h}",
                  width=str(svg_w), height=str(svg_h))

    sty = SubElement(svg, "style")
    sty.text = """
        .bone { stroke:#888; stroke-width:1.5; fill:none; }
        .joint { fill:#e74c3c; stroke:#fff; stroke-width:.5; }
        .joint-sm { fill:#e67e22; stroke:#fff; stroke-width:.5; }
        .arch-highlight { stroke:#e67e22; stroke-width:2.5; fill:none; stroke-dasharray:6,4; }
        .silhouette { fill:#f0d0b8; stroke:#c09070; stroke-width:.8; }
        .label { font-family:sans-serif; font-size:9px; fill:#444; }
        .title { font-family:sans-serif; font-size:14px; font-weight:bold; fill:#333; }
        .callout { font-family:sans-serif; font-size:10px; fill:#2980b9; }
    """

    def tx(point):
        x, y = point
        if foot_side == "left":
            x = -x
        return x * scale + ox, svg_h - padding - y * scale

    s(svg, "text", "title", x=str(padding), y=str(padding + 15)).text = \
        f"{foot_side.capitalize()} Foot - {view.capitalize()} View - Pose: {pose_name}"

    # Joint positions
    hp = tx(joints["heel_posterior"])
    ct = tx(joints["calcaneus_top"])
    ta = tx(joints["talus_ankle"])
    na = tx(joints["navicular"])
    cu = tx(joints["cuneiform"])
    m1 = tx(joints["mt1_head"])
    m5 = tx(joints["mt5_head"])
    bm = tx(joints["big_toe_mcp"])
    bi = tx(joints["big_toe_ip"])
    bt = tx(joints["big_toe_tip"])
    t5 = tx(joints["toe5_tip"]) if "toe5_tip" in joints else bt

    # Dorsal curve points
    dors_pts = [hp, ct, ta, na, cu, m1, bm, bi, bt]

    # Foot silhouette: dorsal + toe arc + sole back to heel
    dp = [f"M {dors_pts[0][0]},{dors_pts[0][1]}"]
    for i in range(1, len(dors_pts)):
        mx = (dors_pts[i - 1][0] + dors_pts[i][0]) / 2
        my = (dors_pts[i - 1][1] + dors_pts[i][1]) / 2
        dp.append(f"Q {dors_pts[i][0]},{dors_pts[i][1]} {mx},{my}")

    # Toe tips
    for tip_name in ["toe2_tip", "toe3_tip", "toe4_tip", "toe5_tip"]:
        if tip_name in joints:
            pt = tx(joints[tip_name])
            dp.append(f"Q {(bt[0]+pt[0])/2},{bt[1]} {pt[0]},{pt[1]}")

    # Sole curve back to heel
    sole_mid = ((t5[0] + hp[0]) / 2, t5[1] + scale * 0.04)
    dp.append(f"Q {sole_mid[0]},{sole_mid[1]} {hp[0]},{hp[1]} Z")
    s(svg, "path", "silhouette", d=" ".join(dp))

    # Bones
    for chain in BONE_CHAINS.values():
        pts = [tx(joints[p]) for p in chain if p in joints]
        for i in range(len(pts) - 1):
            s(svg, "line", "bone",
              x1=str(pts[i][0]), y1=str(pts[i][1]),
              x2=str(pts[i + 1][0]), y2=str(pts[i + 1][1]))
    # Heel to calcaneus
    s(svg, "line", "bone",
      x1=str(hp[0]), y1=str(hp[1]),
      x2=str(ct[0]), y2=str(ct[1]))

    # Arch highlight
    arch_pts = [tx(joints[p]) for p in ARCH_PTS if p in joints]
    if arch_pts:
        ad = f"M {arch_pts[0][0]},{arch_pts[0][1]}"
        for p in arch_pts[1:]:
            ad += f" L {p[0]},{p[1]}"
        s(svg, "path", "arch-highlight", d=ad)

    # Joints
    for name, point in joints.items():
        x, y = tx(point)
        major = name.startswith("talus") or name.endswith("head") or name == "medial_malleolus"
        s(svg, "circle", "joint" if major else "joint-sm",
          r=str(3.5 if major else 2.5), cx=str(x), cy=str(y))
        lbl = LABELS.get(name)
        if lbl:
            s(svg, "text", "label", x=str(x + 6), y=str(y + 3)).text = lbl

    # Callouts
    if arch_pts:
        mid_a = arch_pts[len(arch_pts) // 2]
        s(svg, "text", "callout", x=str(mid_a[0] - 25), y=str(mid_a[1] - 10)).text = "Medial Arch"
    if pose_name == "standing":
        s(svg, "text", "callout", x=str(hp[0]), y=str(hp[1] + 18)).text = "Heel"
        s(svg, "text", "callout", x=str(m1[0] - 8), y=str(m1[1] + 18)).text = "Ball"
    mm = tx(joints["medial_malleolus"])
    s(svg, "text", "callout", x=str(mm[0] - 15), y=str(mm[1] - 10)).text = "Inner ankle (higher)"

    return svg


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pose", default="standing", choices=list(FOOT_JOINTS.keys()))
    ap.add_argument("--foot", default="right", choices=["left", "right"])
    ap.add_argument("--view", default="medial", choices=["medial", "lateral", "dorsal", "plantar"])
    ap.add_argument("--output", default=None)
    args = ap.parse_args()

    global pose_name
    pose_name = args.pose

    out = args.output or f"{args.pose}_{args.foot}_foot.svg"
    with open(out, "w", encoding="utf-8") as f:
        f.write(prettify(create_svg(FOOT_JOINTS[args.pose], args.foot, args.view)))
    print(f"Foot reference saved to: {out}")


if __name__ == "__main__":
    main()
