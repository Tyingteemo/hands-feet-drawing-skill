#!/usr/bin/env python3
"""
Generate an annotated hand reference SVG — realistic or manga (14yo loli) style.

Usage:
    python generate_hand_svg.py --style manga --pose relaxed_open --hand right --output hand.svg

Styles: realistic (adult proportions), manga (14yo soft proportions)
Poses: relaxed_open, fist, pointing, spread, peace (manga only), heart_finger (manga only)
"""

import argparse
import math
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.etree.ElementTree import indent as et_indent


# === REALISTIC (ADULT) JOINT DATA ===
HAND_JOINTS_ADULT = {
    "relaxed_open": dict(
        wrist=(0.0, 0.0), palm_center=(0.0, 0.6),
        thumb_cmc=(-0.7, 0.4), thumb_mcp=(-0.9, 0.8), thumb_ip=(-0.8, 1.2), thumb_tip=(-0.65, 1.5),
        index_mcp=(-0.35, 1.3), index_pip=(-0.3, 2.0), index_dip=(-0.25, 2.5), index_tip=(-0.22, 2.85),
        middle_mcp=(0.0, 1.35), middle_pip=(0.0, 2.1), middle_dip=(0.0, 2.65), middle_tip=(0.0, 3.0),
        ring_mcp=(0.35, 1.3), ring_pip=(0.3, 2.0), ring_dip=(0.25, 2.5), ring_tip=(0.22, 2.8),
        pinky_mcp=(0.6, 1.15), pinky_pip=(0.5, 1.7), pinky_dip=(0.42, 2.0), pinky_tip=(0.38, 2.25),
    ),
    "fist": dict(
        wrist=(0.0, 0.0), palm_center=(0.0, 0.6),
        thumb_cmc=(-0.7, 0.4), thumb_mcp=(-0.8, 0.7), thumb_ip=(-0.6, 0.9), thumb_tip=(-0.4, 1.0),
        index_mcp=(-0.35, 1.3), index_pip=(-0.25, 1.7), index_dip=(-0.15, 1.9), index_tip=(-0.1, 2.0),
        middle_mcp=(0.0, 1.35), middle_pip=(0.0, 1.8), middle_dip=(0.05, 2.0), middle_tip=(0.05, 2.1),
        ring_mcp=(0.35, 1.3), ring_pip=(0.3, 1.7), ring_dip=(0.25, 1.9), ring_tip=(0.2, 2.0),
        pinky_mcp=(0.6, 1.15), pinky_pip=(0.5, 1.5), pinky_dip=(0.42, 1.7), pinky_tip=(0.38, 1.8),
    ),
    "pointing": dict(
        wrist=(0.0, 0.0), palm_center=(0.0, 0.6),
        thumb_cmc=(-0.7, 0.4), thumb_mcp=(-0.85, 0.7), thumb_ip=(-0.7, 1.0), thumb_tip=(-0.55, 1.15),
        index_mcp=(-0.35, 1.3), index_pip=(-0.35, 2.0), index_dip=(-0.3, 2.5), index_tip=(-0.28, 2.85),
        middle_mcp=(0.0, 1.35), middle_pip=(0.05, 1.7), middle_dip=(0.1, 1.9), middle_tip=(0.1, 2.0),
        ring_mcp=(0.35, 1.3), ring_pip=(0.3, 1.65), ring_dip=(0.25, 1.85), ring_tip=(0.2, 1.95),
        pinky_mcp=(0.6, 1.15), pinky_pip=(0.5, 1.45), pinky_dip=(0.42, 1.65), pinky_tip=(0.38, 1.75),
    ),
    "spread": dict(
        wrist=(0.0, 0.0), palm_center=(0.0, 0.6),
        thumb_cmc=(-0.9, 0.2), thumb_mcp=(-1.2, 0.5), thumb_ip=(-1.15, 1.0), thumb_tip=(-1.0, 1.3),
        index_mcp=(-0.45, 1.25), index_pip=(-0.5, 2.0), index_dip=(-0.45, 2.5), index_tip=(-0.42, 2.8),
        middle_mcp=(0.0, 1.35), middle_pip=(0.0, 2.1), middle_dip=(0.0, 2.65), middle_tip=(0.0, 3.0),
        ring_mcp=(0.5, 1.25), ring_pip=(0.55, 2.0), ring_dip=(0.5, 2.5), ring_tip=(0.45, 2.8),
        pinky_mcp=(0.9, 1.05), pinky_pip=(0.95, 1.6), pinky_dip=(0.9, 2.0), pinky_tip=(0.85, 2.2),
    ),
}

