---
name: hands-feet-drawing
description: >
  Manga-style anatomical reference and drawing guidance for rendering hands and feet
  correctly, specialized for young female characters (loli / ~14 years old). Use this
  skill whenever the user is generating or editing images that include hands, fingers,
  feet, or toes — whether through AI image generation (NovelAI, NijiJourney, Stable
  Diffusion, DALL-E, Flux, ComfyUI), code-based drawing (SVG, p5.js, HTML Canvas),
  digital painting, character design, figure drawing, or anatomy study. This skill
  activates automatically and silently enhances any image generation or drawing task
  with proper manga-style hand and foot anatomy. It covers: prompt engineering for
  anime AI image generators, kawaii hand poses, simplified manga construction
  methods, and code-generated reference images for 14yo-character proportions.
  Also trigger when the user complains about hands/feet looking wrong, mentions
  "moe", "kawaii", "anime style", "manga style", "loli", "chibi", or similar.
---

# Hands & Feet Drawing — Manga Loli Style (~14 years)

This skill provides anatomical knowledge, manga-style construction methods, prompt-engineering recipes for anime AI generators, and code-generated reference images for drawing soft, youthful hands and feet.

## How This Skill Works

- **Automatic enhancement:** Whenever you detect a task involving image generation, drawing, painting, character design, or any visual output with young female characters, silently apply the manga hand/foot anatomy from this skill.
- **Progressive disclosure:** This file contains quick-reference cards. Read the first paragraph of each reference file to decide if you need full contents.
- **Three contexts:** For **AI image generation** (NovelAI, NijiJourney, SD), use the prompt-engineering guidance. For **code-based drawing**, use the construction patterns. For **diagnosis**, use the checklist.

---

## Quick Anatomy Card — 14-Year-Old Anime Girl Hand

- **Body proportion:** 5.5–6 head-body ratio. Hands are ~3/4 head height (same as adult in absolute terms, but slightly plumper/softer).
- **Soft joint definition:** MCP knuckles are subtly visible, NOT prominent. PIP and DIP creases are delicate — in manga style, often omitted entirely or shown as faint lines.
- **Knuckle arc:** Still present (MCP joints form a gentle downward curve), but much softer than adult. The middle knuckle is slightly highest.
- **Finger shape:** Tapered, slender, with rounded tips. Width at base = ~2/3 of adult. Fingers look "delicate" not "bony."
- **Finger length cascade:** Middle > Ring > Index > Pinky. Thumb reaches to mid-index proximal phalanx.
- **Nails:** Small, oval/almond-shaped. Sit further back from the fingertip than adult nails. Often highlighted with a subtle gloss in anime.
- **Palmar creases:** In manga style, usually omitted or shown as one or two faint lines (not the full three-crease adult pattern).
- **Thumb:** Slightly thinner, less muscular thenar eminence. Still opposes correctly at ~90°.
- **Webbing:** More subtly indicated than adult. In simplified manga, the webbing curve is a single gentle arc.

## Quick Anatomy Card — 14-Year-Old Anime Girl Foot

- **Proportion:** Foot length ≈ 1/6.5–1/7 of total height. Overall smaller and narrower than adult.
- **Arch:** A gentle curve is visible on the medial side but less pronounced than adult. Slightly flat appearance is normal for young feet.
- **Toes:** Rounded, plump tips. Toe cascade: Big > 2 > 3 > 4 > 5. In manga, often simplified to 2-3 visible toe shapes in shoes/sandals.
- **Ankle:** Medial malleolus higher (subtle), lateral lower — but both are less prominent than adult. In manga, often just a smooth contour.
- **Achilles tendon:** Barely visible — young feet have more subcutaneous fat here.
- **Heel:** Smaller, rounder, less prominent calcaneus.
- **Sole:** Soft fat pads under the heel and metatarsal heads. Arch area has thinner padding.
- **Key manga difference:** Overall softer, rounder, and simpler than realistic anatomy. Think "cute" rather than "accurate."

---

## Manga-Style Construction Method (5 Steps)

1. **Block in the simple form.**
   - Hand = a rounded pentagon (palm) + 5 tapered ovals (fingers). Less angular than realism.
   - Foot = a wedge / soft shoe-shape from heel to toe-box.

