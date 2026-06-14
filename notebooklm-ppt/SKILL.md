---
name: notebooklm-ppt
description: >
  Use this skill whenever the user wants to transform a PPT plan, outline, or rough
  slides into a visually stunning, design-forward presentation. Trigger phrases include:
  "make my PPT beautiful", "turn this into a wow deck", "design my slides", "upgrade
  my presentation", "make this look amazing", or when a user provides a PPT plan/outline
  and wants it turned into a finished, styled .pptx file. Also use when the user asks
  for a specific visual style (editorial, magazine, neo-retro, minimalist, sports, etc.)
  applied to a slide deck.
---

# WOW-PPT Skill

This skill transforms boring PPT plans into visually stunning, design-forward presentations
by combining the NotebookLM style prompt library with Claude Code's native PPTX generation.

> **Also read:** `/mnt/skills/public/pptx/SKILL.md`  -  this skill builds on top of the pptx
> skill. Read both before starting.

---

## Workflow Overview

```
1. Parse user input (outline / plan / rough content)
2. Ask user to pick a visual style (or auto-select based on content)
3. Map style → design spec (colors, fonts, layout rules)
4. Plan slides with layout variants
5. Generate .pptx using pptxgenjs
6. QA visually and fix
7. Deliver
```

---

## Step 1  -  Parse the Input

The user will provide one of:
- A rough bullet-point outline ("Plan")
- A text narrative describing each slide
- An existing .pptx to redesign

Extract from the input:
- **Topic / purpose** of the deck (sales pitch? keynote? product launch? research?)
- **Audience** (investors? team? public?)
- **Slide count** (estimate if not given; aim for 8–15 slides for most requests)
- **Key content per slide** (title, main message, supporting data)

If the input is an existing `.pptx`, read it first:
```bash
python -m markitdown input.pptx
```

---

## Step 2  -  Style Selection

