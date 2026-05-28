# Code Drawing Patterns for Hands & Feet

## Table of Contents
1. The Construction-Skeleton Approach
2. SVG Pattern
3. p5.js Pattern
4. HTML Canvas Pattern
5. Coordinate Tables
6. Common Code-Drawing Gotchas
7. Animation Considerations

---

## 1. The Construction-Skeleton Approach

This approach works identically in SVG, p5.js, Canvas, and any procedural drawing system:

1. **Define joint positions as 2D coordinates** (or 3D for WebGL/Three.js)
2. **Draw the skeleton** — connect joints with line segments
3. **Flesh it out** — draw bezier curves around the skeleton for the silhouette
4. **Add details** — nails, creases, webbing, tendons

The key insight is: the joint coordinates are reusable. You define them once, then draw the skeleton as a debugging overlay, then draw the fleshed-out form around the same coordinates.

---

## 2. SVG Pattern

### Composable Finger Components

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="-2 -1 8 12">
  <defs>
    <!-- A single finger component, centered at MCP joint -->
    <g id="finger">
      <!-- Finger bone lines (construction) -->
      <line x1="0" y1="0" x2="0" y2="-2" stroke="#999" stroke-width="0.5" opacity="0.3"/>
      <!-- Fleshed-out finger silhouette -->
      <path d="
        M -0.3,0
        C -0.35,-0.5 -0.35,-1.0 -0.25,-1.5
        C -0.2,-2.0 -0.15,-2.3 -0.1,-2.6
        C -0.05,-2.8 -0.02,-2.9 0,-2.95
        C 0.02,-2.9 0.05,-2.8 0.1,-2.6
        C 0.15,-2.3 0.2,-2.0 0.25,-1.5
        C 0.35,-1.0 0.35,-0.5 0.3,0
        Z
      " fill="#f0d0b0" stroke="#c09070" stroke-width="0.3"/>
      <!-- Joint dots (construction) -->
      <circle cx="0" cy="0" r="0.08" fill="#e00" opacity="0.5"/>
      <circle cx="0" cy="-0.8" r="0.06" fill="#e00" opacity="0.5"/>
      <circle cx="0" cy="-1.5" r="0.05" fill="#e00" opacity="0.5"/>
    </g>

    <!-- Nail component -->
    <g id="nail">
      <path d="M -0.08,-0.15 C -0.05,-0.2 0.05,-0.2 0.08,-0.15 C 0.1,-0.1 0.08,0 0,0.05 C -0.08,0 -0.1,-0.1 -0.08,-0.15 Z" fill="#e8c0a0" opacity="0.6"/>
    </g>
  </defs>

  <!-- Palm -->
  <path d="
    M -0.5,0.5
    L -0.6,2.0
    C -0.6,2.5 -0.4,3.0 -0.2,3.2
    L 0.2,3.2
    C 0.4,3.0 0.6,2.5 0.6,2.0
    L 0.5,0.5
    Z
  " fill="#f0d0b0" stroke="#c09070" stroke-width="0.3"/>

  <!-- Fingers placed along the MCP arc -->
  <use href="#finger" transform="translate(-0.35, 0.5) rotate(-15)"/>
  <use href="#finger" transform="translate(-0.12, 0.55) rotate(-5)"/>
  <use href="#finger" transform="translate(0.12, 0.55) rotate(5)"/>
  <use href="#finger" transform="translate(0.35, 0.5) rotate(15)"/>

  <!-- Thumb (different plane!) -->
  <g transform="translate(-0.6, 1.2) rotate(-45)">
    <use href="#finger"/>
  </g>
