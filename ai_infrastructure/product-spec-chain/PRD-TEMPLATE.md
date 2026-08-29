# PRD Template

Load during Phase 1. Emit exactly these five headings, in this order, as
`product-requirements.md`.

---

## 1. Elevator Pitch

**Standard:** A single punchy paragraph, max 3 sentences. It must name the core
value proposition, the key mechanism (LLM-powered feature, real-time data,
whatever the actual leverage is), and the primary benefit to the target user.

**Fails the bar:** "A platform for managing tasks efficiently."
**Passes:** "Levercast turns a single voice note into platform-native posts for
LinkedIn and Twitter. You dictate once; an LLM rewrites it per platform and
shows both previews side by side. Solo founders stop losing ideas to the gap
between having a thought and finding time to write it up."

## 2. Who is this App For

**Standard:** A short bulleted list of specific personas or industries. Be
concrete — "Small Business Owners", not "People". If there is a secondary
audience, mark it as secondary; don't let it dilute the primary.

## 3. Functional Requirements — What does it do

**Standard:** A detailed bulleted list of mandatory features, grouped into
logical categories (e.g. Content Input, Processing, Publishing, Management).

Include non-functional requirements that shape the build:
- Authentication model (OAuth 2.0? email/password? SSO?)
- Persistence expectations (what survives a session, for how long)
- Third-party integrations and which are load-bearing vs. nice-to-have
- Extensibility goals — what is expected to be added later

**This is the section most often under-specified.** If the user has not said
how people log in, ask before generating.

## 4. User Stories — How will the user interact

**Standard:** Goal-oriented stories covering the entire core workflow, in the
format:

> As a [persona], I want to [action] so that [benefit].

Cover the unhappy paths too — what happens on failure, on empty state, on first
run. A story set that only describes success produces a build with no error
handling.

## 5. User Interface — How will the app look

**Standard:** A concise bulleted description of key screens and visual
components. Focus on the decisions that constrain implementation:
- Layout structure (side-by-side preview, single column, dashboard grid)
- The prominent element on each screen
- Responsive targets (which breakpoints actually matter)
- Initial implementation scope vs. future design plans

Keep this high-level — the detailed treatment is Phase 2's job.

---

## Deferred Decisions

Close the document with an explicit list of anything the user chose not to
decide yet. Each line: the decision, and the point in the build by which it
must be made.
