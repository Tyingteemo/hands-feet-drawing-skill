# Common AI Mistakes — Manga Loli Style (~14yo)

Diagnostic catalog of common AI failures when generating anime-style hands/feet for young characters.

## Table of Contents
1. Manga-Specific Hand Mistakes
2. Manga-Specific Foot Mistakes
3. Anime AI Diagnostic Checklist

---

## 1. Manga-Specific Hand Mistakes

### 1.1 Adult Hands on Young Characters (AGE MISMATCH)

**Appearance:** Character has a youthful face but adult-proportioned hands with visible knuckles, angular bones, thick fingers, or prominent nails.

**Root cause:** Anime AI models are primarily trained on adult character art (shounen/seinen). The model defaults to adult hand proportions unless explicitly told otherwise.

**Fix:**
- Positive: "young hands, soft delicate hands, youthful hands, no knuckles, smooth skin"
- Negative: "adult hands, bony hands, veiny hands, prominent knuckles"
- For SD: use a "kawaii hands" or "soft hands" LoRA

### 1.2 Bony/Knobby Fingers

**Appearance:** MCP knuckles are sharp bumps, fingers have visible PIP/DIP joints, extensor tendons visible as ridges.

**Root cause:** Model renders realistic hand anatomy instead of manga simplification.

**Fix:**
- Positive: "soft rounded fingers, no visible knuckles, smooth hands, simplified anime hands"
- Negative: "knuckles, joints, tendons, realistic hands, bony fingers"

### 1.3 Male/Adult Finger Proportions

**Appearance:** Fingers too thick, square tips, wide nails, bulky palm.

**Root cause:** The model doesn't distinguish male vs female hand proportions well.

**Fix:**
- Positive: "slender fingers, delicate hands, feminine hands, small cute hands, tapered fingers, rounded fingertips"
- Negative: "thick fingers, masculine hands, large hands, square nails"

### 1.4 Veins/Too Much Detail

**Appearance:** Dorsal veins, deep palmar creases, knuckle wrinkles visible.

**Root cause:** Model adds realistic detail that conflicts with anime style.

**Fix:**
- Positive: "smooth skin, soft skin, simple anime hands, clean line art"
- Negative: "veins, wrinkles, detailed hands, realistic skin texture, pores"

### 1.5 Wrong Nail Style

**Appearance:** Square adult nails, long pointed nails, nails at very fingertip edge, no nail gloss.

**Root cause:** AI doesn't know manga nail conventions.

**Fix:**
- Positive: "small oval nails, cute nails, subtle nail gloss, nails set back from fingertip"
- Negative: "long nails, square nails, thick nails, claw nails, french tips"

### 1.6 Extra Fingers in Complex Poses

**Appearance:** 6+ fingers appear, especially in peace signs, heart fingers, or interlocked hands.

**Root cause:** Manga hand poses with overlapping fingers create ambiguity for the model.

**Fix:**
- Positive: "exactly five fingers, clear finger separation, [specific finger count per hand]"
- Negative: "extra fingers, six fingers, fused fingers"
- For peace sign: explicitly state "two fingers raised, three fingers curled"
- For heart: "thumb and index touching, three fingers relaxed behind"

### 1.7 "Mitten" Hands (No Finger Separation)

**Appearance:** Hand looks like a rounded blob, finger gaps not rendered.

**Root cause:** Hand is too small in image, or the model doesn't distinguish manga finger gaps from the simplified style.

**Fix:**
- Positive: "clearly separated fingers, visible finger gaps, defined fingers"
- Zoom in or increase hand prominence in composition
- Negative: "mitten hands, fused fingers"

### 1.8 Wrong Hand Age for Chibi/Loli

**Appearance:** Chibi character (3-4 heads) but hands have defined fingers with nails and joints — should be simplified stubs.

**Root cause:** Same hand anatomy applied regardless of character body proportion.

**Fix:**
- For chibi: "chibi hands, simplified hands, small round hands, no finger details"
- For 14yo specifically: "youthful hands, soft knuckle definition, delicate fingers"

---

## 2. Manga-Specific Foot Mistakes

### 2.1 Adult Foot Size

**Appearance:** Feet too large relative to character's body; foot length exceeds head length.

**Root cause:** AI defaults to adult 7-8 head-body foot proportions.

**Fix:**
- "small feet, cute small feet, delicate feet, young feet"
- "foot proportionally smaller than adult"
- For 14yo: foot = ~0.85 head (not 1 head like adult)

### 2.2 Overly Defined Ankle Bones

**Appearance:** Sharp medial and lateral malleoli, both clearly visible bumps.

**Root cause:** Realistic ankle rendering.

**Fix:**
- "soft ankles, smooth ankle contour, cute ankles"
- Negative: "bony ankles, sharp ankle bones, protruding ankle bones"

### 2.3 Adult Foot Arch

**Appearance:** High, pronounced medial arch visible in side view.

**Root cause:** Model renders adult foot structure.

**Fix:**
- "soft foot arch, gentle arch, cute feet"
- Negative: "high arch, defined foot arch"

### 2.4 Toe Detail Overload

**Appearance:** Individual toe joints, knuckle creases, toenail cuticles visible.

**Root cause:** Model adding unnecessary detail.

**Fix:**
- "simple toes, soft rounded toes, cute toes, minimal toe detail"
- Negative: "toe knuckles, toe joints, detailed toes"

---

## 3. Anime AI Diagnostic Checklist

When diagnosing manga hand/foot issues, ask:

| # | Check | Good (14yo Manga) | Bad (Too Adult) |
|---|-------|-------------------|-----------------|
| 1 | Knuckles visible? | None or very subtle MCP | Sharp MCP + PIP + DIP |
| 2 | Finger thickness? | Slender, < adult by ~15% | Adult width or thicker |
| 3 | Nail style? | Small ovals, set back from tip | Square, at fingertip edge |
| 4 | Palm creases? | 0–1 faint line | 3 deep lines |
| 5 | Dorsal detail? | Smooth, no tendons/veins | Tendon ridges, veins |
| 6 | Finger count? | Exactly 5, clearly separated | 6+ fingers or mitten hand |
| 7 | Foot vs head? | Foot < head length | Foot ≥ head length |
| 8 | Arch height? | Gentle, ~half adult | High, pronounced |
| 9 | Ankle bones? | Smooth contour, subtle bump | Sharp double bumps |
| 10 | Toe style? | Rounded beans, no joints | Individual knuckles visible |
