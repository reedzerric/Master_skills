---
name: auth-ux-patterns
description: Design the presentation layer of authentication — form styling, validation states, error copy that tells the user what actually went wrong, and the filter/sort action-bar pattern for content listings. Use when login errors are unhelpful or unstyled, when auth forms look inconsistent across pages, or when building a listing page's control bar. For the server-side security work behind these forms, use django-auth-hardening instead.
version: 1.0.0
category: core
triggers: [login errors, form styling, validation states, auth ux, registration form, error messages, action bar, filter drawer, sort controls]
dependencies: [css-elite, frontend-design]
inputs: [existing auth templates, a design token set or brand palette]
outputs: [a form CSS layer, error message copy, styled validation states]
tags: [frontend, ux, forms, auth, css, error-handling]
links: ["[[django-auth-hardening]]", "[[css-elite]]", "[[frontend-design]]"]
confidence_score: 0.9
date: 2026-08-15
task_ref: skill-consolidation
---

# Auth UX Patterns

Make authentication forms legible, consistent, and honest about failure. It does
ONE thing: the presentation layer for auth and listing controls. It does not
harden sessions, rate-limit logins, or wire password reset (that is
`[[django-auth-hardening]]`).

## Operating Posture

You are a design engineer whose measure of success is a support-ticket count.
Most auth frustration is not a security failure — it is a user who cannot tell
whether they mistyped a password, are locked out, or have no account at all.
Every error state is a chance to answer that question or to fail to.

## Hard Rules

1. **Never reveal whether an account exists.** "No user with that email" is a
   user-enumeration vulnerability. Use one message for both wrong-email and
   wrong-password.
2. **Distinguish lockout from bad credentials.** These are different problems
   with different user actions. Collapsing them is the single most common cause
   of auth support tickets.
3. **Every input needs five states**: default, focus, filled, error, disabled.
   A form with only default and error is unfinished.
4. **Error text goes next to the field it concerns**, not only in a banner at
   the top. Form-level errors get the banner; field-level errors do not.
5. **Never use color alone to signal an error.** Pair it with an icon or text —
   red-only fails for colorblind users and in high-contrast mode.
6. **Centralize form CSS.** Inline styles across templates are how auth pages
   drift apart. One stylesheet, reused.

## Workflow

### Phase 1 — Inventory the states

List every state each auth screen can be in. For login alone:
empty, filled, submitting, invalid credentials, account locked, account
inactive, session expired, redirected-from-protected-page, and just-registered.

**Completion criterion:** a written list, with the copy for each state drafted
before any CSS is written.

### Phase 2 — Write the error copy

Each message answers: what happened, and what should I do now.

| State | Copy |
| :--- | :--- |
| Invalid credentials | "That email and password don't match. Check for typos, or reset your password." |
| Account locked | "Too many failed attempts. Try again in 1 hour, or reset your password to unlock now." |
| Inactive account | "This account hasn't been activated. Check your email for the activation link." |
| Session expired | "You were signed out for security. Sign in to continue where you left off." |
| Redirected from protected page | "Sign in to view that page." |

Never: "An error occurred." Never: "Invalid input."

**Completion criterion:** no message in the set is generic, and none reveals
whether an account exists.

### Phase 3 — Build the form layer

One stylesheet covering the whole auth surface. Use logical properties and
custom properties so the layer themes cleanly.

```css
:root {
  --field-bg: #ffffff;
  --field-border: #d4d4d8;
  --field-border-focus: #b8860b;
  --field-border-error: #d32f2f;
  --field-text: #18181b;
  --field-radius: 6px;
  --error-text: #b3261e;
}

@media (prefers-color-scheme: dark) {
  :root {
    --field-bg: #2d2d2d;
    --field-border: #3f3f46;
    --field-text: #eeeeee;
    --error-text: #ff8a80;
  }
}

.auth-form { display: grid; gap: 1.25rem; max-inline-size: 26rem; }

.auth-field { display: grid; gap: 0.375rem; }

.auth-field label { font-weight: 600; font-size: 0.875rem; }

.auth-field input {
  padding-block: 0.625rem;
  padding-inline: 0.75rem;
  background: var(--field-bg);
  color: var(--field-text);
  border: 1px solid var(--field-border);
  border-radius: var(--field-radius);
  transition: border-color 150ms ease-out, box-shadow 150ms ease-out;
}

.auth-field input:focus-visible {
  outline: none;
  border-color: var(--field-border-focus);
  box-shadow: 0 0 0 3px color-mix(in srgb, var(--field-border-focus) 25%, transparent);
}

.auth-field[data-invalid] input { border-color: var(--field-border-error); }

.auth-field .field-error {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  font-size: 0.8125rem;
  color: var(--error-text);
}

.auth-form__banner {
  padding: 0.75rem 1rem;
  border-inline-start: 3px solid var(--field-border-error);
  background: color-mix(in srgb, var(--field-border-error) 8%, transparent);
  border-radius: var(--field-radius);
}

@media (prefers-reduced-motion: reduce) {
  .auth-field input { transition: none; }
}
```

**Completion criterion:** login, register, profile, and password-reset all
render from this one stylesheet with no inline styles remaining.

### Phase 4 — Wire accessibility

- `aria-invalid="true"` on the input when its field is in error
- `aria-describedby` pointing the input at its error element's `id`
- the form-level banner in a `role="alert"` region so it is announced
- focus moves to the first invalid field on submit failure

**Completion criterion:** a screen reader announces the specific failure without
the user hunting for it.

### Phase 5 — Action bar (listing pages)

The same discipline applies to content listings. A left-justified horizontal bar
above the content, holding filter and sort controls that share one visual
treatment:

```html
<div class="action-bar">
  <div class="action-bar__controls">
    <button type="button" class="filter-trigger" aria-expanded="false"
            aria-controls="filter-drawer">
      <svg aria-hidden="true"><!-- sliders icon --></svg>
      Filters
    </button>

    <form method="get" class="sort-form">
      <label for="sort" class="visually-hidden">Sort by</label>
      <select id="sort" name="sort" onchange="this.form.submit()">
        <option value="newest">Newest</option>
        <option value="price_asc">Price: low to high</option>
        <option value="price_desc">Price: high to low</option>
      </select>
    </form>
  </div>
</div>
```

Filters open a drawer rather than expanding inline — inline expansion pushes the
content the user is trying to filter off-screen.

**Completion criterion:** filter and sort controls have identical height,
border-radius, and typographic treatment; the drawer traps focus while open and
restores it on close.

## Known Quirks & Edge Cases

- **The lockout message leaks timing.** "Try again in 1 hour" tells an attacker
  the lockout window. That is an acceptable trade — the user needs it more than
  the attacker gains from it — but make the decision knowingly.
- **`onchange="this.form.submit()"` breaks keyboard users.** Arrowing through a
  native select fires `change` per option in some browsers, submitting
  prematurely. Prefer an explicit Apply button, or listen for `blur`.
- **Autofilled inputs ignore your background color** in WebKit. Style
  `:-webkit-autofill` explicitly or the field will look broken in dark mode.
- **A banner alone loses screen-reader users.** If the only error indication is
  at the top of the form, someone tabbing through fields never encounters it —
  hence `aria-describedby` per field.
- **`color-mix()` needs a fallback** in older browsers; declare a flat color
  first and let `color-mix` override it.

## Related
- [[django-auth-hardening]] — the server-side behavior these forms surface
- [[css-elite]] — subgrid, container queries, and modern layout primitives
- [[frontend-design]] — avoiding generic AI aesthetics
