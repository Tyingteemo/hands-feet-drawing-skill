# Common AI Mistakes — Hands & Feet

A diagnostic catalog of common failures in AI-generated hands and feet, with causes and fixes.

## Table of Contents
1. Hand Mistakes
2. Foot Mistakes
3. General Diagnostic Approach

---

## 1. Hand Mistakes

### 1.1 Extra Fingers (Polydactyly)

**Appearance:** 6, 7, or more fingers on one hand.

**Root cause:** The diffusion model averages multiple plausible finger configurations simultaneously. It "hedges its bets" by including partial features from multiple configurations, resulting in extra digits.

**Fix:**
- Positive prompt: "exactly five fingers on each hand, anatomically correct hand"
- Negative prompt: "extra fingers, six fingers, seven fingers, polydactyly"
- Use ControlNet with OpenPose skeleton reference
- For SD: use a hand-improvement LoRA

### 1.2 Fused / Webbed Fingers (Syndactyly)

**Appearance:** Two or more fingers merge into a single mass with no clear separation.

**Root cause:** The model fails to resolve interdigital boundaries at the chosen resolution. Common when the hand occupies a small area of the image.

**Fix:**
- Positive prompt: "fingers clearly separated, natural finger spacing, visible gaps between fingers"
- Negative prompt: "fused fingers, webbed fingers, conjoined fingers"
- Increase image resolution or zoom in on hands
- For SD: inpaint the hand region at higher denoising strength

### 1.3 Wrong Number of Joints

**Appearance:** A finger shows 4+ visible joints, or the thumb has 3 joints.

**Root cause:** The model doesn't "know" that fingers have a fixed number of joints. It renders creases and folds as joints.

**Fix:**
- Positive prompt: "anatomically correct finger joints, thumb with two joints, fingers with three joints each"
- Use a reference image with similar hand pose

### 1.4 Backward / Impossible Knuckles

**Appearance:** Knuckles bend in the wrong direction (fingers bending backward past straight, or hyperextension past anatomical limits).

**Root cause:** The model fails to learn joint directionality constraints. This is especially common in dynamic poses.

**Fix:**
- Describe joint direction explicitly: "fingers bending naturally forward, knuckles visible on the back of the hand"
- Negative prompt: "hyperextended fingers, backward bending fingers"
- Use a reference image for pose guidance

### 1.5 Thumb on Wrong Side / Missing Thumb

**Appearance:** Thumb appears on the pinky side of the hand (mirrored), or the hand has no visible thumb.

**Root cause:** The model confuses left and right hands, or the hand is in an ambiguous orientation.

**Fix:**
- Specify: "right hand" or "left hand" explicitly
- "thumb on the radial (inner) side of the hand, visible thumb"
- For close-up hand shots, always specify the hand laterality

### 1.6 All Fingers Same Length

**Appearance:** Fingers look like a row of identical sausages with no length variation.

**Root cause:** The model averages finger lengths to a common value.

**Fix:**
- Positive prompt: "naturally varying finger lengths, middle finger longest, index and ring slightly shorter, pinky shortest"
- Reference proportion: middle > ring > index > pinky > thumb

### 1.7 Mitten Hand (No Individual Finger Definition)

**Appearance:** The hand looks like a mitten — a rounded mass with no clear finger separation.

**Root cause:** The hand is too small in the image frame for the model to resolve individual digits.

**Fix:**
- Zoom in on the hand area (closer framing)
- Increase output resolution
- Use region-specific prompting (high-res focus on hands)
- For SD: use SD upscale or tile-based generation

### 1.8 Disembodied / Floating Hand

**Appearance:** A hand that has no visible connection to an arm or body.

**Root cause:** The hand is at the edge of the image or occluded by other elements.

**Fix:**
- "hand connected to wrist and forearm, visible arm"
- Adjust composition so the wrist is visible
- Negative prompt: "floating hand, disembodied hand"

### 1.9 Claw Hand

**Appearance:** Fingers are curled into an extreme, painful-looking claw shape.

**Root cause:** The model produces exaggerated flexion without understanding anatomical range of motion.