</svg>
```

### Key SVG Techniques

- Use `<defs>` + `<use>` to reuse finger components — each finger is the same base shape, just rotated and scaled differently
- Use `<g transform="...">` to position fingers — the MCP joint is the transform origin
- Overlay construction lines (bones, joints) with reduced opacity — they provide reference without cluttering the final output
- Apply webbing: draw a single background path for the palm that includes gentle curves between finger bases

---

## 3. p5.js Pattern

### Skeleton Array Iteration

```javascript
// Define joint positions for a right hand (palm forward)
const joints = {
  wrist:     { x: 0,   y: 0 },
  // MCP joints (knuckles)
  thumb_mcp:  { x: -1.2, y: 0.8 },
  index_mcp:  { x: -0.5, y: 1.2 },
  middle_mcp: { x: 0,   y: 1.3 },
  ring_mcp:   { x: 0.5, y: 1.2 },
  pinky_mcp:  { x: 0.9, y: 1.0 },
  // PIP joints
  index_pip:  { x: -0.4, y: 2.0 },
  middle_pip: { x: 0,   y: 2.2 },
  ring_pip:   { x: 0.4, y: 2.0 },
  pinky_pip:  { x: 0.7, y: 1.6 },
  // DIP joints
  index_dip:  { x: -0.35, y: 2.6 },
  middle_dip: { x: 0,    y: 2.85 },
  ring_dip:   { x: 0.35, y: 2.6 },
  pinky_dip:  { x: 0.6,  y: 2.15 },
  // Tips
  index_tip:  { x: -0.3, y: 3.0 },
  middle_tip: { x: 0,   y: 3.3 },
  ring_tip:   { x: 0.3, y: 3.0 },
  pinky_tip:  { x: 0.5, y: 2.5 },
};

// Thumb joints (different plane)
const thumb = {
  cmc:  { x: -1.2, y: 0.3 },
  mcp:  { x: -1.5, y: 0.8 },
  ip:   { x: -1.4, y: 1.4 },
  tip:  { x: -1.2, y: 1.8 },
};

function drawFinger(mcp, pip, dip, tip, fingerWidth) {
  // Construction skeleton
  stroke(200, 100, 100, 80);
  strokeWeight(1);
  line(mcp.x, mcp.y, pip.x, pip.y);
  line(pip.x, pip.y, dip.x, dip.y);
  line(dip.x, dip.y, tip.x, tip.y);

  // Joint dots
  noStroke();
  fill(200, 100, 100, 100);
  circle(mcp.x, mcp.y, 3);
  circle(pip.x, pip.y, 2.5);
  circle(dip.x, dip.y, 2);

  // Fleshed-out finger using curveVertex
  // The finger tapers from base to tip
  fill(240, 210, 180);
  stroke(190, 140, 110);
  strokeWeight(0.5);
  beginShape();
    // Left side of finger (from MCP to tip)
    curveVertex(mcp.x - fingerWidth*0.5, mcp.y);
    curveVertex(pip.x - fingerWidth*0.4, pip.y);
    curveVertex(dip.x - fingerWidth*0.3, dip.y);
    curveVertex(tip.x - fingerWidth*0.15, tip.y);
    // Rounded tip
    curveVertex(tip.x, tip.y + fingerWidth*0.1);
    // Right side (from tip to MCP)
    curveVertex(tip.x + fingerWidth*0.15, tip.y);
    curveVertex(dip.x + fingerWidth*0.3, dip.y);
    curveVertex(pip.x + fingerWidth*0.4, pip.y);
    curveVertex(mcp.x + fingerWidth*0.5, mcp.y);
  endShape(CLOSE);

  // Nail
  fill(230, 190, 160);
  noStroke();
  const nailSize = fingerWidth * 0.2;
  ellipse(tip.x, tip.y - nailSize*0.5, nailSize, nailSize * 0.6);
}

