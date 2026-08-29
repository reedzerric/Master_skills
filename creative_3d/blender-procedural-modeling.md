---
name: blender-procedural-modeling
description: Build parametric 3D models in Blender with the bpy API — primitive-plus-boolean construction, named-constant dimensioning, sliding-fit tolerances for 3D printing, and repeatable script-driven geometry. Use when scripting Blender, generating printable parts from parameters, cutting grooves or joints with boolean modifiers, or when a model needs to be regenerated at different dimensions. For 2D generative art, use algorithmic-art.
version: 1.0.0
category: creative_3d
triggers: [blender, bpy, procedural modeling, boolean modifier, 3d print, parametric model, dovetail, tolerance, mesh generation, python 3d]
dependencies: [python-elite]
inputs: [a set of dimension parameters, a target print process and material]
outputs: [a Blender scene, an exported mesh, a parameterized generator script]
tags: [creative_3d, blender, bpy, procedural, 3d-printing, parametric]
links: ["[[python-elite]]", "[[algorithmic-art]]"]
confidence_score: 0.85
date: 2026-08-15
task_ref: skill-consolidation
---

# Blender Procedural Modeling

Generate printable 3D geometry from parameters rather than from mouse clicks. It
does ONE thing: script parametric solids with `bpy`. It does not do 2D
generative art (that is `[[algorithmic-art]]`), rendering, or animation.

## Operating Posture

You are a CAD engineer using Blender as a solid modeler, not an artist sculpting.
Every dimension is a named constant at the top of the script; every feature is
cut, not modeled. The measure of success is that changing one constant and
re-running produces a correct model at the new size — including the joints.

## Hard Rules

1. **Every dimension is a named constant.** A literal number inside a
   `dimensions` assignment is a bug waiting for the first resize.
2. **Clear the scene before building.** A script that appends to whatever was
   already open is not reproducible.
3. **Apply transforms before booleans.** An unapplied scale silently corrupts
   boolean results — Blender computes against object-space geometry.
4. **Cutters overshoot the surface they cut.** A cutter that ends exactly on the
   face produces coplanar geometry and a non-manifold result. Add clearance
   (typically +0.5 units) past every intended exit.
5. **Delete cutters after applying.** Leaving them in the scene exports them.
6. **Tolerance is a parameter, not a constant of nature.** Sliding fits need a
   gap sized to the printer and material, and it must be tunable without editing
   geometry code.

## Workflow

### Phase 1 — Parameterize

Every dimension at the top, grouped by what it describes. Comment the ones whose
value came from a physical constraint.

```python
import math

import bpy

# --- Body ---
CAR_L = 7.5           # length, sized to fit a 10x10 in build plate
CAR_W = 3.5
CAR_H = 3.0
WALL_THICKNESS = 0.2  # min printable wall at 0.4mm nozzle, 2 perimeters

# --- Sliding lid mechanism ---
SLIDE_TOLERANCE = 0.015  # per-side gap; tune per printer/material
GROOVE_DEPTH = 0.08
GROOVE_HEIGHT = 0.15     # narrowest point of the dovetail
GROOVE_Z_OFFSET = 0.1    # down from the top of the wall
```

**Completion criterion:** no numeric literal appears below the constant block
except where derived arithmetically from one.

### Phase 2 — Reset the scene and set units

```python
scene = bpy.context.scene
scene.unit_settings.system = "IMPERIAL"
scene.unit_settings.length_unit = "INCHES"

bpy.ops.object.select_all(action="DESELECT")
bpy.ops.object.select_by_type(type="MESH")
bpy.ops.object.delete()
```

Set the unit system explicitly — the default is metric, and a script written
against inches that runs under metric produces a model at the wrong scale with
no error.

**Completion criterion:** running the script twice produces identical scenes.

### Phase 3 — Build the primary solid

Create a primitive, set `dimensions`, position it, then **apply the scale**.

```python
bpy.ops.mesh.primitive_cube_add(size=1)
body = bpy.context.active_object
body.name = "Body"
body.dimensions = (CAR_L, CAR_W, CAR_H)
body.location = (0, 0, CAR_H / 2)
bpy.ops.object.transform_apply(scale=True)
```

`primitive_cube_add(size=1)` then setting `dimensions` is the reliable pattern —
it sets the scale factor, which is why applying it matters before any boolean.

**Completion criterion:** the object's scale reads (1, 1, 1) in the transform
panel.

### Phase 4 — Cut features with booleans

The core pattern: build a cutter, apply a DIFFERENCE modifier, remove the cutter.