# === MANGA (14YO LOLI) JOINT DATA ===
# ~15% narrower, softer arcs, more compact spread
HAND_JOINTS_MANGA = {
    "relaxed_open": dict(
        wrist=(0.0, 0.0), palm_center=(0.0, 0.6),
        thumb_cmc=(-0.65, 0.4), thumb_mcp=(-0.85, 0.75), thumb_ip=(-0.75, 1.15), thumb_tip=(-0.6, 1.4),
        index_mcp=(-0.35, 1.25), index_pip=(-0.3, 1.9), index_dip=(-0.25, 2.35), index_tip=(-0.22, 2.65),
        middle_mcp=(0.0, 1.3), middle_pip=(0.0, 2.0), middle_dip=(0.0, 2.5), middle_tip=(0.0, 2.8),
        ring_mcp=(0.33, 1.25), ring_pip=(0.28, 1.9), ring_dip=(0.23, 2.35), ring_tip=(0.2, 2.6),
        pinky_mcp=(0.55, 1.1), pinky_pip=(0.45, 1.6), pinky_dip=(0.38, 1.85), pinky_tip=(0.34, 2.05),
    ),
    "fist": dict(
        wrist=(0.0, 0.0), palm_center=(0.0, 0.6),
        thumb_cmc=(-0.65, 0.4), thumb_mcp=(-0.75, 0.65), thumb_ip=(-0.55, 0.85), thumb_tip=(-0.35, 0.95),
        index_mcp=(-0.35, 1.25), index_pip=(-0.23, 1.6), index_dip=(-0.13, 1.8), index_tip=(-0.08, 1.9),
        middle_mcp=(0.0, 1.3), middle_pip=(0.0, 1.7), middle_dip=(0.04, 1.9), middle_tip=(0.04, 2.0),
        ring_mcp=(0.33, 1.25), ring_pip=(0.28, 1.6), ring_dip=(0.23, 1.8), ring_tip=(0.18, 1.9),
        pinky_mcp=(0.55, 1.1), pinky_pip=(0.45, 1.4), pinky_dip=(0.38, 1.6), pinky_tip=(0.34, 1.7),
    ),
    "pointing": dict(
        wrist=(0.0, 0.0), palm_center=(0.0, 0.6),
        thumb_cmc=(-0.65, 0.4), thumb_mcp=(-0.8, 0.65), thumb_ip=(-0.65, 0.95), thumb_tip=(-0.5, 1.1),
        index_mcp=(-0.35, 1.25), index_pip=(-0.35, 1.9), index_dip=(-0.3, 2.35), index_tip=(-0.28, 2.65),
        middle_mcp=(0.0, 1.3), middle_pip=(0.04, 1.6), middle_dip=(0.08, 1.8), middle_tip=(0.08, 1.9),
        ring_mcp=(0.33, 1.25), ring_pip=(0.28, 1.55), ring_dip=(0.23, 1.75), ring_tip=(0.18, 1.85),
        pinky_mcp=(0.55, 1.1), pinky_pip=(0.45, 1.35), pinky_dip=(0.38, 1.55), pinky_tip=(0.34, 1.65),
    ),
    "spread": dict(
        wrist=(0.0, 0.0), palm_center=(0.0, 0.6),
        thumb_cmc=(-0.85, 0.2), thumb_mcp=(-1.1, 0.5), thumb_ip=(-1.05, 0.95), thumb_tip=(-0.9, 1.2),
        index_mcp=(-0.42, 1.2), index_pip=(-0.45, 1.9), index_dip=(-0.4, 2.35), index_tip=(-0.38, 2.6),
        middle_mcp=(0.0, 1.3), middle_pip=(0.0, 2.0), middle_dip=(0.0, 2.5), middle_tip=(0.0, 2.8),
        ring_mcp=(0.45, 1.2), ring_pip=(0.48, 1.9), ring_dip=(0.45, 2.35), ring_tip=(0.42, 2.6),
        pinky_mcp=(0.8, 1.0), pinky_pip=(0.82, 1.5), pinky_dip=(0.78, 1.85), pinky_tip=(0.74, 2.0),
    ),
    "peace": dict(
        wrist=(0.0, 0.0), palm_center=(0.0, 0.6),
        thumb_cmc=(-0.65, 0.4), thumb_mcp=(-0.8, 0.65), thumb_ip=(-0.65, 0.95), thumb_tip=(-0.5, 1.1),
        index_mcp=(-0.35, 1.25), index_pip=(-0.35, 2.0), index_dip=(-0.3, 2.55), index_tip=(-0.28, 2.9),
        middle_mcp=(0.0, 1.3), middle_pip=(0.0, 2.0), middle_dip=(0.04, 2.55), middle_tip=(0.04, 2.85),
        ring_mcp=(0.33, 1.25), ring_pip=(0.28, 1.55), ring_dip=(0.23, 1.75), ring_tip=(0.18, 1.85),
        pinky_mcp=(0.55, 1.1), pinky_pip=(0.45, 1.35), pinky_dip=(0.38, 1.55), pinky_tip=(0.34, 1.65),
    ),
    "heart_finger": dict(
        wrist=(0.0, 0.0), palm_center=(0.0, 0.6),
        thumb_cmc=(-0.75, 0.4), thumb_mcp=(-0.85, 0.7), thumb_ip=(-0.65, 0.95), thumb_tip=(-0.3, 1.1),
        index_mcp=(-0.35, 1.25), index_pip=(-0.35, 1.7), index_dip=(-0.25, 1.6), index_tip=(-0.3, 1.3),
        middle_mcp=(0.0, 1.3), middle_pip=(0.04, 1.6), middle_dip=(0.08, 1.8), middle_tip=(0.08, 1.9),
        ring_mcp=(0.33, 1.25), ring_pip=(0.28, 1.55), ring_dip=(0.23, 1.75), ring_tip=(0.18, 1.85),
        pinky_mcp=(0.55, 1.1), pinky_pip=(0.45, 1.35), pinky_dip=(0.38, 1.55), pinky_tip=(0.34, 1.65),
    ),
}