Present the user with the style menu below (or auto-select if they've already indicated a vibe).

### Available Visual Styles

| # | Style Name | Vibe | Best For |
|---|-----------|------|----------|
| 1 | **Modern Newspaper** | Electric yellow + black, Swiss editorial, extreme typography | Business, media, research |
| 2 | **Sharp Minimalism** | Grid-based, architectural whitespace, top-left nav | Portfolio, agency, premium brand |
| 3 | **Yellow × Black Editorial** | High-contrast, fashion magazine, dynamic serif | Bold brand announcements |
| 4 | **Black × Orange Agency** | Blood orange accent, creative studio aesthetic | Agency pitches, creative work |
| 5 | **Neo-Retro Dev Deck** | Grid paper bg, hot pink/cyan/yellow blocks, pixel icons | Tech, dev tools, startup |
| 6 | **Pink Street Style** | Pink bg, deformed pop illustrations, street-meets-cute | Consumer, youth, lifestyle |
| 7 | **Digital / Neo / Pop** | Organic blob shapes, neon pink/cyan/purple, amoeba motifs | Community, social, education |
| 8 | **Sports / Athletic** | Dark bg, Bolt Lime + Neon Orange, diagonal cuts | Sports, energy, fitness |
| 9 | **Studio / Premium Mockup** | Electric Purple + Acid Yellow, device mockup style | Product launches, SaaS |
| 10 | **Tech / Art / Neon** | Beige + neon yellow geometry, constructivist collage | AI, research, thought leadership |
| 11 | **Classic / Pop (Sculpture × Vaporwave)** | Marble statues + modern pop items, high saturation | Events, cultural, provocative |
| 12 | **Anti-Gravity / Living Artifact** | White space, soft blue-to-violet gradients, Apple-level calm | AI infrastructure, product docs |
| 13 | **Royal Blue × Red Watercolor** | Wet watercolor texture, classical palette | Academic, nonprofit, arts |
| 14 | **Seminar Minimal** | White + red accent, fashion portrait photos, dynamic type | Education, conference talks |
| 15 | **Deformed Flat Persona** | Flat colors, illustrated deformed figures, thick outlines | Storytelling, HR, training |

---

## Step 3  -  Design Specs Per Style

Use these specs when generating slides. Each spec maps to pptxgenjs properties.

### Style 1: Modern Newspaper
```yaml
background: "#FFFFFF or #F5F5F5"
text_primary: "#111111"
accent_1: "#FFCC00"  # Electric Yellow
accent_2: "#FF3333"  # Alert Red
font_heading: "Impact"
font_body: "Arial"
heading_size: 48-72pt  # Ultra large
body_size: 10-12pt     # Extreme jump ratio (10:1)
layout_rule: "Asymmetric. Title off top-left or bottom-left. Vast negative space."
cover_rule: "Swiss Style. Off-center title 2-5 words. Ultra-small benefit subtitle."
content_rule: "1 slide = 1 message. Yellow highlight on key words. Monochrome cutout images."
```

### Style 2: Sharp Minimalism
```yaml
background: "#E9E9E9 or #FFFFFF"
text_primary: "#000000 or #333333"
accent: "#000000"  # Black lines only
dark_mode_bg: "#000000"  # For emphasis slides
font_heading: "Helvetica or Arial Black"
font_body: "Calibri Light"
nav_element: "Section number '01. TITLE' top-left, every slide"
layout_rule: "Strict grid, wide margins, large empty areas = luxury"
special_slides: "Dark mode (black bg) for emphasis moments"
```

### Style 3: Yellow × Black Editorial
```yaml
background: "#FFCC00"  # Yellow
text_primary: "#000000"
accent: "#000000"
font_heading: "Large bold serif (Georgia Black)"
font_body: "Arial"
aesthetic: "Fashion magazine. Unique photography-style images, handwriting elements, sticker-like accents."
layout_rule: "Bold asymmetric, large type as graphic element"
```

### Style 4: Black × Orange Agency
```yaml
background: "#FFFFFF"
text_primary: "#000000"
accent: "#CC4400"  # Blood orange
font_heading: "Arial Black or Impact"
font_body: "Calibri"
aesthetic: "Creative agency. Dynamic simple shapes. English typography accents."
```

### Style 5: Neo-Retro Dev Deck
```yaml
background: "#F5F0E8"  # Cream grid paper
grid_lines: "Very light, subtle square grid"
colors:
  hot_pink: "#FF1493"   # Agent/intelligence
  bright_yellow: "#FFE500"  # Code/tools
  cyan: "#00D4FF"       # Browser/web
  black: "#000000"      # Borders and text
font_heading: "Bold condensed sans-serif (Impact/Arial Black)"
font_body: "Consolas or monospace for labels"
icons: "8-bit / pixel art style"
content_blocks: "Thick black borders on all cards, slight overlaps, controlled imperfection"
layout_rule: "Stacked modular blocks, annotated engineering notes feel"
```

### Style 6: Pink Street Style
```yaml
background: "#FF69B4"  # Pink
text: "#FFFFFF and #000000"
illustrations: "Pop deformed figures, thick outlines, flat colors"
shapes: "Photos cropped into soft squishy shapes"
aesthetic: "Street style meets cute. Loose, energetic."
```

### Style 7: Digital / Neo / Pop
```yaml
background: "#FFFFFF with light dot pattern"
organic_shapes: "Amoeba/cloud blobs in pink, cyan, purple at slide edges"
text_primary: "#000000"
accent_colors: "#FF69B4, #00CED1, #9370DB"  # vivid pink, cyan, purple
font_heading: "Bold gothic, outline text allowed (white fill + black stroke)"
font_body: "Clean gothic sans"
decorations: "Dot patterns, hand-drawn highlights, SNS-style icons"
layout_rule: "Organic, wavy, non-rectangular. Donut charts, bubble clusters."
```

### Style 8: Sports / Athletic
```yaml
background: "#111111"  # Asphalt black
text: "#FFFFFF"
accent_1: "#CCFF00"  # Bolt Lime
accent_2: "#FF4500"  # Neon Orange
gradient_overlay: "Black-to-transparent over action photography"
font_heading: "Extra-bold italic (Impact, Din Condensed)"
font_body: "Italic sans-serif"
shapes: "Skewed rectangles, parallelograms, diagonal cuts"
nav: "Page numbers inside angled diagonal-cut shapes"
```

### Style 9: Studio / Premium Mockup
```yaml
background: "#FFFFFF or #F5F5F7 or #000000"
accent_1: "#8D59E9"   # Electric Purple
accent_2: "#EBE021"   # Acid Yellow
sub_color: "#D8E2EC"  # Pale blue-gray
text: "#FFFFFF (on dark) or #2D2D2D (on light)"
font_heading: "Helvetica Now Display Bold or Arial Black"
heading_mix: "Large English + small translated subtitle"
device_rule: "Device mockup occupies 70-80% of slide area; allow overflow/crop for scale"
studio_rule: "Soft shadows under devices = studio environment"
```

### Style 10: Tech / Art / Neon
```yaml
background: "#E0E0D0"  # Warm gray / beige, matte paper texture
text: "#333333"        # Charcoal, not pure black
accent: "#DFFF00"      # Neon Yellow
line_color: "Ultra-thin 0.5pt gray (architectural draft lines)"
font_heading: "Mix serif (Bodoni/Didot) + sans-serif (Helvetica)"
font_numbers: "Courier New (typewriter style)"
collage: "Monochrome cut-out portraits + neon yellow circles/squares"
diagram_style: "Blueprint / technical drawing with leader lines and Fig. labels"
color_layers: "Grid bg → neon geometry → monochrome photo → text (strict order)"
```

### Style 11: Classic / Pop (Sculpture × Vaporwave)
```yaml
background: "High-saturation solid color, changes per slide (cyan, magenta, yellow, lime, purple)"
subjects: "Classical marble sculptures in different poses per slide"
props: "Modern pop items (sunglasses, headphones, smartphones, food)"
font_heading: "Ultra-bold Helvetica Now Display Black"
text_color: "Max contrast vs background (white, black, or matching accent)"
rule: "No repeat of same statue across slides. Complementary/analogous colors per slide."
shapes: "Geometric scattered elements (circles, squares) as decoration"
```

### Style 12: Anti-Gravity / Living Artifact
```yaml
background: "#FFFFFF"  # Pure white
gradient_accents: "Blue→cyan→violet, very low opacity, corners/edges only, NEVER behind text"
text_primary: "#1A1A1A"  # Very dark gray
accent: "Calm blue (used sparingly for arrows, key icons, emphasis)"
font_heading: "Clean modern sans-serif, slightly rounded, medium-bold"
font_body: "Same family, lighter weight"
layout: "Left-aligned, wide margins, massive white space, one idea per slide"
rule: "Nothing decorative. If it feels 'fun', it's wrong. If it feels 'inevitable', it's right."
copy_tone: "Clear, precise, slightly philosophical. No hype."
```

### Style 13: Royal Blue × Red Watercolor
```yaml
palette: "Royal blue + red watercolor washes"
aesthetic: "Classical, artistic, hand-crafted feel"
best_for: "Academic, arts, nonprofit, foundation"
texture: "Wet-on-wet watercolor effect backgrounds"
```

### Style 14: Seminar Minimal
```yaml
background: "#FFFFFF"
text: "#000000"
accent: "#FF0000"  # Red
font: "Sans-serif, clean"
photos: "High-quality fashion-portrait style images"
typography: "Dynamic, asymmetric placement"
aesthetic: "High-sensibility, high-contrast, conference-quality"
```

### Style 15: Deformed Flat Persona
```yaml
background: "Solid flat single color"
palette: "Gentle tones with white mixed in, max 3 colors"
illustration: "Slightly deformed human figures, thick outlines, flat fill"
outline: "Thick black outlines on all illustrated elements"
aesthetic: "Friendly, approachable, storytelling"
```

---

## Step 4  -  Slide Layout Planning

Before writing code, plan each slide's layout type. Use variety across the deck.

### Layout Vocabulary (mix these)

| Layout | When to Use |
|--------|-------------|
| **Manifesto** | 1 huge headline, minimal text, surrounded by decorative elements |
| **System Architecture** | Stacked layers / boxes showing how components connect |
| **Evolution / Timeline** | Left→right boxes showing progression |
| **Data Callout** | Giant numbers + short label below |
| **Two-Column Split** | Text left, visual/chart right |
| **Card Grid** | 3-4 cards with icon + title + description |
| **Full Bleed** | Image or shape occupies entire slide |
| **VS / Comparison** | Two columns, strong divider, contrasting content |
| **Feature List** | Icon + bold header + 1-line description per item |
| **Dark Mode Emphasis** | Switch to dark background for a key moment |
| **Cover / Hero** | Asymmetric, bold, sets the visual identity |
| **Conclusion / CTA** | Mirror the cover, end strong |

### Slide Structure Template

For each slide, define:
```
Slide N: [Type]  -  [1-line description]
  Content: [what goes here]
  Layout: [which layout type]
  Visual: [what image/shape/chart element]
  Style notes: [any style-specific rule]
```

---

## Step 5  -  Generation (pptxgenjs)

Use pptxgenjs. Key setup:
```bash
npm install -g pptxgenjs
```

### Boilerplate
```javascript
const pptxgen = require("pptxgenjs");
const prs = new pptxgen();
prs.layout = "LAYOUT_WIDE"; // 16:9

// Set master slide defaults
prs.defineSlideMaster({
  title: "MASTER",
  background: { color: "FFFFFF" },
});
```

### Style-Specific Code Patterns

**Bold geometric background block:**
```javascript
slide.addShape(prs.ShapeType.rect, {
  x: 0, y: 0, w: 4.5, h: "100%",
  fill: { color: "111111" }
});
```

**Ultra-large headline (newspaper style):**
```javascript
slide.addText("COLLAPSE", {
  x: 0.3, y: 0.2, w: 8, h: 3,
  fontSize: 120, bold: true, color: "111111",
  fontFace: "Impact", fit: "none"
});
```

**Diagonal cut shape (sports style):**
```javascript
slide.addShape(prs.ShapeType.parallelogram, {
  x: 0.5, y: 0.2, w: 1.2, h: 0.4,
  fill: { color: "CCFF00" }
});
```

**Section nav (minimalism style):**
```javascript
slide.addText("01. INTRODUCTION", {
  x: 0.3, y: 0.15, w: 3, h: 0.25,
  fontSize: 9, color: "999999", bold: false,
  fontFace: "Helvetica"
});
```

**Colored accent card:**
```javascript
slide.addShape(prs.ShapeType.rect, {
  x: 0.5, y: 1.5, w: 3.5, h: 2.5,
  fill: { color: "FF1493" },
  line: { color: "000000", width: 3 }
});
slide.addText("Headline", {
  x: 0.5, y: 1.5, w: 3.5, h: 2.5,
  fontSize: 24, bold: true, color: "FFFFFF",
  align: "center", valign: "middle"
});
```

**Neon highlight on keyword:**
```javascript
// Yellow highlight behind key word
slide.addShape(prs.ShapeType.rect, {
  x: 1.2, y: 2.8, w: 2.5, h: 0.45,
  fill: { color: "FFCC00" }, line: { type: "none" }
});
slide.addText("KEY WORD", {
  x: 1.2, y: 2.8, w: 2.5, h: 0.45,
  fontSize: 20, bold: true, color: "111111"
});
```

**Dot/grid pattern background:**
```javascript
// Simulate grid paper with many small shapes
for (let row = 0; row < 20; row++) {
  for (let col = 0; col < 30; col++) {
    slide.addShape(prs.ShapeType.ellipse, {
      x: col * 0.35, y: row * 0.35,
      w: 0.04, h: 0.04,
      fill: { color: "CCCCCC" }, line: { type: "none" }
    });
  }
}
```

---

## Step 6  -  Critical Design Rules (Apply to All Styles)

From the NotebookLM prompts distilled into rules for pptxgenjs:

1. **1 slide = 1 message.** Strip everything that isn't the core point.
2. **No markdown bullets rendered as text.** If it looks like a default PowerPoint, redo it.
3. **Extreme size contrast.** Headline vs body ratio must be at least 5:1. If headlines are 60pt, body is 12pt.
4. **Asymmetry beats center.** Centered layouts are forgettable. Push elements to extremes.
5. **Dark/light sandwich.** Cover + conclusion = dark. Body slides = light. (Or commit to all-dark.)
6. **Every slide has a visual.** Shape, accent color block, icon, or geometric element at minimum.
7. **Vary layouts.** Never use the same layout twice in a row.
8. **No underlines under titles.** This is the #1 AI slide tell. Use color/space instead.
9. **Color carries meaning.** Use your accent color for the ONE most important thing per slide.
10. **Whitespace is a design choice.** Deliberately empty areas signal confidence.

---

## Step 7  -  QA Checklist

After generation, convert to images and check:

```bash
python scripts/office/soffice.py --headless --convert-to pdf output.pptx
pdftoppm -jpeg -r 150 output.pdf slide
```

Then visually inspect each slide for:

- [ ] Does each slide have ONE clear focal point?
- [ ] Is there sufficient contrast (text vs background)?
- [ ] Are layout types varied across the deck?
- [ ] Do cover and conclusion feel like bookends?
- [ ] Is font size ratio ≥ 5:1 (headline vs body)?
- [ ] Are there any underlines under titles? (Remove them)
- [ ] Are there any plain-text-only slides? (Add visual element)
- [ ] Do accent colors land on the most important element only?
- [ ] Are margins consistent (0.5" min)?
- [ ] Do the style rules specific to the chosen style show up clearly?

---

## Prompting Claude Code

When invoking Claude Code to build this, use:

```
Read /path/to/wow-ppt-skill/SKILL.md and /mnt/skills/public/pptx/SKILL.md before starting.

I have this PPT plan:
[PASTE PLAN HERE]

Apply the [STYLE NAME] visual style.

Requirements:
- [N] slides
- Audience: [WHO]
- Tone: [formal/playful/bold/calm]
- Any specific color preferences: [OR "follow the style spec"]

Generate a complete .pptx file. QA it visually before delivering.
```

---

## Example: Turning a 5-Bullet Plan Into a WOW Deck

**Input plan:**
```
Q3 Product Update
- New feature: AI search
- Performance: 2x faster
- Users: 50k new signups
- Roadmap: Mobile app next
- Thank you
```

**Output planning (Neo-Retro Dev Deck style):**
```
Slide 1: Cover/Manifesto
  "Q3 RESULTS"  -  huge bold Impact on cream grid-paper bg
  Pink block bottom-left, yellow accent top-right

Slide 2: Feature Drop
  "AI SEARCH IS LIVE"  -  manifesto style
  Cyan card with icon + "Find anything in 0.3s"

Slide 3: Performance
  Dark mode. "2×" in 120pt bold center-stage
  "Faster than ever" 14pt below

Slide 4: Growth Callout
  Split: "50,000" in pink 96pt left
  "New users this quarter" right column in small text

Slide 5: Roadmap
  System Architecture layout  -  3 boxes with arrows
  Box 1: ✓ AI Search (yellow), Box 2: ✓ Speed (cyan), Box 3: → Mobile (pink dotted)

Slide 6: Closing
  Cover mirror  -  dark bg, "WHAT'S NEXT" huge
  Small subtitle: "Mobile. Smarter. Faster."
```

---

## Skill Location

Place this skill at:
```
~/.claude/skills/wow-ppt/SKILL.md
```

Or wherever your Claude Code skills directory is configured (check your `CLAUDE.md`).
