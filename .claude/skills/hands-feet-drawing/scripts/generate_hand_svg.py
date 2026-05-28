#!/usr/bin/env python3
"""
Generate an annotated hand reference SVG with construction lines and joint labels.

Usage:
    python generate_hand_svg.py --pose relaxed_open --hand right --view palm --output hand_ref.svg

Poses: relaxed_open, fist, pointing, grasping, spread
Hand: left, right
View: palm, dorsal, side
"""

import argparse
import math
import os
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom

# Canonical joint coordinates (unit scale, right hand, palm forward)
# x = ulnar (-) to radial (+), y = proximal (-) to distal (+)
HAND_JOINTS = {
    "relaxed_open": {
        "wrist": (0.0, 0.0),
        "palm_center": (0.0, 0.6),
        "thumb_cmc": (-0.7, 0.4),
        "thumb_mcp": (-0.9, 0.8),
        "thumb_ip": (-0.8, 1.2),
        "thumb_tip": (-0.65, 1.5),
        "index_mcp": (-0.35, 1.3),
        "index_pip": (-0.3, 2.0),
        "index_dip": (-0.25, 2.5),
        "index_tip": (-0.22, 2.85),
        "middle_mcp": (0.0, 1.35),
        "middle_pip": (0.0, 2.1),
        "middle_dip": (0.0, 2.65),
        "middle_tip": (0.0, 3.0),
        "ring_mcp": (0.35, 1.3),
        "ring_pip": (0.3, 2.0),
        "ring_dip": (0.25, 2.5),
        "ring_tip": (0.22, 2.8),
        "pinky_mcp": (0.6, 1.15),
        "pinky_pip": (0.5, 1.7),
        "pinky_dip": (0.42, 2.0),
        "pinky_tip": (0.38, 2.25),
    },
    "fist": {
        "wrist": (0.0, 0.0),
        "palm_center": (0.0, 0.6),
        "thumb_cmc": (-0.7, 0.4),
        "thumb_mcp": (-0.8, 0.7),
        "thumb_ip": (-0.6, 0.9),
        "thumb_tip": (-0.4, 1.0),
        "index_mcp": (-0.35, 1.3),
        "index_pip": (-0.25, 1.7),
        "index_dip": (-0.15, 1.9),
        "index_tip": (-0.1, 2.0),
        "middle_mcp": (0.0, 1.35),
        "middle_pip": (0.0, 1.8),
        "middle_dip": (0.05, 2.0),
        "middle_tip": (0.05, 2.1),
        "ring_mcp": (0.35, 1.3),
        "ring_pip": (0.3, 1.7),
        "ring_dip": (0.25, 1.9),
        "ring_tip": (0.2, 2.0),
        "pinky_mcp": (0.6, 1.15),
        "pinky_pip": (0.5, 1.5),
        "pinky_dip": (0.42, 1.7),
        "pinky_tip": (0.38, 1.8),
    },
    "pointing": {
        "wrist": (0.0, 0.0),
        "palm_center": (0.0, 0.6),
        "thumb_cmc": (-0.7, 0.4),
        "thumb_mcp": (-0.85, 0.7),
        "thumb_ip": (-0.7, 1.0),
        "thumb_tip": (-0.55, 1.15),
        "index_mcp": (-0.35, 1.3),
        "index_pip": (-0.35, 2.0),
        "index_dip": (-0.3, 2.5),
        "index_tip": (-0.28, 2.85),
        "middle_mcp": (0.0, 1.35),
        "middle_pip": (0.05, 1.7),
        "middle_dip": (0.1, 1.9),
        "middle_tip": (0.1, 2.0),
        "ring_mcp": (0.35, 1.3),
        "ring_pip": (0.3, 1.65),
        "ring_dip": (0.25, 1.85),
        "ring_tip": (0.2, 1.95),
        "pinky_mcp": (0.6, 1.15),
        "pinky_pip": (0.5, 1.45),
        "pinky_dip": (0.42, 1.65),
        "pinky_tip": (0.38, 1.75),
    },
    "spread": {
        "wrist": (0.0, 0.0),
        "palm_center": (0.0, 0.6),
        "thumb_cmc": (-0.9, 0.2),
        "thumb_mcp": (-1.2, 0.5),
        "thumb_ip": (-1.15, 1.0),
        "thumb_tip": (-1.0, 1.3),
        "index_mcp": (-0.45, 1.25),
        "index_pip": (-0.5, 2.0),
        "index_dip": (-0.45, 2.5),
        "index_tip": (-0.42, 2.8),
        "middle_mcp": (0.0, 1.35),
        "middle_pip": (0.0, 2.1),
        "middle_dip": (0.0, 2.65),
        "middle_tip": (0.0, 3.0),
        "ring_mcp": (0.5, 1.25),
        "ring_pip": (0.55, 2.0),
        "ring_dip": (0.5, 2.5),
        "ring_tip": (0.45, 2.8),
        "pinky_mcp": (0.9, 1.05),
        "pinky_pip": (0.95, 1.6),
        "pinky_dip": (0.9, 2.0),
        "pinky_tip": (0.85, 2.2),
    },
}