```python
def cut(target, cutter, name: str) -> None:
    """Boolean-difference `cutter` out of `target`, then delete the cutter."""
    bpy.context.view_layer.objects.active = target
    mod = target.modifiers.new(type="BOOLEAN", name=name)
    mod.object = cutter
    mod.operation = "DIFFERENCE"
    bpy.ops.object.modifier_apply(modifier=name)
    bpy.data.objects.remove(cutter, do_unlink=True)
```

Hollowing — note the `+ 1.0` overshoot so the cutter clears the top face:

```python
bpy.ops.mesh.primitive_cube_add(size=1)
void = bpy.context.active_object

inner_l = CAR_L - (WALL_THICKNESS * 2)
inner_w = CAR_W - (WALL_THICKNESS * 2)
inner_h = CAR_H - WALL_THICKNESS          # leaves a solid floor

void.dimensions = (inner_l, inner_w, inner_h + 1.0)
void.location = (0, 0, WALL_THICKNESS + (inner_h + 1.0) / 2)
cut(body, void, "Hollow")
```

**Completion criterion:** the result is manifold — no interior faces, no
zero-thickness walls.

### Phase 5 — Cut joints with a rotated-profile cutter

A dovetail groove is a square cutter rotated 45° to present a diamond profile.
The diagonal relationship is where the arithmetic goes wrong most often: a
square of side `s` has diagonal `s × √2`, so to get a groove of a given height
the cutter must be sized by that factor.

```python
def dovetail_cutter(is_left: bool):
    bpy.ops.mesh.primitive_cube_add(size=1)
    cutter = bpy.context.active_object

    # Run from past the rear wall to short of the front wall (blind slot)
    rear_x = -(CAR_L / 2) - 0.5           # 0.5 overshoot clears the rear wall
    front_x = (CAR_L / 2) - WALL_THICKNESS
    cut_len = front_x - rear_x

    cutter_size = GROOVE_HEIGHT * math.sqrt(2)   # square -> diamond diagonal
    cutter.dimensions = (cut_len, cutter_size, cutter_size)
    cutter.rotation_euler = (math.radians(45), 0, 0)

    cutter.location = (
        (rear_x + front_x) / 2,
        ((CAR_W / 2) - WALL_THICKNESS) * (1 if is_left else -1),
        CAR_H - GROOVE_Z_OFFSET - (GROOVE_HEIGHT / 2),
    )
    return cutter
```

Join both cutters into one object before applying, so the groove is a single
boolean rather than two:

```python
left, right = dovetail_cutter(True), dovetail_cutter(False)
left.select_set(True)
right.select_set(True)
bpy.context.view_layer.objects.active = left
bpy.ops.object.join()
cut(body, left, "Dovetail")
```

**Completion criterion:** the slot runs through the rear wall and stops before
the front, and both sides are symmetric.

### Phase 6 — Model the mating part with tolerance

The sliding part is the groove profile minus the tolerance, on every contacting
face — not just one. Apply `SLIDE_TOLERANCE` per side, so a slot and rail that
share a nominal dimension differ by `2 × SLIDE_TOLERANCE` in total.

**Completion criterion:** printing both parts at the current tolerance produces a
fit that slides without force and without slop. If it does not, change only
`SLIDE_TOLERANCE` and reprint.

### Phase 7 — Export

Export STL or 3MF. Verify manifold-ness in the slicer before printing — Blender
will happily produce geometry that no slicer can handle.

**Completion criterion:** the slicer reports zero errors and the preview shows
the intended walls.

## Known Quirks & Edge Cases

- **`bpy.ops` acts on the active object and current selection**, which are
  global state. Set `bpy.context.view_layer.objects.active` explicitly before
  every operator call; do not assume the last-created object is still active.
- **Unapplied scale silently breaks booleans.** This is the single most common
  cause of a boolean that "does nothing" or produces garbage.
- **Coplanar faces produce non-manifold results.** Any cutter face that lands
  exactly on a target face is a bug. Overshoot always.
- **The 45° diamond needs `√2`, not `2`.** Sizing the cutter by `GROOVE_HEIGHT`
  directly yields a groove ~29% too shallow.
- **`bpy.data.objects.remove(obj, do_unlink=True)` is required** — removing
  without unlinking leaves the mesh datablock, and the next run's cleanup will
  not catch it.
- **Tolerance does not transfer between printers or materials.** PETG shrinks
  differently from PLA; a resin print needs a different gap again. Treat a
  working tolerance as calibrated to one setup.
- **Imperial units in Blender are display-only.** Internally everything is
  metres. Scripted numbers are interpreted in the scene's unit scale — verify an
  exported dimension against the slicer once before trusting a batch.

## Related
- [[python-elite]] — the `uv`/`ruff` toolchain for the generator script
- [[algorithmic-art]] — the 2D generative counterpart