FINGER_CHAINS = {
    "thumb": ["thumb_cmc", "thumb_mcp", "thumb_ip", "thumb_tip"],
    "index": ["index_mcp", "index_pip", "index_dip", "index_tip"],
    "middle": ["middle_mcp", "middle_pip", "middle_dip", "middle_tip"],
    "ring": ["ring_mcp", "ring_pip", "ring_dip", "ring_tip"],
    "pinky": ["pinky_mcp", "pinky_pip", "pinky_dip", "pinky_tip"],
}

LABELS = {
    "wrist": "Wrist", "palm_center": "",
    "thumb_cmc": "CMC", "thumb_mcp": "MCP", "thumb_ip": "IP",
    "index_mcp": "Index MCP", "index_pip": "PIP", "index_dip": "DIP",
    "middle_mcp": "Middle MCP", "middle_pip": "PIP", "middle_dip": "DIP",
    "ring_mcp": "Ring MCP", "ring_pip": "PIP", "ring_dip": "DIP",
    "pinky_mcp": "Pinky MCP", "pinky_pip": "PIP", "pinky_dip": "DIP",
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


def create_svg(joints, hand_side, view, pose_name, style, scale=80):
    padding = 40
    svg_w = int(scale * 4.5 + padding * 2)
    svg_h = int(scale * 4 + padding * 2)
    cx = svg_w / 2
    is_manga = (style == "manga")

    svg = Element("svg", xmlns="http://www.w3.org/2000/svg",
                  viewBox=f"0 0 {svg_w} {svg_h}",
                  width=str(svg_w), height=str(svg_h))

    sty = SubElement(svg, "style")
    sty.text = ("""
        .bone { stroke:#888; stroke-width:1.5; fill:none; }
        .joint { fill:#e74c3c; stroke:#fff; stroke-width:.5; }
        .joint-sm { fill:#e67e22; stroke:#fff; stroke-width:.5; }
        .silhouette { fill:#f5d5c5; stroke:#c09070; stroke-width:.8; }
        .nail { fill:#ffe8e0; stroke:#e8c0a0; stroke-width:0.3; }
        .label { font-family:sans-serif; font-size:9px; fill:#444; }
        .title { font-family:sans-serif; font-size:14px; font-weight:bold; fill:#333; }
        .callout { font-family:sans-serif; font-size:10px; fill:#2980b9; }
        .callout-line { stroke:#2980b9; stroke-width:.6; stroke-dasharray:3,3; }
    """)

    def tx(point):
        x, y = point
        if hand_side == "left":
            x = -x
        return x * scale + cx, y * scale + padding

    style_label = "Manga (14yo Loli)" if is_manga else "Realistic (Adult)"
    s(svg, "text", "title", x=str(padding), y=str(padding + 15)).text = \
        f"{hand_side.capitalize()} Hand [{style_label}] - {view.capitalize()} - Pose: {pose_name}"

    wrist = tx(joints["wrist"])
    palm_c = tx(joints["palm_center"])
    th_cmc = tx(joints["thumb_cmc"])
    th_mcp = tx(joints["thumb_mcp"])
    ix_mcp = tx(joints["index_mcp"])
    md_mcp = tx(joints["middle_mcp"])
    rg_mcp = tx(joints["ring_mcp"])
    pk_mcp = tx(joints["pinky_mcp"])

    # Palm silhouette
    th_side = th_cmc[0]
    pk_side = pk_mcp[0]
    w_thumb = (wrist[0] + (th_side - wrist[0]) * 0.3, wrist[1])
    w_pinky = (wrist[0] + (pk_side - wrist[0]) * 0.3, wrist[1])
    nudge = scale * (0.04 if is_manga else 0.06)
    nudge_sm = scale * (0.03 if is_manga else 0.04)
    pd = (
        f"M {th_cmc[0]},{th_cmc[1]}"
        f" C {th_cmc[0]},{th_cmc[1]+nudge} {w_thumb[0]},{w_thumb[1]+nudge} {w_thumb[0]},{w_thumb[1]}"
        f" L {w_pinky[0]},{w_pinky[1]}"
        f" C {w_pinky[0]},{w_pinky[1]+nudge} {pk_mcp[0]},{pk_mcp[1]+nudge} {pk_mcp[0]},{pk_mcp[1]}"
        f" L {rg_mcp[0]},{rg_mcp[1]} L {md_mcp[0]},{md_mcp[1]} L {ix_mcp[0]},{ix_mcp[1]}"
        f" C {ix_mcp[0]},{ix_mcp[1]-nudge_sm} {th_mcp[0]},{th_mcp[1]-nudge_sm} {th_cmc[0]},{th_cmc[1]} Z"
    )
    s(svg, "path", "silhouette", d=pd)

    # Finger silhouettes
    for fname, chain in FINGER_CHAINS.items():
        pts = [tx(joints[p]) for p in chain if p in joints]
        if len(pts) < 2:
            continue
        mw = scale * (0.13 if is_manga else 0.17) if fname == "thumb" else scale * (0.10 if is_manga else 0.14)
        tw = scale * (0.07 if is_manga else 0.09) if fname == "thumb" else scale * (0.05 if is_manga else 0.07)

        lp, rp = [], []
        for i, (x, y) in enumerate(pts):
            if i < len(pts) - 1:
                dx, dy = pts[i + 1][0] - x, pts[i + 1][1] - y
            else:
                dx, dy = x - pts[i - 1][0], y - pts[i - 1][1]
            ln = math.hypot(dx, dy)
            if ln < 0.01:
                continue
            nx, ny = -dy / ln, dx / ln
            w = (mw + (tw - mw) * i / max(len(pts) - 1, 1)) * (0.65 if i == 0 else 1.0)
            lp.append((x + nx * w, y + ny * w))
            rp.append((x - nx * w, y - ny * w))
        if len(lp) < 2:
            continue

        fp = [f"M {lp[0][0]},{lp[0][1]}"]
        for i in range(1, len(lp)):
            mx = (lp[i - 1][0] + lp[i][0]) / 2
            my = (lp[i - 1][1] + lp[i][1]) / 2
            fp.append(f"Q {mx},{my} {lp[i][0]},{lp[i][1]}")

        # Rounded tip (manga: softer)
        tip_ctrl_y = lp[-1][1] + tw * (1.5 if is_manga else 1.0)
        fp.append(f"Q {lp[-1][0]},{tip_ctrl_y} {rp[-1][0]},{rp[-1][1]}")

        for i in range(len(rp) - 1, 0, -1):
            mx = (rp[i][0] + rp[i - 1][0]) / 2
            my = (rp[i][1] + rp[i - 1][1]) / 2
            fp.append(f"Q {mx},{my} {rp[i - 1][0]},{rp[i - 1][1]}")
        fp.append("Z")
        s(svg, "path", "silhouette", d=" ".join(fp))

        # Manga: add nail (small oval, set back from tip)
        if is_manga and len(pts) >= 2:
            tip_pt = pts[-1]
            nail_y = tip_pt[1] - tw * 0.2
            s(svg, "ellipse", "nail",
              cx=str(tip_pt[0]), cy=str(nail_y),
              rx=str(tw * 0.35), ry=str(tw * 0.55))

    # Bones (skeleton lines) — only for realistic style
    if not is_manga:
        for chain in FINGER_CHAINS.values():
            pts = [tx(joints[p]) for p in chain if p in joints]
            for i in range(len(pts) - 1):
                s(svg, "line", "bone", x1=str(pts[i][0]), y1=str(pts[i][1]),
                  x2=str(pts[i + 1][0]), y2=str(pts[i + 1][1]))
        s(svg, "line", "bone", x1=str(wrist[0]), y1=str(wrist[1]),
          x2=str(palm_c[0]), y2=str(palm_c[1]))
        for pn in ["thumb_mcp", "index_mcp", "middle_mcp", "ring_mcp", "pinky_mcp"]:
            pt = tx(joints[pn])
            s(svg, "line", "bone", x1=str(palm_c[0]), y1=str(palm_c[1]),
              x2=str(pt[0]), y2=str(pt[1]))

    # Joints — manga: only MCP (no PIP/DIP)
    for name, point in joints.items():
        x, y = tx(point)
        major = name.endswith("mcp") or name in ("wrist", "thumb_cmc")
        minor = name.endswith("pip") or name.endswith("dip") or name.endswith("ip")
        if is_manga and minor:
            continue  # manga: skip PIP/DIP joint dots
        s(svg, "circle", "joint" if major else "joint-sm",
          r=str(3.0 if is_manga else 3.5 if major else 2.5), cx=str(x), cy=str(y))
        lbl = LABELS.get(name, "")
        if lbl and not (is_manga and minor):
            s(svg, "text", "label", x=str(x + 6), y=str(y + 3)).text = lbl

    # Callouts
    mcps = [tx(joints[n]) for n in ["index_mcp", "middle_mcp", "ring_mcp", "pinky_mcp"]]
    cd = f"M {mcps[0][0]},{mcps[0][1]}" + "".join(f" L {p[0]},{p[1]}" for p in mcps[1:])
    s(svg, "path", "callout-line", d=cd)
    mid = mcps[len(mcps) // 2]
    arc_label = "Soft MCP Arc" if is_manga else "Knuckle Arc"
    s(svg, "text", "callout", x=str(mid[0] - 30), y=str(mid[1] - 8)).text = arc_label
    length_label = "Length: Middle > Ring > Index > Pinky"
    if is_manga:
        length_label += " (manga: slender, ~15% thinner)"
    s(svg, "text", "callout", x=str(tx(joints["wrist"])[0] - 30), y=str(padding)).text = length_label

    # Manga: style note
    if is_manga:
        s(svg, "text", "callout", x=str(padding), y=str(svg_h - padding + 15)).text = \
            "Manga style: softer contours, no PIP/DIP joints, small nails, thinner fingers"

    return svg


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--style", default="manga", choices=["realistic", "manga"])
    ALL_JOINTS = {**HAND_JOINTS_ADULT, **HAND_JOINTS_MANGA}
    ap.add_argument("--pose", default="relaxed_open", choices=list(ALL_JOINTS.keys()))
    ap.add_argument("--hand", default="right", choices=["left", "right"])
    ap.add_argument("--view", default="palm")
    ap.add_argument("--output", default=None)
    args = ap.parse_args()

    if args.style == "manga" and args.pose in HAND_JOINTS_MANGA:
        joints = HAND_JOINTS_MANGA[args.pose]
    else:
        joints = HAND_JOINTS_ADULT.get(args.pose, HAND_JOINTS_ADULT["relaxed_open"])

    out = args.output or f"{args.pose}_{args.hand}_hand.svg"
    with open(out, "w", encoding="utf-8") as f:
        f.write(prettify(create_svg(joints, args.hand, args.view, args.pose, args.style)))
    print(f"Hand reference saved to: {out}")


if __name__ == "__main__":
    main()
