# Code Drawing Patterns — Manga Loli Style (~14yo)

## Table of Contents
1. Manga-Style Construction Approach
2. SVG Pattern (14yo Proportions)
3. p5.js Pattern
4. Coordinate Tables (14yo Manga)
5. Common Manga Code-Drawing Gotchas

---

## 1. Manga-Style Construction Approach

Unlike realistic drawing, manga code drawing should:
- Use **fewer, softer lines** — no individual bone traces
- Render **silhouette-focused** shapes rather than construction-skeleton
- Use **rounded beziers** for all finger/toe contours
- Show **minimal joint detail** — MCP only, no PIP/DIP
- Produce a **clean, simple** reference that looks like a manga sketch

---

## 2. SVG Pattern (14yo Proportions)

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="-2 -1 7 11">
  <defs>
    <!-- Manga finger: tapered, rounded tip, soft -->
    <g id="manga-finger">
      <!-- Soft silhouette — no bone lines visible -->
      <path d="
        M -0.2,0
        C -0.22,-0.4 -0.24,-0.8 -0.2,-1.3
        C -0.16,-1.8 -0.1,-2.2 -0.05,-2.5
        C 0.05,-2.2 0.1,-1.8 0.16,-1.3
        C 0.2,-0.8 0.22,-0.4 0.2,0
        Z
      " fill="#fce4d6" stroke="#e8c0a0" stroke-width="0.2"/>
      <!-- Small oval nail, set back from tip -->
      <ellipse cx="0" cy="-2.3" rx="0.04" ry="0.06" fill="#ffe8e0" stroke="#e8c0a0" stroke-width="0.1"/>
    </g>
  </defs>

  <!-- Palm: rounded pentagon -->
  <path d="
    M -0.8,2.0
    C -0.9,1.2 -0.8,0.5 -0.5,0.2
    L 0.5,0.2
    C 0.8,0.5 0.9,1.2 0.8,2.0
    Z
  " fill="#fce4d6" stroke="#e8c0a0" stroke-width="0.3"/>

  <!-- Manga fingers placed along soft MCP arc -->
  <use href="#manga-finger" transform="translate(-0.35, 2.0) rotate(-10) scale(1.0)"/>
  <use href="#manga-finger" transform="translate(-0.1, 2.1) rotate(-3) scale(1.05)"/>
  <use href="#manga-finger" transform="translate(0.15, 2.1) rotate(3) scale(1.0)"/>
  <use href="#manga-finger" transform="translate(0.4, 2.0) rotate(8) scale(0.8)"/>

  <!-- Thumb (soft, opposite plane) -->
  <g transform="translate(-0.65, 1.4) rotate(-40) scale(0.95)">
    <use href="#manga-finger"/>
  </g>
