---
name: hands-feet-drawing
description: >
  Anatomical reference and drawing guidance for rendering human hands and feet correctly.
  Use this skill whenever the user is generating images, writing image generation prompts,
  drawing or painting (digital or traditional), designing characters, creating sprites or
  illustrations, or writing code that produces visual output involving human figures —
  including but not limited to hands, fingers, feet, or toes. This skill activates
  automatically and silently enhances any image generation or drawing task with proper
  hand and foot anatomy, even when the user does not explicitly mention hands or feet.
  It covers: prompt engineering for AI image generators (Stable Diffusion, Midjourney,
  DALL-E, Flux, ComfyUI), code-based drawing (SVG, p5.js, HTML Canvas, Processing),
  character design, figure drawing, and anatomical study. Also trigger when the user
  complains about hands or feet looking wrong in generated images or drawings.
---

# Hands & Feet Drawing Skill

This skill provides anatomical knowledge, step-by-step construction methods, prompt-engineering recipes, and code-generated reference images for drawing hands and feet correctly.

## How This Skill Works

- **Automatic enhancement:** Whenever you detect a task involving image generation, drawing, painting, character design, or any visual output with human figures, silently apply the hand/foot anatomy knowledge from this skill — the user should NOT need to ask for it.
- **Progressive disclosure:** This file contains quick-reference anatomy cards. Read the first paragraph of each reference file to decide if you need the full contents.
- **Two contexts:** For **AI image generation** tasks, use the prompt-engineering guidance. For **code-based drawing**, use the construction patterns and coordinate tables.

---

## Quick Anatomy Card — Hand

- **Bone count:** 27 bones (8 carpals, 5 metacarpals, 14 phalanges)
- **Finger joints:** Thumb = 2 phalanges. Index/Middle/Ring/Pinky = 3 each (proximal, middle, distal). The thumb has a CMC joint at the wrist base, MCP at the knuckle, and IP at the fingertip.
- **Knuckle arc:** The MCP joints (main knuckles) form a **downward arc** across the back of the hand — NOT a straight line. The middle finger knuckle is highest, pinky is lowest.
- **Palm concavity:** The palm is NOT flat — it forms a natural cup when relaxed. The thenar eminence (thumb pad) and hypothenar eminence (pinky pad) are thick mounds.
- **Finger length cascade:** Middle > Ring > Index > Pinky > Thumb. The thumb tip reaches about to the middle of the index finger's proximal phalanx when adducted.
- **Thumb opposition:** The thumb's metacarpal rotates ~90° relative to the other metacarpals, enabling opposition. The thumbnail faces roughly 90° from the fingernails when palm-forward.
- **Webbing:** Interdigital webbing reaches different heights — deepest between index/middle, shallowest between ring/pinky.
- **Wrist connection:** The hand emerges between the radius and ulna styloid processes. The wrist is narrower than the palm.

## Quick Anatomy Card — Foot

- **Bone count:** 26 bones (7 tarsals, 5 metatarsals, 14 phalanges)
- **Three arches:**
  - **Medial longitudinal arch** — main visible arch on the inner side (calcaneus → talus → navicular → cuneiforms → 1st-3rd metatarsals)
  - **Lateral longitudinal arch** — lower, outer side (calcaneus → cuboid → 4th-5th metatarsals)
  - **Transverse arch** — across the metatarsal heads, highest at 2nd metatarsal
- **Toe cascade:** Big toe (1) > 2 > 3 > 4 > 5. Variant: Morton's foot where 2nd toe is longest. Big toe has 2 phalanges; toes 2-5 have 3 each.
- **Ankle fork:** Medial malleolus (tibia) sits higher and more anterior. Lateral malleolus (fibula) sits lower and more posterior. **Never at the same height.**
- **Weight tripod:** Heel (calcaneus) + ball of big toe (1st metatarsal head) + ball of little toe (5th metatarsal head).
- **Achilles tendon:** Stands visibly clear of the ankle joint, inserting at the posterior calcaneus.
- **Foot width** narrows from the ball to the heel.

---

## The Universal Construction Method (5 Steps)

Use this approach for ANY hand or foot drawing, whether in code or on canvas:

1. **Block in the simple form.**
   - Hand = a pentagon (palm) with a fan of cylinders (fingers). The palm base aligns with the wrist.
   - Foot = a wedge (heel to ball) with a triangular toe box.

