# UI Design Document Template

Load during Phase 2. Input is the finished PRD. Emit as `ux-design.md`.

Questions to resolve before generating:
- Desired feel in the user's own words (then translate it to concrete values)
- Platform targets — desktop-first, mobile-first, or genuinely both
- Existing brand assets, component library, or design system constraints
- Accessibility floor (WCAG AA is a sane default; ask if they need AAA)

---

## Layout Structure

Describe the overall skeleton: navigation placement, primary content region,
persistent chrome. State what is fixed and what scrolls. Name each distinct
screen implied by the PRD's user stories and describe its arrangement.

## Core Components

Enumerate reusable components — inputs, cards, modals, tables, empty states.
For each: what it contains, when it appears, and what its states are (default,
hover, loading, error, empty, disabled). Missing states are missing UI.

## Interaction Patterns

How things respond. Cover:
- Navigation model (routing, tabs, drawers)
- Feedback on action (optimistic, spinner, toast)
- Destructive-action confirmation
- Keyboard affordances for anything used repeatedly

Motion belongs here: entrances use `ease-out`, never `ease-in`; UI transitions
stay under 300ms; animate `transform` and `opacity` only; honor
`prefers-reduced-motion`.

## Visual Design Elements & Color Scheme

**Concrete values, not adjectives.** "Modern and clean" is not a spec.

Specify: background colors, surface colors, primary text, secondary text,
accent, and semantic colors (success, warning, danger) — as hex values. State
whether there is a dark mode and give both sets if so.

Avoid generic AI aesthetics: no purple-gradient-on-white, no default system
font stack, no centered-everything layout.

## Typography

Font families (display and body), the size scale, weights in use, and line
heights. Body copy at 1.5–1.6 line height; headings tighter, around 1.2.

## Accessibility

Contrast ratios met, focus-visible treatment, keyboard traversal order, screen
reader landmarks, and how error messages are announced. State the standard
being targeted.

---

## Open Design Questions

List what still needs a decision and who makes it.