</svg>
```

---

## 3. p5.js Pattern

```javascript
// 14yo manga hand: soft, rounded, minimal detail
function drawMangaFinger(mcp, pip, dip, tip, baseW, tipW) {
  // Silhouette only — no bone lines
  fill('#fce4d6');
  stroke('#e8c0a0');
  strokeWeight(0.5);
  beginShape();
  // Left side (graceful curve)
  vertex(mcp.x - baseW/2, mcp.y);
  bezierVertex(
    mcp.x - baseW*0.45, (mcp.y + pip.y)/2,
    pip.x - baseW*0.4, pip.y,
    pip.x - baseW*0.38, pip.y
  );
  bezierVertex(
    pip.x - baseW*0.35, (pip.y + dip.y)/2,
    dip.x - baseW*0.3, dip.y,
    tip.x - tipW/2, tip.y
  );
  // Rounded tip
  bezierVertex(
    tip.x - tipW/2, tip.y + tipW*0.3,
    tip.x + tipW/2, tip.y + tipW*0.3,
    tip.x + tipW/2, tip.y
  );
  // Right side
  bezierVertex(
    dip.x + baseW*0.3, dip.y,
    pip.x + baseW*0.35, (pip.y + dip.y)/2,
    pip.x + baseW*0.38, pip.y
  );
  bezierVertex(
    pip.x + baseW*0.4, (mcp.y + pip.y)/2,
    mcp.x + baseW*0.45, mcp.y,
    mcp.x + baseW/2, mcp.y
  );
  endShape(CLOSE);

  // Small nail (manga)
  fill('#ffe8e0');
  noStroke();
  ellipse(tip.x, tip.y - tipW*0.15, tipW*0.4, tipW*0.6);

  // Subtle MCP bump only (no PIP/DIP)
  fill('#f5d5c0');
  noStroke();
  ellipse(mcp.x, mcp.y + baseW*0.1, baseW*0.3, baseW*0.15);
}
```

---

## 4. Coordinate Tables (14yo Manga, Right Hand)

### Relaxed Open, Palm Forward (Unit Scale × 80 = pixels)

| Point | x | y | Manga Notes |
|-------|---|---|-------------|
| Wrist | 0.0 | 0.0 | Smooth oval transition |
| Palm center | 0.0 | 0.6 | Rounded pentagon center |
| **Thumb** | | | Softer CMC position |
| CMC | -0.65 | 0.4 | Less abducted than adult |
| MCP | -0.85 | 0.75 | Softer bump |
| IP | -0.75 | 1.15 | |
| Tip | -0.6 | 1.4 | Rounded end |
| **Index** | | | ~15% thinner |
| MCP | -0.35 | 1.25 | Soft bump (flatter arc) |
| PIP | -0.3 | 1.9 | Almost straight from MCP |
| DIP | -0.25 | 2.35 | Barely distinct from PIP |
| Tip | -0.22 | 2.65 | Rounded tip |
| **Middle** | | | |
| MCP | 0.0 | 1.3 | Highest point (subtle) |
| PIP | 0.0 | 2.0 | |
| DIP | 0.0 | 2.5 | |
| Tip | 0.0 | 2.8 | |
| **Ring** | | | Slightly narrower spread |
| MCP | 0.33 | 1.25 | |
| PIP | 0.28 | 1.9 | |
| DIP | 0.23 | 2.35 | |
| Tip | 0.2 | 2.6 | |
| **Pinky** | | | |
| MCP | 0.55 | 1.1 | |
| PIP | 0.45 | 1.6 | |
| DIP | 0.38 | 1.85 | |
| Tip | 0.34 | 2.05 | |

**Left Hand Mirroring:** Multiply all x by -1.

### Right Foot (Standing, Medial, 14yo Manga)

| Point | x | y | Manga Notes |
|-------|---|---|------------|
| Heel (posterior) | 0.0 | 0.0 | Small, round |
| Calcaneus (top) | 0.25 | 0.6 | Subtle |
| Talus (ankle) | 0.6 | 1.0 | Ankle center |
| Medial malleolus | 0.55 | 1.15 | Barely a bump |
| Navicular | 0.9 | 0.7 | Arch high point (lower than adult) |
| Cuneiform | 1.2 | 0.55 | |
| MT1 Base | 1.4 | 0.4 | |
| MT1 Head | 1.65 | 0.1 | Ball of big toe |
| MT5 Head | 1.45 | 0.1 | Ball of little toe |
| Big toe MCP | 1.8 | 0.15 | |
| Big toe IP | 1.95 | 0.2 | |
| Big toe tip | 2.1 | 0.25 | Rounded |
| Toe2 tip | 2.05 | 0.2 | |
| Toe3 tip | 1.95 | 0.15 | |
| Toe4 tip | 1.85 | 0.1 | |
| Toe5 tip | 1.75 | 0.05 | |

**Left Foot Mirroring:** Multiply all x by -1. Arch stays on medial (inner) side.

---

## 5. Common Manga Code-Drawing Gotchas

1. **Drawing adult-width fingers** — 14yo manga fingers are ~15% thinner at base. Use `scale * 0.12` not `0.14`.

2. **Too many joints** — Manga needs MCP only (one subtle bump). Never draw PIP/DIP in code for manga style.

3. **Sharp finger tips** — Tips must be rounded/bezier curves. Never pointy.

4. **Adult nail placement** — Manga nails are smaller, set BACK from the tip. Not at the edge.

5. **Drawing bone lines** — Manga silhouettes should be clean. No internal bone structure visible.

6. **Too much palm detail** — No palmar creases, no thenar/hypothenar definition. Just a rounded pentagon.

7. **Thick outlines** — Manga line art is thin and delicate for hands. Use `stroke-width: 0.2–0.5`.

8. **Foot joints visible** — Toes should be smooth beans. No individual joint circles.

9. **Adult foot arch** — Manga arch is about half the adult height.

10. **Forgotten nails** — Even though they're tiny, manga nails are essential. They're a key feature that says "this is a detailed drawing, not a sketch."
