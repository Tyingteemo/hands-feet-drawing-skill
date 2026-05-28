#!/usr/bin/env python3
"""
Generate an annotated foot reference SVG with construction lines and joint labels.

Usage:
    python generate_foot_svg.py --pose standing --foot right --view medial --output foot_ref.svg

Poses: standing, walking, dangling, tiptoe
Foot: left, right
View: medial, lateral, dorsal, plantar
"""

import argparse
import math
import os
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom

# Canonical joint coordinates (unit scale, right foot, medial view)
# x = posterior (-) to anterior (+), y = ground (0) to up (+)
FOOT_JOINTS = {
    "standing": {
        "heel_posterior": (0.0, 0.0),
        "calcaneus_top": (0.3, 0.7),
        "talus_ankle": (0.7, 1.1),
        "medial_malleolus": (0.65, 1.3),
        "navicular": (1.0, 0.8),
        "cuneiform": (1.3, 0.6),
        "mt1_base": (1.5, 0.4),
        "mt1_head": (1.8, 0.1),
        "mt5_head": (1.6, 0.0),
        "big_toe_mcp": (2.0, 0.15),
        "big_toe_ip": (2.2, 0.25),
        "big_toe_tip": (2.4, 0.3),
        "toe2_tip": (2.35, 0.25),
        "toe3_tip": (2.25, 0.2),
        "toe4_tip": (2.15, 0.15),
        "toe5_tip": (2.05, 0.1),
    },
    "walking": {
        "heel_posterior": (0.0, 0.1),
        "calcaneus_top": (0.3, 0.8),
        "talus_ankle": (0.7, 1.2),
        "medial_malleolus": (0.65, 1.4),
        "navicular": (1.0, 0.9),
        "cuneiform": (1.3, 0.7),
        "mt1_base": (1.5, 0.5),
        "mt1_head": (1.8, 0.2),
        "mt5_head": (1.6, 0.1),
        "big_toe_mcp": (2.0, 0.25),
        "big_toe_ip": (2.2, 0.35),
        "big_toe_tip": (2.4, 0.4),
        "toe2_tip": (2.35, 0.35),
        "toe3_tip": (2.25, 0.3),
        "toe4_tip": (2.15, 0.25),
        "toe5_tip": (2.05, 0.2),
    },
    "dangling": {
        "heel_posterior": (0.0, 0.3),
        "calcaneus_top": (0.3, 0.9),
        "talus_ankle": (0.7, 1.3),
        "medial_malleolus": (0.65, 1.5),
        "navicular": (1.0, 1.0),
        "cuneiform": (1.3, 0.8),
        "mt1_base": (1.5, 0.7),
        "mt1_head": (1.8, 0.5),
        "mt5_head": (1.6, 0.4),
        "big_toe_mcp": (2.0, 0.55),
        "big_toe_ip": (2.2, 0.6),
        "big_toe_tip": (2.4, 0.65),
        "toe2_tip": (2.35, 0.6),
        "toe3_tip": (2.25, 0.55),
        "toe4_tip": (2.15, 0.5),
        "toe5_tip": (2.05, 0.45),
    },
    "tiptoe": {
        "heel_posterior": (0.0, 1.5),
        "calcaneus_top": (0.3, 1.8),
        "talus_ankle": (0.7, 2.0),
        "medial_malleolus": (0.65, 2.2),
        "navicular": (1.0, 1.5),
        "cuneiform": (1.3, 1.2),
        "mt1_base": (1.5, 1.0),
        "mt1_head": (1.8, 0.5),
        "mt5_head": (1.6, 0.45),
        "big_toe_mcp": (2.0, 0.4),
        "big_toe_ip": (2.2, 0.3),
        "big_toe_tip": (2.4, 0.2),
        "toe2_tip": (2.35, 0.25),
        "toe3_tip": (2.25, 0.3),
        "toe4_tip": (2.15, 0.35),
        "toe5_tip": (2.05, 0.4),
    },
}

