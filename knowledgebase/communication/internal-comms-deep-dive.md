---
name: internal-comms-deep-dive
description: 'Templates and structural rules for internal writing: 3P updates (Progress, Plans, Problems), company newsletters, and internal FAQs, all shaped to be read in under sixty seconds. Use when drafting a status update, a newsletter, or an FAQ for colleagues or leadership. For the workflow of gathering and pitching the content, use internal-comms.'
version: 1.1.0
category: utilities
triggers: [write a status update, progress plans problems, weekly update for leadership, internal newsletter, write an internal faq, update the team on this]
dependencies: [internal-comms]
inputs: [raw status or announcement material]
outputs: [a formatted internal update]
tags: [communication, management, internal-comms, patterns]
links: ['[[internal-comms]]', '[[doc-coauthoring]]']
confidence_score: 1.0
date: '2026-08-29'
task_ref: routing-repair-kb
---

# Internal Communication Patterns

## 🚀 3P Updates (Progress, Plans, Problems)
Succinct, data-driven updates for leadership and teammates. Intended to be read in <60 seconds.

### Formatting (Strict)
`[Emoji] [Team Name] (Dates Covered)`
- **Progress:** 1-3 sentences on what was shipped/achieved in the past week.
- **Plans:** 1-3 sentences on top-of-mind priorities for the next week.
- **Problems:** 1-3 sentences on blockers, bugs, or resource gaps.

---

## 📢 Company Newsletters
Summarizes the past week/month for the entire company.
- **Length:** ~20-25 bullet points.
- **Tone:** Use "we" tense; professional but approachable.
- **Content:** Focus on company-wide impact, leadership announcements, and major milestones. Link heavily to source docs and Slack announcements.

---

## ❓ Internal FAQs
Summarizes and answers common points of confusion across the company.
- **Source:** Look for Slack messages with high reaction counts or repetitive questions in threads.
- **Format:**
  - *Question:* [1 sentence]
  - *Answer:* [1-2 sentences with links to authoritative sources].

---

## 📝 General Internal Comms
For messages that don't fit the above formats.
- **Principles:** Active voice, most important info first, clear call-to-action (CTA).
- **Workflow:** Clarify audience, purpose, and tone (formal/casual) before drafting.