FINGER_CHAINS = {
    "thumb": ["thumb_cmc", "thumb_mcp", "thumb_ip", "thumb_tip"],
    "index": ["index_mcp", "index_pip", "index_dip", "index_tip"],
    "middle": ["middle_mcp", "middle_pip", "middle_dip", "middle_tip"],
    "ring": ["ring_mcp", "ring_pip", "ring_dip", "ring_tip"],
    "pinky": ["pinky_mcp", "pinky_pip", "pinky_dip", "pinky_tip"],
}

JOINT_LABELS = {
    "wrist": "Wrist",
    "thumb_cmc": "CMC",
    "thumb_mcp": "MCP",
    "thumb_ip": "IP",
    "index_mcp": "MCP",
    "index_pip": "PIP",
    "index_dip": "DIP",
    "middle_mcp": "MCP",
    "middle_pip": "PIP",
    "middle_dip": "DIP",
    "ring_mcp": "MCP",
    "ring_pip": "PIP",
    "ring_dip": "DIP",
    "pinky_mcp": "MCP",
    "pinky_pip": "PIP",
    "pinky_dip": "DIP",
}


def prettify(elem):
    rough = tostring(elem, "utf-8")
    parsed = minidom.parseString(rough)
    return parsed.toprettyxml(indent="  ")