function setup() {
  createCanvas(400, 600);

  // Scale and center
  const scale = 60;
  translate(width/2, height/2);

  // Draw palm
  fill(240, 210, 180);
  stroke(190, 140, 110);
  beginShape();
    // Left edge (thumb side)
    vertex(joints.thumb_mcp.x * scale, joints.thumb_mcp.y * scale);
    // Wrist
    vertex(joints.wrist.x - 0.5 * scale, joints.wrist.y * scale);
    vertex(joints.wrist.x + 0.5 * scale, joints.wrist.y * scale);
    // Right edge (pinky side)
    vertex(joints.pinky_mcp.x * scale, joints.pinky_mcp.y * scale);
    // Top edge (MCP arc)
    vertex(joints.ring_mcp.x * scale, joints.ring_mcp.y * scale);
    vertex(joints.middle_mcp.x * scale, joints.middle_mcp.y * scale);
    vertex(joints.index_mcp.x * scale, joints.index_mcp.y * scale);
  endShape(CLOSE);

  // Draw fingers
  const fingerWidth = 0.3 * scale;
  drawFinger(joints.index_mcp, joints.index_pip, joints.index_dip, joints.index_tip, fingerWidth);
  drawFinger(joints.middle_mcp, joints.middle_pip, joints.middle_dip, joints.middle_tip, fingerWidth * 1.1);
  drawFinger(joints.ring_mcp, joints.ring_pip, joints.ring_dip, joints.ring_tip, fingerWidth * 0.95);
  drawFinger(joints.pinky_mcp, joints.pinky_pip, joints.pinky_dip, joints.pinky_tip, fingerWidth * 0.8);

  // Draw thumb (different plane — draw it over the palm)
  const thumbWidth = fingerWidth * 1.2;
  drawFinger(thumb.cmc, thumb.mcp, thumb.ip, thumb.tip, thumbWidth);
}
```

### Key p5.js Techniques

- Define joint coordinates as data, not hardcoded shapes — this lets you tweak proportions globally
- Use `curveVertex()` for organic contours (smooth bezier curves)
- The taper formula: `widthAtJoint = baseWidth * (1 - 0.2 * jointIndex)` where jointIndex is 0 for MCP, 1 for PIP, etc.
- Draw the thumb LAST so it overlaps the palm correctly (thumb sits in front of the palm in most views)

---

## 4. HTML Canvas Pattern

```javascript
const canvas = document.getElementById('hand-canvas');
const ctx = canvas.getContext('2d');

