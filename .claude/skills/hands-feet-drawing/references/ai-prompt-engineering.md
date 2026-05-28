# AI Prompt Engineering — Manga Loli Style (~14yo)

## Table of Contents
1. Why Anime AI Struggles with Young Hands
2. Universal Manga Positive Prompt Additions
3. Universal Manga Negative Prompt Additions
4. NovelAI / NAI Diffusion Specific
5. NijiJourney Specific
6. Stable Diffusion Anime Models (Anything-v5, AOM3, Meina, Counterfeit)
7. ComfyUI / Workflow Guidance
8. DALL-E 3 Specific
9. Incremental Refinement for Anime Hands

---

## 1. Why Anime AI Struggles with Young Hands

- **Training data bias:** Most anime training images show adult-proportioned hands (shounen/seinen). Young/small hands are underrepresented.
- **Manga simplification:** Real hands have 27 bones with distinct joints. Manga hands have ~3-5 visible features. AI gets confused about which features to include vs omit.
- **The "adult hand" problem:** AI defaults to rendering adult-knuckled, veiny hands on characters intended to be 14. The model doesn't understand "age" in hand anatomy.
- **Finger count errors:** Same root cause as realistic — statistical averaging of multiple configurations. Extra bad in anime because training data includes chibi hands (3-4 fingers), stylized hands, and simplified hands mixed together.

---

## 2. Universal Manga Positive Prompt Additions

### Always Include:
```text
soft delicate hands, youthful hands, slender tapered fingers, small oval nails, smooth skin, no visible knuckles, no veins, cute hands, manga style hands, anime hands
```

### 14yo-Specific:
```text
young hands, teenage girl hands, soft knuckle definition, rounded fingertips, small neat nails, delicate fingers, kawaii hands
```

### Pose-Specific (Manga):

| Pose | Prompt Addition |
|------|----------------|
| Peace sign | [peace sign hand pose, two fingers raised, soft rounded fingers, kawaii gesture] |
| Heart finger | [heart shape made with thumb and index finger, cute hand gesture, idol pose] |
| Relaxed open | [relaxed open hand, palm facing viewer, soft rounded palm, delicate fingers] |
| Holding cup | [hands gently holding cup, soft grip, slender fingers wrapped around cup] |
| Pointing | [pointing with index finger, soft rounded fingertip, cute pointing pose] |

---

## 3. Universal Manga Negative Prompt Additions

```text
adult hands, bony hands, veiny hands, old hands, wrinkled hands, masculine hands, large hands, thick fingers, prominent knuckles, sharp knuckles, defined tendons, realistic hands, muscular hands, rough skin, thick nails, long fingernails, dirty nails, claw hands, extra fingers, fused fingers, six fingers, deformed hands, bad anatomy, mutated hands
```

---

## 4. NovelAI / NAI Diffusion Specific

### Model: NAI Diffusion V3 / V4

**Best practices:**
- Use the quality tag set: `masterpiece, best quality, amazing quality`
- Add `detailed hands` for better finger rendering
- The model responds well to Danbooru-style tags

**Positive prompt template:**
```
masterpiece, best quality, 1girl, [age:14], [scene description], [pose],
soft hands, delicate fingers, kawaii hands, small nails, smooth skin,
anatomically correct hands, five fingers, cute hands
```

**Negative prompt template:**
```
lowres, bad anatomy, bad hands, extra fingers, fused fingers, missing fingers,
bony hands, adult hands, veiny hands, realistic, photorealistic, 3d,
wrinkled skin, thick fingers, prominent knuckles
```

**UC (Undesired Content) preset:**
- NovelAI has built-in "Bad Anatomy" UC presets — always enable these
- Consider adding a custom UC embedding for hands if generating many character images

---

## 5. NijiJourney Specific

### Model: Niji 6

**Best practices:**
- `--niji 6` has excellent anime hand rendering compared to v5
- `--style cute` produces softer, more youthful features
- `--style expressive` for dynamic gestures (peace signs, heart poses)

**Prompt template:**
```
[character description], [pose], soft delicate hands, youthful hands,
five fingers, small cute nails, anime style --niji 6 --style cute
--no adult hands, bony hands, realistic hands, extra fingers, deformed hands
```

**Character reference:**
- `--cref <URL>` with a reference character that has good hands improves hand consistency dramatically

---

## 6. Stable Diffusion Anime Models

### Supported models: Anything-v5, AOM3 (AbyssOrangeMix3), MeinaMix, Counterfeit

**Universal SD anime positive:**
```
1girl, young, [age:14], [scene], [pose], masterpiece, best quality,
soft delicate hands, youthful hands, slender fingers, small oval nails,
anatomically correct hands, five fingers, cute hands, smooth skin
```

**Universal SD anime negative:**
```
(worst quality, low quality:1.4), adult hands, bony hands, veiny hands,
prominent knuckles, sharp knuckles, thick fingers, muscular hands,
(bad anatomy:1.2), (bad hands:1.3), extra fingers, fused fingers,
missing fingers, deformed hands, realistic, photorealistic
```

### Recommended LoRAs:
- **"Better Hands" / "Perfect Hands" LoRA** — general hand improvement
- **"Kawaii Hands" LoRA** — specifically for soft, youthful hands (CivitAI)
- Apply at 0.5–0.7 weight (lower than adult hand LoRAs to avoid over-correction)

### ControlNet for anime hands:
- **OpenPose** with a reference image of a young character with good hand pose
- **Depth** control for hand-object interaction (holding cups, phones)
- **IP-Adapter** with a reference hand image for style consistency

### Inpainting (if hands go wrong):
1. Mask hand region
2. Denoising: 0.65–0.75 (lower than realistic — anime hands are simpler)
3. Focused prompt: `soft youthful hand, [pose], delicate fingers, five fingers`
4. 2–3 passes

---

## 7. ComfyUI / Workflow Guidance

- **Node setup:** SDXL/SD3 anime checkpoint → Hand Improvement LoRA → KSampler
- **For hands specifically:** Add a "Detailer" node (like SEGS Detailer) focused on hand regions
- **Negative embedding:** Use `bad-hands-5` or similar negative embedding
- **Face + hands refinement:** Two-pass workflow — generate full image, then hand-detail pass with higher CFG

---

## 8. DALL-E 3 Specific

- DALL-E 3 has good native hand rendering but tends toward realistic proportions
- Explicitly request "anime style, soft youthful hands, delicate fingers"
- If hands look too adult, add "cute young hands, kawaii style, simplified anime hands"
- DALL-E inpainting is limited — better to regenerate with more explicit prompt

---

## 9. Incremental Refinement for Anime Hands

```
Pass 1: Basic prompt + "soft hands, five fingers, anime style"
↓ (check: are hands youthful or adult-looking?)
Pass 2: Add "youthful hands, no knuckles, delicate fingers" + negative "adult hands"
↓ (check: finger count correct? no extra/missing?)
Pass 3: Add LoRA / ControlNet + pose-specific description
↓ (check: style consistent with overall image?)
Pass 4: Inpaint problem areas with focused hand prompt
↓
If still failing: Generate hands separately as reference, then composite
```

### Key Principle for Anime

> In realistic art, MORE detail = better hands. In anime, LESS detail = better hands. The AI needs to be told explicitly NOT to render adult anatomical features. "No knuckles, no veins, no tendons" is as important as "five fingers."