def create_svg(joints, hand_side, view, scale=80):
    """Create an SVG document with hand anatomy reference."""
    padding = 40
    svg_w = int(scale * 4.5 + padding * 2)
    svg_h = int(scale * 4 + padding * 2)

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
        .silhouette { fill: #f5d5c5; stroke: #c09070; stroke-width: 0.8; }
        .label { font-family: sans-serif; font-size: 9px; fill: #555; }
        .title { font-family: sans-serif; font-size: 14px; font-weight: bold; fill: #333; }
        .callout { font-family: sans-serif; font-size: 10px; fill: #2980b9; }
        .callout-line { stroke: #2980b9; stroke-width: 0.5; stroke-dasharray: 3,3; }
    """
    svg.append(style)

    def tx(point):
        """Transform joint coordinates to SVG coordinates."""
        x, y = point
        # Flip x for left hand
        if hand_side == "left":
            x = -x
        sx = x * scale + svg_w / 2
        sy = y * scale + padding
        return sx, sy

    # Title
    title = SubElement(svg, "text", x=str(padding), y=str(padding + 15))
    title.set("class", "title")
    title.text = f"{hand_side.capitalize()} Hand — {view.capitalize()} View — Pose: {pose_name}"

    # Draw silhouette (palm outline)
    palm_pts = ["wrist", "index_mcp", "middle_mcp", "ring_mcp", "pinky_mcp"]
    if hand_side == "left":
        palm_pts = ["wrist", "pinky_mcp", "ring_mcp", "middle_mcp", "index_mcp"]

    palm_corners = [tx(joints[p]) for p in palm_pts]
    # Add thumb side and pinky side anchors
    thumb_cmc = tx(joints["thumb_cmc"])
    pinky_mcp = tx(joints["pinky_mcp"])

    sil = SubElement(svg, "path")
    sil.set("class", "silhouette")
    d_parts = [f"M {thumb_cmc[0]},{thumb_cmc[1]}"]
    d_parts.append(f"L {palm_corners[0][0]},{palm_corners[0][1]}")
    for c in palm_corners[1:]:
        d_parts.append(f"L {c[0]},{c[1]}")
    d_parts.append(f"L {pinky_mcp[0]},{pinky_mcp[1]}")
    d_parts.append("Z")
    sil.set("d", " ".join(d_parts))

    # Draw finger silhouettes (quick tapered cylinders)
    for finger_name, chain in FINGER_CHAINS.items():
        pts = [tx(joints[p]) for p in chain]
        if len(pts) < 2:
            continue
        # Taper: wider at MCP, narrower at tip
        mcp_w = scale * 0.14  # ~1.1cm at MCP
        tip_w = scale * 0.07  # ~0.55cm at tip
        # For thumb: wider
        if finger_name == "thumb":
            mcp_w = scale * 0.17
            tip_w = scale * 0.09

        # Build silhouette path along the chain
        # Perpendicular offset at each joint
        path_pts_left = []
        path_pts_right = []
        for i, (x, y) in enumerate(pts):
            if i < len(pts) - 1:
                dx = pts[i + 1][0] - x
                dy = pts[i + 1][1] - y
            else:
                dx = x - pts[i - 1][0]
                dy = y - pts[i - 1][1]
            length = math.hypot(dx, dy)
            if length == 0:
                continue
            nx = -dy / length
            ny = dx / length
            frac = i / max(len(pts) - 1, 1)
            w = mcp_w + (tip_w - mcp_w) * frac
            path_pts_left.append((x + nx * w, y + ny * w))
            path_pts_right.append((x - nx * w, y - ny * w))

        # Build finger silhouette path
        d_parts = [f"M {path_pts_left[0][0]},{path_pts_left[0][1]}"]
        for p in path_pts_left:
            d_parts.append(f"L {p[0]},{p[1]}")
        for p in reversed(path_pts_right):
            d_parts.append(f"L {p[0]},{p[1]}")
        d_parts.append("Z")

        finger_sil = SubElement(svg, "path")
        finger_sil.set("class", "silhouette")
        finger_sil.set("d", " ".join(d_parts))

    # Draw bones (connecting lines)
    for finger_name, chain in FINGER_CHAINS.items():
        pts = [tx(joints[p]) for p in chain]
        for i in range(len(pts) - 1):
            line = SubElement(svg, "line")
            line.set("class", "bone")
            line.set("x1", str(pts[i][0]))
            line.set("y1", str(pts[i][1]))
            line.set("x2", str(pts[i + 1][0]))
            line.set("y2", str(pts[i + 1][1]))
            svg.append(line)

    # Draw wrist to palm connection
    wrist = tx(joints["wrist"])
    palm_c = tx(joints["palm_center"])
    wrist_line = SubElement(svg, "line")
    wrist_line.set("class", "bone")
    wrist_line.set("x1", str(wrist[0]))
    wrist_line.set("y1", str(wrist[1]))
    wrist_line.set("x2", str(palm_c[0]))
    wrist_line.set("y2", str(palm_c[1]))
    svg.append(wrist_line)

    # Draw palm to MCP joints
    for p_name in ["thumb_mcp", "index_mcp", "middle_mcp", "ring_mcp", "pinky_mcp"]:
        pt = tx(joints[p_name])
        line = SubElement(svg, "line")
        line.set("class", "bone")
        line.set("x1", str(palm_c[0]))
        line.set("y1", str(palm_c[1]))
        line.set("x2", str(pt[0]))
        line.set("y2", str(pt[1]))
        svg.append(line)

    # Draw joints as circles with labels
    for name, point in joints.items():
        x, y = tx(point)
        circle = SubElement(svg, "circle")
        circle.set("class", "joint")
        r = 3 if name.endswith("mcp") or name == "wrist" or name == "thumb_cmc" else 2.5
        circle.set("r", str(r))
        circle.set("cx", str(x))
        circle.set("cy", str(y))
        svg.append(circle)

        # Label
        label_text = JOINT_LABELS.get(name, "")
        if label_text:
            lbl = SubElement(svg, "text")
            lbl.set("class", "label")
            lbl.set("x", str(x + 4))
            lbl.set("y", str(y + 3))
            lbl.text = label_text
            svg.append(lbl)

        # Joint name (full)
        lbl2 = SubElement(svg, "text")
        lbl2.set("class", "label")
        lbl2.set("x", str(x + 4))
        lbl2.set("y", str(y + 13))
        lbl2.text = name.replace("_", " ").title()
        svg.append(lbl2)

    # Callout: MCP arc
    mcp_names = ["index_mcp", "middle_mcp", "ring_mcp", "pinky_mcp"]
    mcp_pts = [tx(joints[n]) for n in mcp_names]
    arc_line = SubElement(svg, "path")
    arc_line.set("class", "callout-line")
    d = f"M {mcp_pts[0][0]},{mcp_pts[0][1]}"
    for p in mcp_pts[1:]:
        d += f" L {p[0]},{p[1]}"
    arc_line.set("d", d)
    svg.append(arc_line)

    # Callout label: Knuckle Arc
    mid = mcp_pts[len(mcp_pts) // 2]
    cl = SubElement(svg, "text")
    cl.set("class", "callout")
    cl.set("x", str(mid[0] - 25))
    cl.set("y", str(mid[1] - 8))
    cl.text = "← Knuckle Arc →"
    svg.append(cl)

    # Callout: finger length cascade
    tips = {
        "Index": tx(joints["index_tip"]),
        "Middle": tx(joints["middle_tip"]),
        "Ring": tx(joints["ring_tip"]),
        "Pinky": tx(joints["pinky_tip"]),
    }
    max_y = max(y for _, y in tips.values())
    cl2 = SubElement(svg, "text")
    cl2.set("class", "callout")
    cl2.set("x", str(tx(joints["wrist"])[0] - 30))
    cl2.set("y", str(padding))
    cl2.text = "Length: Middle > Ring > Index > Pinky"
    svg.append(cl2)

    return svg


def main():
    parser = argparse.ArgumentParser(description="Generate hand reference SVG")
    parser.add_argument("--pose", default="relaxed_open",
                        choices=list(HAND_JOINTS.keys()),
                        help="Hand pose")
    parser.add_argument("--hand", default="right", choices=["left", "right"],
                        help="Left or right hand")
    parser.add_argument("--view", default="palm", choices=["palm", "dorsal", "side"],
                        help="View angle")
    parser.add_argument("--output", default=None,
                        help="Output SVG file path")
    args = parser.parse_args()

    global pose_name
    pose_name = args.pose

    joints = HAND_JOINTS[args.pose]
    svg = create_svg(joints, args.hand, args.view)

    output_path = args.output or f"{args.pose}_{args.hand}_hand.svg"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(prettify(svg))

    print(f"Hand reference saved to: {output_path}")


if __name__ == "__main__":
    main()
