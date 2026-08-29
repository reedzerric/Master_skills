---
name: diegetic-game-ui
description: Design and implement immersive, diegetic 2D game UI artifacts (antique parchment scrolls, fantasy maps, alchemical treaties, reward modals, stone tablets). Use when the user asks to design game modals, reward popups, map screens, parchment overlays, or when requesting 9-slice cartographic frames, deckle-edge styling, image generation prompts, or technical UI architecture for tactile game surfaces.
version: 1.0.0
category: game_design
triggers: [diegetic ui, parchment modal, map popup, deckle edge, scroll ui, fantasy ui, 9-slice map, game modal artifact]
dependencies: [frontend-design]
inputs: [modal requirements, game theme, reward structure]
outputs: [diegetic UI component, SVG filter setup, image prompts, 9-slice specs]
tags: [game-ui, diegetic, parchment, cartography, 9-slice, svg-filters, framer-motion]
links: ["[[frontend-design]]", "[[SKILL_STANDARD]]"]
---

# Diegetic Game UI & Cartographic Artifacts

This skill guides the design, prompt engineering, and technical implementation of physical, in-world (diegetic) UI elements — replacing generic floating web modals with tangible game artifacts (aged scrolls, treasure maps, enchanted treaties, and carved runestones).

---

## 1. Key Terminology Reference

When authoring prompts, UI specifications, or design documents, always use precise physical and cartographic terminology:

### Physical Paper & Edge Styles
- **Deckle Edge**: The rough, untrimmed, feathered edge of handmade paper or antique parchment.
- **Tattered / Frayed Parchment**: Edges worn, weathered, or torn from age and handling.
- **Burnt / Singed Edges**: Darkened, charred vellum margins with soot gradients.
- **Curled / Dog-Eared Corners**: Corners that roll inward or fold, typical of unrolled maps.
- **Worn Fold Creases**: Visible faint grid lines or cross creases from storage in quarters.

### Cartographic & Map Framing Styles
- **Cartographic Neatline**: The clean, thin outer boundary line that contains the map area.
- **Graduated / Barred Map Border**: Alternating dark-and-light segments indicating latitude/longitude scale ticks.
- **Nautical Chart Frame**: Inset compass roses, corner rosettes, rhumb lines, and coordinate marks.
- **Ornamental Filigree Corners**: Antique flourishes, brass corner brackets, or Renaissance cartouches.

---

## 2. Prompt Engineering Templates

### A. Image Generator Template (Midjourney, DALL-E, Stable Diffusion)
```text
2D Game UI pop-up window background, antique fantasy map aesthetic, worn deckle-edged parchment paper, torn and frayed ragged borders, subtle cartographic neatline with coordinate tick marks, aged vellum texture, unrolled scroll style with faint fold creases, clean center area for text, transparent alpha background (PNG), high resolution UI asset --no modern elements, flat UI, gradients, blur
```

### B. LLM Design Spec & GDD Prompt
```text
I am designing a 2D fantasy game UI popup for [feature name, e.g. Boon Choice / Map Expedition / Boss Spoils]. Describe the background as an antique cartographic scroll with authentic map edges. Specify deckle edges, frayed paper borders, a subtle graduated map neatline, and aged parchment textures, while ensuring the central area remains high-contrast and unobstructed for legible text and interactive sockets.
```

---

## 3. Technical UI Architecture

### 9-Slice (NinePatch) Compatibility
Irregular deckle edges and torn map paper cannot be uniformly stretched across dynamic resolutions without distorting paper grain:
1. **4 Fixed Corners**: Contain permanent wear, curled tips, and decorative brass/wood finials.
2. **4 Edge Rails (Top/Bottom/Left/Right)**: Low-frequency repeating texture or tileable deckle trim.
3. **1 Center Tile**: High-contrast neutral parchment fill that scales freely in X and Y.

### 4-Layer UI Composition Model
Always structure the rendered DOM/Canvas in distinct depth planes:
1. **Base Parchment Fill**: High-contrast, warm aged parchment (`#f5ebd6` to `#d6bc92`) ensuring text readability.
2. **Edge & Trim Layer**: Isolated SVG displacement filter / 9-slice mask for the ragged deckle boundary.
3. **Watermark / Geometry Layer**: Translucent alchemical circles or rhumb lines set to **5%–12% opacity** (`mix-blend-multiply`), never occluding text.
4. **Foreground Content Layer**: Vector-sharp typography (`#3b1e08`), vibrant artifact icons, tactile sockets, and wax-sealed buttons.

---

## 4. Frontend Code Implementation (React + SVG + Framer Motion)

### A. Non-Destructive Ragged Edge (SVG Displacement)
> **Crucial Rule**: Never apply `feDisplacementMap` to parent containers holding text. Apply displacement strictly to an absolute background layer so typography stays 100% vector-sharp.

```tsx
{/* 1. Define Displacement Filter */}
<svg className="absolute w-0 h-0 pointer-events-none" aria-hidden="true">
  <defs>
    <filter id="deckle-edge" x="-10%" y="-10%" width="120%" height="120%">
      <feTurbulence type="fractalNoise" baseFrequency="0.04" numOctaves="4" result="noise" />
      <feDisplacementMap in="SourceGraphic" in2="noise" scale="8" xChannelSelector="R" yChannelSelector="G" />
    </filter>
  </defs>
</svg>

{/* 2. Apply to Background Only */}
<div className="relative w-full max-w-lg p-8">
  <div
    style={{ filter: 'url(#deckle-edge)' }}
    className="absolute inset-0 bg-gradient-to-br from-[#f5ebd6] via-[#ebd7b5] to-[#d6bc92] border-2 border-[#8b5a2b]/40 shadow-2xl"
  />
  <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,transparent_40%,rgba(120,70,20,0.25)_80%,rgba(60,30,8,0.55)_100%)] mix-blend-multiply pointer-events-none" />
  
  {/* 3. Sharp Foreground Content */}
  <div className="relative z-10 text-center">
    <h2 className="font-serif font-black text-2xl text-[#3b1e08] uppercase tracking-widest italic">
      Arcane Treaty
    </h2>
  </div>
</div>
```

### B. Physical Unroll Entrance (Spring Physics)
```tsx
<motion.div
  initial={{ scaleX: 0.15, scaleY: 0.85, opacity: 0 }}
  animate={{ scaleX: 1, scaleY: 1, opacity: 1 }}
  exit={{ scaleX: 0.1, opacity: 0 }}
  transition={{ type: 'spring', stiffness: 280, damping: 26 }}
  className="origin-center"
>
  {/* Scroll Content */}
</motion.div>
```

### C. Tactile Wax Seal Button
```tsx
<motion.button
  whileHover={{ scale: 1.05 }}
  whileTap={{ scale: 0.95 }}
  className="px-7 py-2.5 bg-gradient-to-b from-[#a3281e] to-[#6e150d] text-[#f7eedf] font-serif font-black text-xs uppercase tracking-widest rounded-xl shadow-[0_4px_14px_rgba(110,21,13,0.5)] border-2 border-[#4a0a05] cursor-pointer"
>
  Claim Spoils
</motion.button>
```