FOOT_CHAINS = {
    "heel_arch": ["heel_posterior", "calcaneus_top", "talus_ankle",
                   "navicular", "cuneiform", "mt1_base", "mt1_head"],
    "big_toe": ["mt1_head", "big_toe_mcp", "big_toe_ip", "big_toe_tip"],
    "toes_dorsal": ["big_toe_tip", "toe2_tip", "toe3_tip", "toe4_tip", "toe5_tip"],
}

JOINT_LABELS = {
    "heel_posterior": "",
    "calcaneus_top": "Calcaneus",
    "talus_ankle": "Talus",
    "medial_malleolus": "Med. Malleolus",
    "navicular": "Navicular",
    "cuneiform": "Cuneiform",
    "mt1_base": "MT1 Base",
    "mt1_head": "MT1 Head",
    "mt5_head": "MT5 Head",
    "big_toe_mcp": "MCP",
    "big_toe_ip": "IP",
    "big_toe_tip": "",
    "toe2_tip": "",
    "toe3_tip": "",
    "toe4_tip": "",
    "toe5_tip": "",
}


def prettify(elem):
    rough = tostring(elem, "utf-8")
    parsed = minidom.parseString(rough)
    return parsed.toprettyxml(indent="  ")


def create_svg(joints, foot_side, view, scale=80):
    """Create an SVG document with foot anatomy reference."""
    padding = 40
    svg_w = int(scale * 4 + padding * 2)
    svg_h = int(scale * 3.5 + padding * 2)

    svg = Element(
        "svg",
        xmlns="http://www.w3.org/2000/svg",
        viewBox=f"0 0 {svg_w} {svg_h}",
        width=str(svg_w),
        height=str(svg_h),
    )

    # Style
    style = Element("style")
    style.text = """
        .bone { stroke: #888; stroke-width: 1.5; fill: none; }
        .joint { fill: #e74c3c; }
        .arch-highlight { stroke: #e67e22; stroke-width: 2; fill: none; stroke-dasharray: 5,3; }
        .silhouette { fill: #f0d0b8; stroke: #c09070; stroke-width: 0.8; }
        .label { font-family: sans-serif; font-size: 9px; fill: #555; }
        .title { font-family: sans-serif; font-size: 14px; font-weight: bold; fill: #333; }
        .callout { font-family: sans-serif; font-size: 10px; fill: #2980b9; }
        .callout-line { stroke: #2980b9; stroke-width: 0.5; stroke-dasharray: 3,3; }
    """
    svg.append(style)

    def tx(point):
        x, y = point
        if foot_side == "left":
            x = -x
        sx = x * scale + svg_w * 0.2  # offset to fit
        sy = svg_h - padding - y * scale
        return sx, sy

    # Title
    title = SubElement(svg, "text", x=str(padding), y=str(padding + 15))
    title.set("class", "title")
    title.text = f"{foot_side.capitalize()} Foot — {view.capitalize()} View — Pose: {pose_name}"

    # Draw silhouette (foot outline)
    sil_pts = ["heel_posterior", "calcaneus_top", "talus_ankle",
               "navicular", "cuneiform", "mt1_base", "mt1_head",
               "big_toe_mcp", "big_toe_ip", "big_toe_tip",
               "toe2_tip", "toe3_tip", "toe4_tip", "toe5_tip"]
    pts = [tx(joints[p]) for p in sil_pts]

    # Add sole curve (from toe5_tip back to heel)
    sole_start = tx(joints["toe5_tip"])
    sole_end = tx(joints["heel_posterior"])

    sil = SubElement(svg, "path")
    sil.set("class", "silhouette")
    d_parts = [f"M {pts[0][0]},{pts[0][1]}"]
    for p in pts[1:]:
        d_parts.append(f"L {p[0]},{p[1]}")
    # Sole curve back
    d_parts.append(f"Q {(sole_start[0] + sole_end[0]) / 2},{sole_start[1] + 5} {sole_end[0]},{sole_end[1]}")
    d_parts.append("Z")
    sil.set("d", " ".join(d_parts))

    # Draw bones (connecting chains)
    for chain_name, chain in FOOT_CHAINS.items():
        pts_chain = [tx(joints[p]) for p in chain]
        for i in range(len(pts_chain) - 1):
            line = SubElement(svg, "line")
            line.set("class", "bone")
            line.set("x1", str(pts_chain[i][0]))
            line.set("y1", str(pts_chain[i][1]))
            line.set("x2", str(pts_chain[i + 1][0]))
            line.set("y2", str(pts_chain[i + 1][1]))
            svg.append(line)

    # Highlight the medial longitudinal arch
    arch_pts_names = ["calcaneus_top", "talus_ankle", "navicular", "cuneiform", "mt1_head"]
    arch_pts = [tx(joints[p]) for p in arch_pts_names]
    arch = SubElement(svg, "path")
    arch.set("class", "arch-highlight")
    d = f"M {arch_pts[0][0]},{arch_pts[0][1]}"
    for p in arch_pts[1:]:
        d += f" L {p[0]},{p[1]}"
    arch.set("d", d)
    svg.append(arch)

    # Arch callout
    mid_arch = arch_pts[len(arch_pts) // 2]
    ac = SubElement(svg, "text")
    ac.set("class", "callout")
    ac.set("x", str(mid_arch[0] - 20))
    ac.set("y", str(mid_arch[1] - 10))
    ac.text = "← Medial Longitudinal Arch →"
    svg.append(ac)

    # Draw joints
    for name, point in joints.items():
        x, y = tx(point)
        circle = SubElement(svg, "circle")
        circle.set("class", "joint")
        r = 3 if name.endswith("head") or name.startswith("talus") or name.endswith("ankle") else 2.5
        circle.set("r", str(r))
        circle.set("cx", str(x))
        circle.set("cy", str(y))
        svg.append(circle)

        label_text = JOINT_LABELS.get(name, "")
        if label_text:
            lbl = SubElement(svg, "text")
            lbl.set("class", "label")
            lbl.set("x", str(x + 4))
            lbl.set("y", str(y + 3))
            lbl.text = label_text
            svg.append(lbl)

    # Weight-bearing callout
    if pose_name == "standing":
        heel_pt = tx(joints["heel_posterior"])
        mt1 = tx(joints["mt1_head"])
        mt5 = tx(joints["mt5_head"])

        wt = SubElement(svg, "text")
        wt.set("class", "callout")
        wt.set("x", str(heel_pt[0] - 5))
        wt.set("y", str(heel_pt[1] + 20))
        wt.text = "▲ Heel (weight)"
        svg.append(wt)

        wt2 = SubElement(svg, "text")
        wt2.set("class", "callout")
        wt2.set("x", str(mt1[0] - 10))
        wt2.set("y", str(mt1[1] + 20))
        wt2.text = "▲ Ball (weight)"
        svg.append(wt2)

    return svg


def main():
    parser = argparse.ArgumentParser(description="Generate foot reference SVG")
    parser.add_argument("--pose", default="standing",
                        choices=list(FOOT_JOINTS.keys()),
                        help="Foot pose")
    parser.add_argument("--foot", default="right", choices=["left", "right"],
                        help="Left or right foot")
    parser.add_argument("--view", default="medial",
                        choices=["medial", "lateral", "dorsal", "plantar"],
                        help="View angle")
    parser.add_argument("--output", default=None,
                        help="Output SVG file path")
    args = parser.parse_args()

    global pose_name
    pose_name = args.pose

    joints = FOOT_JOINTS[args.pose]
    svg = create_svg(joints, args.foot, args.view)

    output_path = args.output or f"{args.pose}_{args.foot}_foot.svg"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(prettify(svg))

    print(f"Foot reference saved to: {output_path}")


if __name__ == "__main__":
    main()
