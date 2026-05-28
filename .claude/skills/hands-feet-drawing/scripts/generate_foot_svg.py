#!/usr/bin/env python3
"""
Generate an annotated foot reference SVG — realistic or manga (14yo loli) style.

Usage:
    python generate_foot_svg.py --style manga --pose standing --foot right --output foot.svg

Styles: realistic (adult proportions), manga (14yo soft proportions)
Poses: standing, walking, dangling, tiptoe
"""

import argparse
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.etree.ElementTree import indent as et_indent


# === REALISTIC (ADULT) ===
FOOT_JOINTS_ADULT = {
    "standing": dict(
        heel_posterior=(0.0, 0.0), calcaneus_top=(0.3, 0.7), talus_ankle=(0.7, 1.1),
        medial_malleolus=(0.65, 1.3), navicular=(1.0, 0.8), cuneiform=(1.3, 0.6),
        mt1_base=(1.5, 0.4), mt1_head=(1.8, 0.1), mt5_head=(1.6, 0.1),
        big_toe_mcp=(2.0, 0.15), big_toe_ip=(2.2, 0.25), big_toe_tip=(2.4, 0.3),
        toe2_tip=(2.35, 0.25), toe3_tip=(2.25, 0.2), toe4_tip=(2.15, 0.15), toe5_tip=(2.05, 0.1),
    ),
    "walking": dict(
        heel_posterior=(0.0, 0.1), calcaneus_top=(0.3, 0.8), talus_ankle=(0.7, 1.2),
        medial_malleolus=(0.65, 1.4), navicular=(1.0, 0.9), cuneiform=(1.3, 0.7),
        mt1_base=(1.5, 0.5), mt1_head=(1.8, 0.2), mt5_head=(1.6, 0.2),
        big_toe_mcp=(2.0, 0.25), big_toe_ip=(2.2, 0.35), big_toe_tip=(2.4, 0.4),
        toe2_tip=(2.35, 0.35), toe3_tip=(2.25, 0.3), toe4_tip=(2.15, 0.25), toe5_tip=(2.05, 0.2),
    ),
    "dangling": dict(
        heel_posterior=(0.0, 0.3), calcaneus_top=(0.3, 0.9), talus_ankle=(0.7, 1.3),
        medial_malleolus=(0.65, 1.5), navicular=(1.0, 1.0), cuneiform=(1.3, 0.8),
        mt1_base=(1.5, 0.7), mt1_head=(1.8, 0.5), mt5_head=(1.6, 0.4),
        big_toe_mcp=(2.0, 0.55), big_toe_ip=(2.2, 0.6), big_toe_tip=(2.4, 0.65),
        toe2_tip=(2.35, 0.6), toe3_tip=(2.25, 0.55), toe4_tip=(2.15, 0.5), toe5_tip=(2.05, 0.45),
    ),
    "tiptoe": dict(
        heel_posterior=(0.0, 1.5), calcaneus_top=(0.3, 1.8), talus_ankle=(0.7, 2.0),
        medial_malleolus=(0.65, 2.2), navicular=(1.0, 1.5), cuneiform=(1.3, 1.2),
        mt1_base=(1.5, 1.0), mt1_head=(1.8, 0.5), mt5_head=(1.6, 0.45),
        big_toe_mcp=(2.0, 0.4), big_toe_ip=(2.2, 0.3), big_toe_tip=(2.4, 0.2),
        toe2_tip=(2.35, 0.25), toe3_tip=(2.25, 0.3), toe4_tip=(2.15, 0.35), toe5_tip=(2.05, 0.4),
    ),
}