**Fix:**
- "relaxed hand pose, natural finger curvature, comfortable hand position"
- Describe the specific pose in detail rather than leaving it to the model
- Negative prompt: "claw hand, deformed hand, cramped hand"

### 1.10 Invisible or Missing Fingers

**Appearance:** Fewer than 5 fingers visible (not due to occlusion, but because the model omitted them).

**Root cause:** The model treats fingers as optional detail rather than counting them.

**Fix:**
- "five fingers visible, all five fingers clearly shown"
- Negative prompt: "missing fingers, fewer than five fingers"

---

## 2. Foot Mistakes

### 2.1 Extra / Missing Toes

**Appearance:** 6+ toes or fewer than 5 on one foot.

**Root cause:** Same as hand polydactyly — the model averages toe configurations.

**Fix:**
- "five toes on each foot, anatomically correct foot"
- Negative prompt: "extra toes, six toes, missing toes"

### 2.2 Flat Foot (No Arch)

**Appearance:** The foot has a flat, paddle-like silhouette with no visible arch.

**Root cause:** The model doesn't distinguish medial vs. lateral foot contour, or the foot is in a non-medial view.

**Fix:**
- If the view should show the arch: "visible medial foot arch, anatomically correct foot structure"
- "inner side of foot showing natural arch curve"

### 2.3 All Toes Same Length

**Appearance:** All five toes appear the same length.

**Root cause:** The model averages toe lengths instead of applying the natural cascade.

**Fix:**
- "naturally varying toe lengths, big toe longest, toes tapering toward pinky"
- Note: Egyptian foot (1 > 2 > 3 > 4 > 5) is the most common pattern

### 2.4 Impossible Ankle Angle

**Appearance:** The foot is bent at 90+ degrees laterally (sideways) from the leg, which is anatomically impossible.

**Root cause:** The model doesn't understand that the ankle is a hinge joint (dorsiflexion/plantarflexion only).

**Fix:**
- "ankle at natural angle, foot aligned with leg direction"
- Describe the ankle orientation explicitly
- Negative prompt: "twisted ankle, impossible ankle angle"

### 2.5 Mitten Foot

**Appearance:** The foot has no visible toe separation — looks like a block or stump.

**Root cause:** Low resolution or poor training data for foot detail.

**Fix:**
- "clearly defined toes, individual toes visible"
- Zoom in or increase resolution

### 2.6 One Malleolus

**Appearance:** Only one ankle bump is visible when both should be.

**Root cause:** The model renders the ankle as a single generic bump rather than two distinct structures.

**Fix:**
- "visible inner and outer ankle bones (medial and lateral malleoli), inner ankle higher than outer ankle"
- This is especially important in 3/4 and frontal views where both malleoli should be visible

### 2.7 Inverted Foot

**Appearance:** The foot appears to be attached to the wrong leg (left foot on right leg, or vice versa), or the medial/lateral anatomy is swapped.

**Root cause:** The model confuses foot orientation.

**Fix:**
- Specify: "right foot, lateral view" or "left foot, medial view"
- "foot in correct anatomical orientation"

---

## 3. General Diagnostic Approach

When a user says "the hands/feet look wrong but I'm not sure what's wrong," apply this systematic approach:

### Step 1: Count

Count fingers/toes. Are there exactly 5? Is the thumb present? Are all visible joints correct?

### Step 2: Check Proportions

Are the fingers in the correct length cascade? Are the toes graded? Is the palm/arch proportioned correctly?

### Step 3: Check Anatomy

Are the joints in the right locations and directions? Is the thumb opposing correctly? Are the ankle malleoli at different heights?

### Step 4: Check Pose

Does the pose look natural? Are the fingers following the object they're holding? Is the weight distribution correct for standing feet?

### Step 5: Check Connection

Is the hand connected to a wrist? Is the foot connected to an ankle? Are the transitions smooth?

### Step 6: Determine Fix

Based on the error type, apply the corresponding fix from this catalog. For AI-generated images: add specific positive/negative prompt terms. For code-drawn hands: adjust joint coordinates and construction method.
