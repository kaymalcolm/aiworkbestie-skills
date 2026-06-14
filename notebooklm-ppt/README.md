# notebooklm-ppt

Transform a plain outline, slide notes, or rough `.pptx` file into a visually polished, design-forward PowerPoint presentation. Choose from 15 built-in visual styles. Output is a production-ready `.pptx` file.

---

## What It Does

1. Parses your input (text outline, narrative, or existing `.pptx`)
2. Presents a menu of 15 visual styles (or auto-selects based on content)
3. Maps the chosen style to a full design spec (colors, fonts, layout rules)
4. Plans each slide's layout from a 12-layout vocabulary
5. Generates the `.pptx` using `pptxgenjs`
6. QA: converts to PDF via LibreOffice, then to images via `pdftoppm`, visually inspects against a 10-item checklist
7. Delivers the final file

---

## Usage

```
/notebooklm-ppt
```

Trigger phrases:
```
Make my PPT beautiful
Turn this outline into a wow deck
Design my slides
Apply [style name] to this presentation
```

Supply your content in any of these forms:
- Paste an outline directly in the chat
- Share a file path to a `.pptx` file to redesign
- Paste a narrative or script

---

## Prerequisites

| Tool | Purpose | Install |
|------|---------|---------|
| Node.js + npm | Required to run `pptxgenjs` | `brew install node` |
| `pptxgenjs` | Generates `.pptx` files | `npm install -g pptxgenjs` |
| LibreOffice | QA step: converts `.pptx` to PDF | `brew install --cask libreoffice` |
| `poppler` | QA step: converts PDF to images for visual inspection | `brew install poppler` |
| `markitdown` | Optional: extracts text from existing `.pptx` for redesign | `pip install markitdown` |

---

## 15 Visual Styles

| # | Style Name |
|---|-----------|
| 1 | Modern Newspaper |
| 2 | Sharp Minimalism |
| 3 | Yellow × Black Editorial |
| 4 | Black × Orange Agency |
| 5 | Neo-Retro Dev Deck |
| 6 | Pink Street Style |
| 7 | Digital / Neo / Pop |
| 8 | Sports / Athletic |
| 9 | Studio / Premium Mockup |
| 10 | Tech / Art / Neon |
| 11 | Classic / Pop (Sculpture × Vaporwave) |
| 12 | Anti-Gravity / Living Artifact |
| 13 | Royal Blue × Red Watercolor |
| 14 | Seminar Minimal |
| 15 | Deformed Flat Persona |

---

## Design Rules

Every generated deck enforces these 10 universal rules regardless of style:

1. **1 slide = 1 message** — one clear idea per slide, no cramming
2. **Extreme size contrast** — minimum 5:1 ratio between largest and smallest text elements
3. **Asymmetry over center** — avoid centered layouts; use intentional imbalance
4. **No underlines under titles** — title hierarchy comes from size and weight, not decoration
5. **Vary layouts** — no two consecutive slides use the same layout type
6. **Every slide has a visual element** — no text-only slides
7. **Color is intentional** — accent color used sparingly, not everywhere
8. **White space is content** — breathing room is part of the design
9. **Numbers are hero elements** — stats and data get oversized, prominent treatment
10. **Icons over bullet points** — replace bullets with simple visual anchors where possible

---

## Adapting to Your Brand

To apply your own brand colors and fonts instead of the built-in styles, edit the style definitions in `SKILL.md`. Each style is defined as a block with:

```
colors: { primary, secondary, accent, background, text }
fonts: { heading, body }
layout_preferences: [...]
```

Add a new style block with your brand values and give it a name. Claude will include it in the style selection menu automatically.

---

## QA Process

After generating, the skill automatically:
1. Converts the `.pptx` to PDF using LibreOffice (`soffice --headless --convert-to pdf`)
2. Converts PDF pages to images using `pdftoppm`
3. Visually reviews each slide against the 10-item design checklist
4. Reports any violations and optionally regenerates the offending slides

If LibreOffice or `pdftoppm` is not installed, the QA step is skipped and a warning is shown.