# === MANGA (14YO LOLI) — ~10% smaller, softer, lower arch ===
FOOT_JOINTS_MANGA = {
    "standing": dict(
        heel_posterior=(0.0, 0.0), calcaneus_top=(0.25, 0.6), talus_ankle=(0.6, 1.0),
        medial_malleolus=(0.55, 1.15), navicular=(0.9, 0.7), cuneiform=(1.2, 0.55),
        mt1_base=(1.4, 0.4), mt1_head=(1.65, 0.1), mt5_head=(1.45, 0.1),
        big_toe_mcp=(1.8, 0.15), big_toe_ip=(1.95, 0.2), big_toe_tip=(2.1, 0.25),
        toe2_tip=(2.05, 0.2), toe3_tip=(1.95, 0.15), toe4_tip=(1.85, 0.1), toe5_tip=(1.75, 0.05),
    ),
    "walking": dict(
        heel_posterior=(0.0, 0.1), calcaneus_top=(0.25, 0.7), talus_ankle=(0.6, 1.1),
        medial_malleolus=(0.55, 1.25), navicular=(0.9, 0.8), cuneiform=(1.2, 0.65),
        mt1_base=(1.4, 0.5), mt1_head=(1.65, 0.2), mt5_head=(1.45, 0.2),
        big_toe_mcp=(1.8, 0.25), big_toe_ip=(1.95, 0.3), big_toe_tip=(2.1, 0.35),
        toe2_tip=(2.05, 0.3), toe3_tip=(1.95, 0.25), toe4_tip=(1.85, 0.2), toe5_tip=(1.75, 0.15),
    ),
    "dangling": dict(
        heel_posterior=(0.0, 0.3), calcaneus_top=(0.25, 0.8), talus_ankle=(0.6, 1.2),
        medial_malleolus=(0.55, 1.35), navicular=(0.9, 0.9), cuneiform=(1.2, 0.75),
        mt1_base=(1.4, 0.65), mt1_head=(1.65, 0.45), mt5_head=(1.45, 0.35),
        big_toe_mcp=(1.8, 0.5), big_toe_ip=(1.95, 0.55), big_toe_tip=(2.1, 0.6),
        toe2_tip=(2.05, 0.55), toe3_tip=(1.95, 0.5), toe4_tip=(1.85, 0.45), toe5_tip=(1.75, 0.4),
    ),
    "tiptoe": dict(
        heel_posterior=(0.0, 1.3), calcaneus_top=(0.25, 1.6), talus_ankle=(0.6, 1.8),
        medial_malleolus=(0.55, 1.95), navicular=(0.9, 1.35), cuneiform=(1.2, 1.1),
        mt1_base=(1.4, 0.9), mt1_head=(1.65, 0.45), mt5_head=(1.45, 0.4),
        big_toe_mcp=(1.8, 0.35), big_toe_ip=(1.95, 0.25), big_toe_tip=(2.1, 0.15),
        toe2_tip=(2.05, 0.2), toe3_tip=(1.95, 0.25), toe4_tip=(1.85, 0.3), toe5_tip=(1.75, 0.35),
    ),
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
    et_indent(elem, space="  ")
    return tostring(elem, encoding="unicode")


def s(parent, tag, cls=None, **attrs):
    e = SubElement(parent, tag)
    if cls:
        e.set("class", cls)
    for k, v in attrs.items():
        e.set(k, str(v))
    return e


def create_svg(joints, foot_side, view, pose_name, style, scale=80):
    padding = 40
    svg_w = int(scale * 3.5 + padding * 2)
    svg_h = int(scale * 3 + padding * 2)
    ox = svg_w * 0.2
    is_manga = (style == "manga")

    svg = Element("svg", xmlns="http://www.w3.org/2000/svg",
                  viewBox=f"0 0 {svg_w} {svg_h}",
                  width=str(svg_w), height=str(svg_h))

    sty = SubElement(svg, "style")
    sty.text = ("""
        .bone { stroke:#888; stroke-width:1.5; fill:none; }
        .joint { fill:#e74c3c; stroke:#fff; stroke-width:.5; }
        .joint-sm { fill:#e67e22; stroke:#fff; stroke-width:.5; }
        .arch-highlight { stroke:#e67e22; stroke-width:2.5; fill:none; stroke-dasharray:6,4; }
        .silhouette { fill:#f0d0b8; stroke:#c09070; stroke-width:.8; }
        .nail { fill:#ffe8e0; stroke:#e8c0a0; stroke-width:0.3; }
        .label { font-family:sans-serif; font-size:9px; fill:#444; }
        .title { font-family:sans-serif; font-size:14px; font-weight:bold; fill:#333; }
        .callout { font-family:sans-serif; font-size:10px; fill:#2980b9; }
    """)

    def tx(point):
        x, y = point
        if foot_side == "left":
            x = -x
        return x * scale + ox, svg_h - padding - y * scale

    style_label = "Manga (14yo Loli)" if is_manga else "Realistic (Adult)"
    s(svg, "text", "title", x=str(padding), y=str(padding + 15)).text = \
        f"{foot_side.capitalize()} Foot [{style_label}] - {view.capitalize()} - Pose: {pose_name}"

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

    # Foot silhouette
    dors_pts = [hp, ct, ta, na, cu, m1, bm, bi, bt]
    dp = [f"M {dors_pts[0][0]},{dors_pts[0][1]}"]
    for i in range(1, len(dors_pts)):
        mx = (dors_pts[i - 1][0] + dors_pts[i][0]) / 2
        my = (dors_pts[i - 1][1] + dors_pts[i][1]) / 2
        dp.append(f"Q {mx},{my} {dors_pts[i][0]},{dors_pts[i][1]}")

    prev = bt
    for tip_name in ["toe2_tip", "toe3_tip", "toe4_tip", "toe5_tip"]:
        if tip_name in joints:
            pt = tx(joints[tip_name])
            mx = (prev[0] + pt[0]) / 2
            my = max(prev[1], pt[1]) + scale * (0.015 if is_manga else 0.02)
            dp.append(f"Q {mx},{my} {pt[0]},{pt[1]}")
            prev = pt

    # Sole curve
    sole_mid = ((t5[0] + hp[0]) / 2, t5[1] + scale * (0.03 if is_manga else 0.04))
    dp.append(f"Q {sole_mid[0]},{sole_mid[1]} {hp[0]},{hp[1]} Z")
    s(svg, "path", "silhouette", d=" ".join(dp))

    # Arch highlight (if not manga: arch is very subtle)
    arch_pts = [tx(joints[p]) for p in ARCH_PTS if p in joints]
    if arch_pts:
        if not is_manga:
            ad = f"M {arch_pts[0][0]},{arch_pts[0][1]}" + "".join(
                f" L {p[0]},{p[1]}" for p in arch_pts[1:])
            s(svg, "path", "arch-highlight", d=ad)

    # Manga: arch note
    if is_manga:
        mid_a = arch_pts[len(arch_pts) // 2]
        s(svg, "text", "callout", x=str(mid_a[0] - 20), y=str(mid_a[1] - 10)).text = \
            "Gentle arch (half adult height)"

    # Bones — only for realistic; manga omits internal bone lines
    if not is_manga:
        for chain in BONE_CHAINS.values():
            pts = [tx(joints[p]) for p in chain if p in joints]
            for i in range(len(pts) - 1):
                s(svg, "line", "bone",
                  x1=str(pts[i][0]), y1=str(pts[i][1]),
                  x2=str(pts[i + 1][0]), y2=str(pts[i + 1][1]))
        s(svg, "line", "bone", x1=str(hp[0]), y1=str(hp[1]),
          x2=str(ct[0]), y2=str(ct[1]))

    # Joints — manga: only big joints (ankle, MT heads, toes are smooth beans)
    for name, point in joints.items():
        x, y = tx(point)
        is_toe = name.startswith("toe") or name.startswith("big_toe")
        if is_manga and is_toe:
            continue  # manga: toes are smooth, no joints
        major = name.startswith("talus") or name.endswith("head") or name == "medial_malleolus"
        s(svg, "circle", "joint" if major else "joint-sm",
          r=str(3.0 if is_manga else 3.5 if major else 2.5), cx=str(x), cy=str(y))
        lbl = LABELS.get(name)
        if lbl and not (is_manga and is_toe):
            s(svg, "text", "label", x=str(x + 6), y=str(y + 3)).text = lbl

    # Manga: big toe nail
    if is_manga:
        nail_x, nail_y = bt[0], bt[1] + 2
        s(svg, "ellipse", "nail",
          cx=str(nail_x), cy=str(nail_y),
          rx=str(scale * 0.03), ry=str(scale * 0.04))

    # Callouts
    lx = 8 if foot_side == "left" else -8
    lx_big = 15 if foot_side == "left" else -15
    arch_label = "Gentle Arch" if is_manga else "Medial Arch"
    if arch_pts and not is_manga:
        mid_a = arch_pts[len(arch_pts) // 2]
        s(svg, "text", "callout", x=str(mid_a[0] + lx_big), y=str(mid_a[1] - 10)).text = arch_label
    if pose_name == "standing":
        s(svg, "text", "callout", x=str(hp[0]), y=str(hp[1] + 18)).text = "Heel"
        s(svg, "text", "callout", x=str(m1[0] + lx), y=str(m1[1] + 18)).text = "Ball"
    mm = tx(joints["medial_malleolus"])
    ankle_label = "Soft inner ankle" if is_manga else "Inner ankle (higher)"
    s(svg, "text", "callout", x=str(mm[0] + lx_big), y=str(mm[1] - 10)).text = ankle_label

    if is_manga:
        s(svg, "text", "callout", x=str(padding), y=str(svg_h - padding + 15)).text = \
            "Manga: softer arch, no toe joints, smaller proportions, rounded silhouette"

    return svg


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--style", default="manga", choices=["realistic", "manga"])
    ALL_JOINTS = {**FOOT_JOINTS_ADULT, **FOOT_JOINTS_MANGA}
    ap.add_argument("--pose", default="standing", choices=list(ALL_JOINTS.keys()))
    ap.add_argument("--foot", default="right", choices=["left", "right"])
    ap.add_argument("--view", default="medial")
    ap.add_argument("--output", default=None)
    args = ap.parse_args()

    if args.style == "manga" and args.pose in FOOT_JOINTS_MANGA:
        joints = FOOT_JOINTS_MANGA[args.pose]
    else:
        joints = FOOT_JOINTS_ADULT.get(args.pose, FOOT_JOINTS_ADULT["standing"])

    out = args.output or f"{args.pose}_{args.foot}_foot.svg"
    with open(out, "w", encoding="utf-8") as f:
        f.write(prettify(create_svg(joints, args.foot, args.view, args.pose, args.style)))
    print(f"Foot reference saved to: {out}")


if __name__ == "__main__":
    main()
