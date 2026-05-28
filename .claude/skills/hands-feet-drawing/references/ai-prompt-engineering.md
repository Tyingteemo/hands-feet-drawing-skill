# AI Prompt Engineering for Hands & Feet

## Table of Contents
1. Why AI Struggles with Hands & Feet
2. Universal Prompt Additions (Model-Agnostic)
3. Midjourney Specific
4. Stable Diffusion / Flux Specific
5. DALL-E 3 Specific
6. ComfyUI / Workflow Guidance
7. Incremental Refinement Strategy

---

## 1. Why AI Struggles with Hands & Feet

**Hands:** 27 bones in a small area with enormous pose variation (each finger has 4 degrees of freedom, the thumb has 5). The pose space is so large that the training data is sparse for any specific configuration. The model sees many configurations but not enough of any single one, leading to statistical averaging — the classic "extra fingers" as the model guesses multiple finger configurations simultaneously.

**Feet:** Less photographed at high resolution from multiple angles compared to faces and hands. The subtleties of arch variation, toe alignment, and ankle anatomy are underrepresented in training data.

**Self-occlusion:** Hands especially occlude their own parts (fingers behind other fingers, thumb behind the palm), creating ambiguous edge cases that the model resolves poorly.

---

## 2. Universal Prompt Additions (Model-Agnostic)

### Always Include in Positive Prompts

```
[anatomically correct hands and feet, natural hand pose, clearly defined knuckles and fingernails, five fingers on each hand, natural finger proportions, visible foot arch, correct toe anatomy, natural joint definition]
```

### Pose-Specific Additions

| Pose | Prompt Addition |
|------|----------------|
| Relaxed hand | [relaxed open hand, fingers gently curved, natural finger spacing] |
| Fist | [closed fist, fingers curled into palm, knuckles visible] |
| Pointing | [pointing finger, index finger extended, other fingers curled naturally] |
| Grasping object | [hand grasping [object], fingers wrapped around [object], natural grip] |
| Standing foot | [foot standing flat on ground, visible medial arch, natural toe splay] |
| Walking | [foot in mid-stride, dynamic pose, natural toe-off position] |

### Universal Negative Prompt Additions

Copy-paste these into the negative prompt:

```text
extra fingers, fused fingers, missing fingers, fewer than five fingers, six fingers, deformed hands, bad anatomy, extra limbs, mutated hands, poorly drawn hands, extra digits, fewer digits, malformed hands, long fingers, webbed fingers, conjoined fingers, extra toes, missing toes, deformed feet, bad foot anatomy, mutated feet, extra limbs, missing limbs, distorted hands, claw hand, mitten hand, floating limbs, disembodied limbs, bad proportions, disjointed anatomy, impossible anatomy
```

---

## 3. Midjourney Specific

### Parameters

- `--no extra fingers, deformed hands, bad anatomy, extra limbs` (append to any prompt that includes hands)
- `--style raw` — reduces artistic exaggeration, produces more literal/anatomical renderings
- `--iw 2` — when using a reference image that has good hands (image weight)
- `--cref <URL>` — character reference to maintain consistent hand proportions across generations

### Prompt Structure

```
[subject/scene], [pose description], anatomically correct hands, natural hand pose, five fingers --ar 3:2 --style raw --no extra fingers, deformed hands, bad anatomy
```

### Midjourney Version Notes

- **V6 / V6.1:** Significantly improved hand rendering. Explicit finger counts still help. `--style raw` reduces hand errors.
- **V7:** Further improvements. The `--no` parameter continues to be effective.
- **General rule:** When Midjourney gets hands wrong, first try: regenerating with `--style raw` and the negative prompt. If still bad, add more explicit hand description to the positive prompt.

### Character Reference

Use `--cref` with an image that has correctly-drawn hands. This improves hand consistency and reduces the random variation in hand anatomy across generations.

---

## 4. Stable Diffusion / Flux Specific

### Negative Prompt Embed

Include the full universal negative prompt in the negative prompt field. For SDXL, consider using a dedicated negative TEXT encoder or embedding for "bad hands."

### Dedicated LoRAs

Several community LoRAs specifically improve hand rendering:
- **"Perfect Hands" / "Hand Improvement"** LoRAs — train the model to produce better hand anatomy
- Apply at weights between 0.6-0.8 (higher weights may introduce artifacts)

### ControlNet

The most reliable way to fix hands in Stable Diffusion:

| ControlNet Type | How It Helps |
|----------------|-------------|
| **OpenPose** | Use a reference image with a similar hand pose. OpenPose will detect the skeleton and enforce a similar hand configuration. |
| **Depth** | Provide a depth map of the hand pose. Ensures correct spatial relationships between fingers. |
| **IP-Adapter** | Use a reference hand image for compositional guidance. |

### Inpainting Workflow

When hands come out wrong in an otherwise good image:

1. Mask just the hand region (leave a small margin around the hand)
2. Set denoising strength to 0.75-0.85 (high enough to fix structure, low enough to match the rest)
3. Use a focused prompt for the inpainting: `[anatomically correct right/left hand, [pose description], natural fingers]`
4. Use strong negative prompt for the inpaint region
5. Run 2-3 passes until the hand looks correct

### Regional Prompting (For Couple / Regional Prompter extension)

If using extensions like "For Couple" or "Regional Prompter":

- Assign a dedicated prompt region to each hand
- Prompt the region with: `[hand, [pose], [view], anatomically correct hand, five fingers]`
- This prevents the model from "borrowing" features from the main prompt

### Flux Specific

- Flux has better native hand rendering than SDXL
- Still benefits from explicit finger counts and pose descriptions
- Negative prompting works differently in Flux — use natural language negatives rather than embedded negative prompts
- Example: "The hands should have five fingers, not six. The fingers should not be fused or deformed."

---

## 5. DALL-E 3 Specific

### Strengths

- DALL-E 3 has the best native hand rendering of all major models
- Typically gets finger counts correct without explicit prompting
- Better at rendering hand-object interactions

### Still Beneficial

```
Anatomically correct hands with exactly five fingers each, clearly defined knuckles and fingernails, natural hand pose
```

### When Hands Go Wrong

- Regenerate with more explicit hand description (unlike SD, DALL-E's inpainting has different behavior and may not help)
- Try requesting a "close-up" view of the hand area if the full composition has hand issues
- Break the pose into simpler components

---

## 6. ComfyUI / Workflow Guidance

- **Node-based approach:** Always include a "CLIP Text Encode" node for negative prompt with the full negative terms
- **For hands:** Chain a hand-improvement LoRA node before the KSampler
- **ControlNet workflow:** Use OpenPose + hand reference image as a preprocessor → ControlNet → KSampler chain
- **Face and hands refinement:** Use separate KSampler passes for face and hands with lower denoising

---

## 7. Incremental Refinement Strategy

```
First pass:  Basic prompt with "anatomically correct hands, five fingers"
↓ (check results)
Second pass: Add negative prompt + pose-specific description
↓ (check results)
Third pass:  Add ControlNet / LoRA + focus on problem hand
↓ (check results)
Fourth pass: Inpaint / regenerate problem hand region with focused prompt
↓
If still failing: Generate hands separately and composite, or use a reference image
```

### Key Principle

> The more explicit you are about hand and foot anatomy, the fewer errors the AI will make. "Natural hands" is not enough — specify finger count, pose, joint visibility, and anatomical correctness.