2. **Mark the joints.**
   - Hand: For each finger, place dots at MCP, PIP, DIP (or MCP, IP for thumb).
   - Foot: Mark the ankle (talus), metatarsal heads, and IP joints.

3. **Connect with cylinders.** Fingers/toes taper — wider at the base joint, narrower at the tip. Joints are not points but rounded transitions.

4. **Add refinements.** Knuckle bumps, nail beds, skin creases, webbing curves, tendon lines on the dorsum of the hand/foot.

5. **Check the silhouette.** If the outline looks wrong, go back to step 2. "Draw through" — sketch hidden bones to verify alignment.

---

## Context-Specific Workflows

### A. AI Image Generation (Midjourney / Stable Diffusion / DALL-E / Flux)

When the user is writing prompts for AI image generators:

1. **Always** include explicit finger/toe count and natural hand/foot anatomy descriptions in positive prompts — even when the user doesn't mention hands.
2. **Always** include negative prompt terms targeting hand/foot deformities.
3. Read `references/ai-prompt-engineering.md` for model-specific templates and advanced strategies (ControlNet, LoRA, inpainting).
4. Read `references/common-poses.md` for pose-specific description language.

### B. Code-Based Drawing (SVG / p5.js / Canvas / Processing)

When the user is writing code that draws human figures:

1. Start with the construction-skeleton approach from `references/code-drawing-patterns.md`.
2. Use the canonical coordinate tables as a starting point — scale, rotate, and adapt them.
3. Run the scripts at `scripts/generate_hand_svg.py` or `scripts/generate_foot_svg.py` to produce annotated reference SVGs.
4. Read `references/common-proportions.md` for age/gender-based adjustments.

### C. Diagnosis — Fixing Wrong-Looking Hands or Feet

When the user shows or describes a generated image/drawing with bad hands or feet:

1. Run through the **Diagnostic Checklist** (below).
2. Read `references/common-ai-mistakes.md` for the common failure catalog.
3. Explain what's wrong, why it happens, and how to fix it.

---

## Quick Diagnostic Checklist

| # | Check |
|---|-------|
| 1 | Count fingers. Exactly 5 per hand? |
| 2 | Count knuckles per finger. Thumb = 2; others = 3. |
| 3 | Do MCP joints form an arc, not a straight line? |
| 4 | Finger length cascade: Middle > Ring > Index > Pinky? |
| 5 | Thumb opposing correctly, not on the same plane as fingers? |
| 6 | Webbing sloping naturally, not a sharp V-cut? |
| 7 | Wrist present? Hand doesn't float or abruptly end. |
| 8 | Toes: Exactly 5, tapering in size? |
| 9 | Foot arch visible on medial (inner) side? |
| 10 | Ankle malleoli at different heights? |

---

## Reference File Guide

| File | Contents | Read when... |
|------|----------|-------------|
| `references/hand-anatomy.md` | Full hand bone/joint/soft tissue anatomy | Drawing a hand from scratch; need anatomical accuracy |
| `references/foot-anatomy.md` | Full foot bone/arch/ankle anatomy | Drawing a foot from scratch; need anatomical accuracy |
| `references/common-proportions.md` | Ratios by age, gender, body type | User specifies a character with age/gender details |
| `references/common-poses.md` | Pose catalog with joint positions | User describes a specific hand/foot pose |
| `references/ai-prompt-engineering.md` | Prompt templates per model, LoRA/ControlNet | Writing prompts for AI image generation |
| `references/code-drawing-patterns.md` | SVG/p5.js/Canvas patterns, coordinate tables | Writing code that draws hands or feet |
| `references/common-ai-mistakes.md` | Failure catalog with causes and fixes | Diagnosing wrong-looking hands/feet |

---

## Using the Scripts

```bash
# Generate an annotated hand reference SVG
python scripts/generate_hand_svg.py --pose relaxed_open --hand right --view palm --output hand_ref.svg

# Generate an annotated foot reference SVG
python scripts/generate_foot_svg.py --pose standing --foot right --view medial --output foot_ref.svg
```

Available poses: `relaxed_open`, `fist`, `pointing`, `grasping`, `spread` (hand); `standing`, `walking`, `dangling`, `tiptoe` (foot).

Run these scripts whenever you need a visual reference to show the user or to extract coordinate data from.