2. **Mark the joints softly.**
   - MCP knuckles = subtle bumps, not sharp circles.
   - In manga, you often only mark MCP + one flex point per finger (merging PIP/DIP into a single curve).

3. **Draw the silhouette with smooth arcs.**
   - Use gentle curves, avoid sharp corners. Fingers are delicate sausages — slightly wider at base, gracefully tapered.
   - No hard bone lines on the dorsum of the hand.

4. **Add minimal details.**
   - One faint palmar crease line at most.
   - Small oval nails near (but not at) the fingertip.
   - Subtle webbing arcs between fingers.

5. **Check proportions against the face.**
   - Open hand should approximately cover the face area.
   - Middle finger ≈ nose length.
   - If proportions look off, the hand is probably too large (common mistake: drawing adult hands on young characters).

---

## Context-Specific Workflows

### A. AI Image Generation (NovelAI / NijiJourney / SD Anime Models)

When writing prompts for anime-style AI image generators:

1. **Always include** explicit finger count + "soft", "delicate", "slender" descriptors.
2. **Always include** negative terms for adult/jagged hands.
3. For **NovelAI / NAI Diffusion**: use quality tags + "detailed hands" in positive.
4. For **NijiJourney**: `--niji 6` has excellent anime hand rendering. Add `--style cute` for softer look.
5. For **SD anime models** (Anything-v5, AOM3, Meina, Counterfeit): use dedicated hand-improvement LoRAs.
6. Read `references/ai-prompt-engineering.md` for model-specific templates.

### B. Code-Based Drawing (SVG / p5.js / Canvas)

When writing code for manga-style hands:

1. Use the 14yo coordinate tables from `references/code-drawing-patterns.md`.
2. Fingers are thinner (`scale * 0.12` vs adult `0.14`), rounded tips.
3. Joint dots should be smaller / fewer.
4. Run `scripts/generate_hand_svg.py --style manga` for manga-proportioned reference SVGs.

### C. Diagnosis — Fixing Wrong Hands/Feet

Quick manga-specific checks:
1. Fingers look bony/knobby → too adult. Soften joint definition.
2. Hand too large → check face-size comparison.
3. Fingers all same width → add taper.
4. Nails too prominent → reduce nail size, push back from tip.
5. Creases too harsh → remove or soften palm lines.

---

## Reference File Guide

| File | Contents | Read when... |
|------|----------|-------------|
| `references/hand-anatomy.md` | Full hand anatomy + manga simplifications | Drawing a hand; need anatomical reference |
| `references/foot-anatomy.md` | Full foot anatomy + manga simplifications | Drawing a foot |
| `references/common-proportions.md` | 14yo proportion tables, age/gender comparisons | Character has specific age/body type |
| `references/common-poses.md` | Manga/kawaii hand poses catalog | Specific pose needed (peace sign, heart finger, etc.) |
| `references/ai-prompt-engineering.md` | Anime model-specific prompt recipes | Writing prompts for anime AI generators |
| `references/code-drawing-patterns.md` | SVG/p5.js/Canvas patterns, manga coordinate tables | Writing drawing code |
| `references/common-ai-mistakes.md` | Anime-specific AI failure catalog | Diagnosing wrong hands/feet in AI output |

---

## Using the Scripts

```bash
# Manga-style hand reference (14yo proportions)
python scripts/generate_hand_svg.py --style manga --pose relaxed_open --hand right --output hand_ref.svg

# Manga-style foot reference
python scripts/generate_foot_svg.py --style manga --pose standing --foot right --output foot_ref.svg

# Supports both left/right and multiple poses
python scripts/generate_hand_svg.py --style manga --pose peace --hand left --output peace_left.svg
```

Available poses: `relaxed_open`, `fist`, `pointing`, `spread`, `peace` (manga only), `heart_finger` (manga only), `cup_hold` (hand); `standing`, `walking`, `dangling`, `tiptoe` (foot).

**Left vs Right:** Scripts mirror x-coordinates for left side. All reference files default to right side — mirror for left. Anatomy is bilaterally symmetrical.