function drawFinger(ctx, mcp, pip, dip, tip, width) {
  // Draw silhouette using bezier curves
  ctx.beginPath();

  // Start at left side of MCP
  ctx.moveTo(mcp.x - width * 0.5, mcp.y);

  // Left side curve
  ctx.bezierCurveTo(
    mcp.x - width * 0.45, (mcp.y + pip.y) / 2,
    pip.x - width * 0.4, pip.y,
    pip.x - width * 0.4, pip.y
  );
  ctx.bezierCurveTo(
    pip.x - width * 0.35, (pip.y + dip.y) / 2,
    dip.x - width * 0.3, dip.y,
    dip.x - width * 0.25, dip.y
  );
  ctx.bezierCurveTo(
    dip.x - width * 0.2, (dip.y + tip.y) / 2,
    tip.x - width * 0.15, tip.y,
    tip.x, tip.y + width * 0.1 // rounded tip
  );

  // Right side curve
  ctx.bezierCurveTo(
    tip.x + width * 0.15, tip.y,
    dip.x + width * 0.25, dip.y,
    dip.x + width * 0.3, dip.y
  );
  ctx.bezierCurveTo(
    dip.x + width * 0.35, (dip.y + pip.y) / 2,
    pip.x + width * 0.4, pip.y,
    pip.x + width * 0.4, pip.y
  );
  ctx.bezierCurveTo(
    pip.x + width * 0.45, (pip.y + mcp.y) / 2,
    mcp.x + width * 0.5, mcp.y,
    mcp.x + width * 0.5, mcp.y
  );

  ctx.closePath();
  ctx.fillStyle = '#f0d0b0';
  ctx.strokeStyle = '#c09070';
  ctx.lineWidth = 0.5;
  ctx.fill();
  ctx.stroke();
}
```

---

## 5. Coordinate Tables

### Right Hand (Relaxed, Palm Forward, Unit Scale)

| Point | x | y | Notes |
|-------|---|---|-------|
| Wrist | 0.0 | 0.0 | Reference origin |
| Palm center | 0.0 | 0.6 | Palm mass center |
| **Thumb** | | | |
| CMC | -0.7 | 0.4 | Saddle joint |
| MCP | -0.9 | 0.8 | Thumb knuckle |
| IP | -0.8 | 1.2 | Single thumb knuckle |
| Tip | -0.65 | 1.5 | Thumb pad |
| **Index** | | | |
| MCP | -0.35 | 1.3 | Knuckle |
| PIP | -0.3 | 2.0 | Middle joint |
| DIP | -0.25 | 2.5 | Fingertip joint |
| Tip | -0.22 | 2.85 | Fingertip |
| **Middle** | | | |
| MCP | 0.0 | 1.35 | Highest knuckle |
| PIP | 0.0 | 2.1 | Middle joint |
| DIP | 0.0 | 2.65 | Fingertip joint |
| Tip | 0.0 | 3.0 | Fingertip |
| **Ring** | | | |
| MCP | 0.35 | 1.3 | Knuckle |
| PIP | 0.3 | 2.0 | Middle joint |
| DIP | 0.25 | 2.5 | Fingertip joint |
| Tip | 0.22 | 2.8 | Fingertip |
| **Pinky** | | | |
| MCP | 0.6 | 1.15 | Knuckle |
| PIP | 0.5 | 1.7 | Middle joint |
| DIP | 0.42 | 2.0 | Fingertip joint |
| Tip | 0.38 | 2.25 | Fingertip |

### Right Foot (Standing, Medial View, Unit Scale)

| Point | x | y | Notes |
|-------|---|---|-------|
| Heel (posterior) | 0.0 | 0.0 | Ground contact |
| Calcaneus (top) | 0.3 | 0.7 | |
| Talus (ankle) | 0.7 | 1.1 | Ankle joint center |
| Medial malleolus | 0.65 | 1.3 | Inner ankle bump |
| Navicular | 1.0 | 0.8 | Highest point of arch |
| Cuneiform | 1.3 | 0.6 | Anterior midfoot |
| 1st MT head | 1.8 | 0.1 | Ball of big toe (ground contact) |
| Big toe MCP | 2.0 | 0.15 | |
| Big toe IP | 2.2 | 0.25 | |
| Big toe tip | 2.4 | 0.3 | |
| 2nd MT head | 1.9 | 0.1 | |
| 5th MT head | 1.6 | 0.1 | Ball of little toe (ground contact) |

---

## 6. Common Code-Drawing Gotchas

1. **Straight lines for finger contours** — fingers have subtle arcs along both sides. Use bezier curves, not straight lines.

2. **MCP joints on a straight line** — the knuckle arc is a real anatomical feature. The middle finger knuckle should be the highest point.

3. **All fingers the same length** — apply the cascade: middle > ring > index > pinky > thumb.

4. **No taper** — fingers are NOT cylinders of uniform width. They taper from base to tip by roughly 20-30%.

5. **Sharp V-webs** — the interdigital webbing should be a gentle curve, not a sharp V.

6. **Thumb on the same plane** — the thumb metacarpal is rotated ~90° relative to the other metacarpals. From palm-forward view, the thumbnail should face roughly toward the viewer, not to the side.

7. **Ignoring the palm cup** — the palm is not flat. Add a subtle concavity to the palm surface.

8. **No joint indication** — even in a simplified drawing, the PIP and DIP joints should be subtly indicated (creases, slight angle changes, or width changes).

---

## 7. Animation Considerations

### Finger Flexion

- Finger flexion follows a **logarithmic spiral**, not a circular arc. The fingertip traces a spiral path as the finger curls.
- **Maximum flexion ranges:**
  - MCP: ~90° (fingers), ~45° (thumb)
  - PIP: ~100°
  - DIP: ~80°
  - Thumb IP: ~80°

### The Enslavement Effect (Finger Interdependence)

When one finger flexes, adjacent fingers flex slightly. This is a neurological coupling:
- Middle finger PIP flexion causes ~15° of coupled flexion in the ring finger PIP
- Ring finger PIP flexion causes ~10° in the pinky PIP
- The index finger is the most independent

**Animation implication:** Isolated finger movements look unnatural. When animating, add subtle coupled movement to adjacent fingers.

### Thumb Animation

- The thumb moves in a fundamentally different plane from the other fingers
- Opposition is a compound motion: the thumb CMC abducts, the metacarpal rotates, and the MCP/IP flex
- When the thumb moves from adduction to opposition, the thumb pad rotates ~90° relative to the palm plane

### Foot Animation

- During walking, the foot goes through a smooth rocker motion: heel contact → foot flat → mid-stance → heel-off → toe-off
- The arch height changes through the gait cycle (flattens at mid-stance, rises at heel-off)
- The ankle angle at toe-off is approximately 20° of dorsiflexion relative to the leg
- Toes spread slightly on weight-bearing and relax in the air
