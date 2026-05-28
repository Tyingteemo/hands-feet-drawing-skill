# Hands & Feet Drawing — Claude Code Skill

A Claude Code skill for drawing anatomically correct hands and feet. Provides:

- **Anatomical knowledge** — bones, joints, proportions, surface landmarks
- **AI image generation recipes** — prompt engineering for Midjourney, Stable Diffusion, DALL-E, Flux
- **Code-based drawing patterns** — SVG, p5.js, HTML Canvas coordinate tables and construction methods
- **Diagnostic tools** — common AI mistakes catalog with fixes
- **Reference SVGs** — Python scripts to generate annotated hand/foot reference images

## Installation

```bash
# Clone the repo
git clone https://github.com/Tyingteemo/hands-feet-drawing-skill.git

# Or copy the skill into your project
cp -r hands-feet-drawing-skill/.claude/skills/hands-feet-drawing your-project/.claude/skills/
```

## Usage

This skill triggers **automatically** whenever you work on image generation, drawing, character design, or any visual output involving human figures. No manual invocation needed.

### Manual reference generation

```bash
# Generate hand reference SVG
python .claude/skills/hands-feet-drawing/scripts/generate_hand_svg.py \
  --pose relaxed_open --hand right --output hand_ref.svg

# Generate foot reference SVG
python .claude/skills/hands-feet-drawing/scripts/generate_foot_svg.py \
  --pose standing --foot right --view medial --output foot_ref.svg
```

## Skill Structure

```
hands-feet-drawing/
├── SKILL.md                              # Main skill file
├── references/
│   ├── hand-anatomy.md                   # Full hand anatomy reference
│   ├── foot-anatomy.md                   # Full foot anatomy reference
│   ├── common-proportions.md             # Proportion tables by age/gender
│   ├── common-poses.md                   # Pose catalog with joint positions
│   ├── ai-prompt-engineering.md          # Prompt templates per AI model
│   ├── code-drawing-patterns.md          # SVG/p5.js/Canvas construction code
│   └── common-ai-mistakes.md             # Diagnostic failure catalog
├── scripts/
│   ├── generate_hand_svg.py              # Hand reference SVG generator
│   └── generate_foot_svg.py              # Foot reference SVG generator
└── assets/
    ├── proportion-grid.svg               # Measurement reference grid
    └── skeleton-template.svg             # Hand skeleton wireframe
```

## License

Apache 2.0
