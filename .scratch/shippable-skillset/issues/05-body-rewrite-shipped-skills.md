# 05 — Rewrite the shipped skills' bodies to the agreed structure

Type: grilling
Status: open
Blocked by: 04, 09

## Question

This carries destination B. It was charted as a pure execution ticket, but 01's
resolution gave it a decision to make first, so it is now a grilling ticket.

**The scope inverted.** Charting settled "body conformance covers what ships",
chosen specifically to keep B small. 01 then settled "everything ships". Those
two together mean B covers all 54 legacy-template files — the opposite of the
intent. Something has to give:

- **Rewrite all 54.** Honest to the standard, and the corpus ends internally
  consistent. It is also the single largest chunk of work on this map, and most
  of it lands on skills whose value is unproven — exactly the skills 01 declined
  to make claims about.
- **Follow `battle_tested` as it accretes** (ticket 09). A skill earns a
  hand-written body when it earns the flag. Keeps effort proportional to
  demonstrated value and spreads it over time. Costs a corpus that is
  structurally mixed for months, which is the trap 03 is trying to avoid on the
  directory side.
- **Rewrite by shape, cheapest first.** The 54 are not equal: Reference skills
  need little more than section renaming once 04 defines their contract, while
  Procedure skills need real workflow authoring. Doing all the Reference ones
  mechanically and letting Procedure follow `battle_tested` splits the
  difference.

Resolve the scope question, then execute. Batch as the routing repair was
batched: smallest directory first, both gates green after each, one commit per
batch, never starting a batch on a red gate.

Per batch, record: files touched, shape classified per file, and gate output
verbatim.

Batch it the way the routing repair was batched: smallest directory first, gates
green after each, one commit per batch. Do not start a batch on a red gate.

Per batch, record: files touched, shape classified per file, and gate output
verbatim.

## Comments
