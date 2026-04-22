# Design Agent v4.0 — Full-Stack Design Intelligence

**Date:** 2026-04-22
**Status:** Design (approved for implementation planning)
**Author:** Rilner + Claude (brainstorming session)
**Implementation approach:** Refactor + Extract (from v3.1)
**Target file:** `subagents/design-agent.md` in Marketing OS

---

## 1. Purpose

Replace the current `subagents/design-agent.md` (v3.1, 3.546 lines, marketing-content focused) with v4.0: a full-stack design intelligence agent covering marketing content, product design, design systems, and brand systems. Operate as a hybrid builder + orchestrator, supported by modular companions and executable templates.

Eliminate the gap where the current agent documents design systems but does not build them, and does not coordinate with the user's existing Figma MCP, shadcn, and frontend-design skills.

## 2. Context and Motivation

### 2.1 Current state (v3.1)

- Single monolithic file `subagents/design-agent.md` at 3.546 lines
- 28 sections covering marketing-content design deeply
- Touches atomic design, tokens, WCAG 2.2 — but shallow and not actionable
- Self-proclaimed "most advanced design agent on the planet" (marketing copy, not benchmarked)
- No awareness of or integration with the user's Figma MCP skills, shadcn, frontend-design
- No executable templates (everything is conceptual)
- No orchestration logic (agent never delegates)

### 2.2 User goal

User wants this agent to be genuinely best-in-class full-stack: marketing + product + design system + brand. Not a rebrand of the existing content — a meaningful capability upgrade.

### 2.3 Clarifying decisions taken in brainstorming

| Question | Decision |
|----------|----------|
| Scope | **B** — Full-stack (marketing + product + DS + brand) |
| Execution model | **D** — Hybrid: builder for lightweight artifacts + orchestrator for heavy work |
| File architecture | **B** — One agent + modular companions + templates |
| Ambition v1 | **B** — Comprehensive (~10 companions + ~8 templates), one extensive session |
| Implementation path | **Approach 2** — Refactor + extract from v3.1 (preserve value, avoid regressions) |

## 3. Architecture

### 3.1 File layout

```
subagents/
  design-agent.md                          # v4.0 — strategic brain + orchestrator + builder
  design-agent-v3.1-archive.md             # backup of current; keep until v4 validated

references/design/                         # 10 companions (domain depth)
  01-tokens-w3c-spec.md
  02-atomic-design-playbook.md
  03-ds-governance.md
  04-accessibility-wcag22.md
  05-motion-spec.md
  06-brand-system-blueprint.md
  07-figma-mcp-playbook.md
  08-shadcn-integration.md
  09-handoff-to-code.md
  10-orchestration-routes.md

templates/design/                          # 8 executable templates
  tokens.json.template
  theme.css.template
  component-spec.md.template
  ds-readme.md.template
  style-dictionary.config.js.template
  storybook-main.ts.template
  brand-guidelines.md.template
  design-review.md.template
```

Total: 1 agent + 10 companions + 8 templates = 19 new/refactored files.

### 3.2 Architectural principles

1. **Single entry point.** User always calls `@design-agent`. Companions are loaded by the agent when relevant, not directly by the user.
2. **Builder for lightweight artifacts.** Agent generates tokens.json, theme.css, component specs, brand books, design reviews, AI prompts, social post direction — directly, without delegation.
3. **Orchestrator for heavy work.** For Figma design system creation, production React components, and similar specialist work, agent explicitly delegates to installed skills (figma MCP, shadcn, frontend-design).
4. **Companions are deep, agent is broad.** Agent stays under 2.500 lines covering strategy + decisions + routing + essentials. Companions go deep on single domains.
5. **No duplicated content.** Each concept lives in exactly one place (agent OR a specific companion).

## 4. Agent v4.0 Internal Structure

Target size: 1.800-2.500 lines.

```
1. Quando Acionar (expanded trigger conditions — marketing + product + DS + brand + handoff)
2. Mental Model: Como Este Agente Pensa (triagem de request → domain)
3. ORCHESTRATION ROUTES (decision tree: request → skill/tool; core new value)
4. BUILDER MODE (list of artifacts agent generates directly)
5. Design Principles — Condensed (Rams, Vignelli, Rand, Scher essentials; deep → companion 02)
6. Visual Perception — Essentials (13ms vs 250ms, Gestalt; condensed from v3.1)
7. Color + Typography + Composition — Essentials (deep → companions 06, 02)
8. AI Image Generation 2026 (preserved from v3.1 — GPT Image 1.5, MJ V7, FLUX.2, Ideogram 3.0, Recraft V3)
9. Design System — Overview + Build Flow (deep → companions 01, 02, 03, 07, 08, 09)
10. Brand System — Overview + Build Flow (deep → companion 06)
11. Marketing Content Playbooks (social, thumbnails, carousels, VSL, e-commerce, presentations)
12. Motion + Video Design — Essentials (deep → companion 05)
13. Accessibility — Essentials (deep → companion 04)
14. Quality Gate — Design Review Checklist (15 points; uses design-review template)
15. Integration with Marketing OS (how it collaborates with other subagents)
```

## 5. Companions Detail

### 5.1 `references/design/01-tokens-w3c-spec.md` (~1.200 lines)

W3C Design Tokens Community Group spec 2025.10. Three layers: core (raw values) → semantic (purpose) → component (context). All 13 token types (color, dimension, fontFamily, fontWeight, duration, cubicBezier, shadow, border, gradient, transition, typography, composite). `$value`, `$type`, `$description`, `$extensions` explained. Examples: light/dark theme, multi-brand, responsive tokens. Style Dictionary pipeline. Tokens Studio workflow. Validation and linting.

### 5.2 `references/design/02-atomic-design-playbook.md` (~900 lines)

Brad Frost's 6 levels (Tokens + Atoms + Molecules + Organisms + Templates + Pages). Decision criteria for when each level exists. Naming conventions per level. Variant systems (Figma variants + code). Composition patterns (slot, children, render props). Anti-patterns (over-abstraction, premature composition). 12 practical end-to-end examples.

### 5.3 `references/design/03-ds-governance.md` (~700 lines)

Semver for design systems. RFC process for new additions. Deprecation policy (sunset timeline, migration guides). Contribution model (core team + community). Design review rituals. Breaking changes: detection, communication, rollback. Metrics: adoption rate, consistency score, debt tracker. Roadmap and backlog templates.

### 5.4 `references/design/04-accessibility-wcag22.md` (~1.000 lines)

WCAG 2.2 AAA checklist per component (button, input, modal, table, form, nav). Contrast requirements (normal, large, UI components, non-text). Focus indicators (2.4.11 new in 2.2, 2.4.12, 2.4.13). Target size (2.5.8 — 24×24 minimum). Keyboard navigation patterns. Screen reader patterns (ARIA live regions, aria-describedby, aria-expanded). Cognitive a11y (readability, predictability). Testing: axe-core, Lighthouse, NVDA/JAWS, Voice Control. Common failures and fixes.

### 5.5 `references/design/05-motion-spec.md` (~600 lines)

Motion tokens (duration scale: 100/150/250/400/700ms). Easing library (ease-out for enter, ease-in for exit, custom cubic-bezier). Choreography: stagger, parallel, sequential. Reduced motion (prefers-reduced-motion). Motion grammar: what motion means (orientation, feedback, continuity). Component-level motion recipes. Lottie, Rive, Framer Motion, CSS transitions — when to use each.

### 5.6 `references/design/06-brand-system-blueprint.md` (~1.500 lines)

Complete brand book structure (30 sections). Logo system (primary, secondary, lockups, clear space, don'ts). Color (primary, secondary, semantic, tints/shades, accessibility). Typography (display, body, UI, hierarchy). Voice and tone matrix (context → tone). Vocabulary (on-brand/off-brand words). Photography direction (style, composition, mood boards). Illustration system. Icon system. Grid and layout (5 canvases: web, mobile, print, social, merch). Motion guidelines. Sonic brand (if applicable). Applications (stationery, signage, packaging, digital, merch, environmental). Brand architecture (masterbrand, endorsed, freestanding).

### 5.7 `references/design/07-figma-mcp-playbook.md` (~500 lines)

When to invoke `figma:figma-generate-library`, `figma:figma-use`, `figma:figma-generate-design`, `figma:figma-implement-design`, `figma:figma-code-connect`. Correct order: variables → styles → components → variants → libraries. Prompt patterns for Figma MCP (what works, what fails). Common gotchas and workarounds. Designer → dev handoff via Code Connect.

### 5.8 `references/design/08-shadcn-integration.md` (~400 lines)

When to use `vercel:shadcn`. Custom registries (building a private DS on top of shadcn). Theming (CSS variables + tokens). Composition patterns. Coexistence with a proprietary DS.

### 5.9 `references/design/09-handoff-to-code.md` (~700 lines)

Complete design-to-code pipeline. Tokens.json → Style Dictionary → CSS/iOS/Android/Flutter output. Figma Code Connect setup. Component documentation: Storybook + MDX. Change propagation: token change → automated PR → preview deploy. Review gates between design and dev.

### 5.10 `references/design/10-orchestration-routes.md` (~800 lines)

**Central document of the hybrid model.** Complete decision tree: request type → action. 40+ scenarios mapped with the correct skill/tool. Fallbacks when a skill is unavailable. Examples: user asks "build me a DS for the app" → agent asks 5 questions → delegates phases to the right skills. Integration patterns with other Marketing OS subagents.

**Total companion content:** ~8.300 lines.

## 6. Templates Detail

Templates are skeletons with placeholders. Builder mode fills them.

| File | Lines | Purpose |
|------|-------|---------|
| `tokens.json.template` | ~200 | W3C tokens skeleton (core, semantic, component layers) |
| `theme.css.template` | ~150 | CSS variables from tokens; light+dark; @layer organized |
| `component-spec.md.template` | ~300 | Purpose, anatomy, props API, variants, states, a11y, do/don't, examples, changelog |
| `ds-readme.md.template` | ~200 | DS README: intro, install, usage, contribution, links, changelog, badges |
| `style-dictionary.config.js.template` | ~150 | Multi-platform output config + custom transforms/formats |
| `storybook-main.ts.template` | ~100 | Storybook 8+ with a11y, controls, docs, viewport, themes addons |
| `brand-guidelines.md.template` | ~500 | 30-section brand book skeleton |
| `design-review.md.template` | ~150 | 15-point review checklist, severity matrix, PASS/CONCERNS/FAIL rubric |

**Total templates:** ~1.750 lines.

## 7. Extraction Plan (v3.1 → v4.0)

### 7.1 Preserved (moved/condensed, quality retained)

| v3.1 Section | Destination | Treatment |
|-------------|-------------|-----------|
| 2. Visual Perception | Agent §6 | Condense 30%; preserve frameworks |
| 3. Rams 10 Commandments | Agent §5 | Condense to list + essence |
| 4. Neurodesign | Agent §6 (merge) | Merge with §6; cut redundancy |
| 5. Color Theory | Agent §7 essentials + Companion 06 | Split: psychology→agent, full palettes→brand |
| 6. Typography | Agent §7 + Companion 06 | Split: principles→agent, scale→brand |
| 7. Composition | Agent §7 + Companion 02 | Split: essentials→agent, atomic→companion |
| 8. Design for Conversion | Agent §11 | Preserve as Marketing Playbook |
| 9. Visual Storytelling | Agent §11 | Preserve |
| 11. Motion | Agent §12 + Companion 05 | Split: essentials→agent, spec→companion |
| 13. Accessibility | Agent §13 + Companion 04 | Split: essentials→agent, WCAG AAA→companion |
| 14. Cultural Design | Companion 06 (localization section) | Move whole |
| 15. Platform Specs | Agent §11 | Preserve + update for April 2026 |
| 16. Brand System | Companion 06 (base) | Expand to ~1.500 lines |
| 17. AI Images | Agent §8 | **Preserve integral** (v3.1 is excellent here) |
| 18. Tools | Companions 07, 08, 09 | Split by tool |
| 22. Photography | Companion 06 (photography direction) | Move |
| 23. Print | Companion 06 (applications) | Move condensed |
| 25. Video Design | Agent §12 + §11 | Split motion/marketing |
| 26. Hybrid Posts System | Agent §11 | **Preserve integral** (system already strong) |
| 27. Niche Templates | Agent §11 + templates/ | Concept→agent, concrete→templates |
| 28. Workflows/Integration | Agent §15 | Expand with orchestration |

### 7.2 Reduced/Refactored

| v3.1 Section | Treatment |
|-------------|-----------|
| 10. 2026 Trends | Disperse — each trend into relevant companion (avoid concentrated bit rot) |
| 12. UX Design | Condense 60% — companion 02 covers atomic; agent keeps essentials |
| 19. Data Visualization | Condense to 1 page in agent §11 (low demand in Marketing OS) |
| 20. E-Commerce | Condense → agent §11 subsection |
| 21. Presentations | Condense → agent §11 subsection |
| 24. Metrics/Testing | Split → governance metrics (companion 03) + quality gate (agent §14) |

### 7.3 New (not in v3.1)

- Orchestration routes (agent §3 + companion 10) — core of hybrid model
- Builder mode spec (agent §4) — formalized artifact list
- Mental model / decision framework (agent §2)
- W3C Tokens deep (companion 01)
- Figma MCP playbook (companion 07)
- shadcn integration (companion 08)
- Handoff-to-code pipeline (companion 09)
- DS Governance deep (companion 03)
- 8 executable templates

### 7.4 Discarded

- Duplications between v3.1 sections (color/typography/brand overlap)
- Self-congratulatory marketing copy ("most advanced on the planet") — replaced by objective trigger conditions
- Date-stamped sections that would age poorly in 2 months

## 8. Definition of Done

1. All 19 files created (1 agent + 10 companions + 8 templates).
2. `design-agent.md` size 1.800-2.500 lines.
3. `design-agent-v3.1-archive.md` exists in `subagents/` as backup.
4. Structural gates pass (files exist, sizes respected, internal references resolve).
5. Content quality checklist passes (no placeholders, no prohibited words, accents consistent, no unsupported claims, no broken links).
6. 5/5 integration smoke tests pass:
   - "Create a DS for my B2B SaaS app" — agent asks 5 questions, delegates phases, produces tokens.json.
   - "Brand book for my personal brand" — agent fills brand-guidelines template.
   - "Instagram carousel about X" — agent produces visual spec + AI image prompt.
   - "Create Button component in Figma" — agent invokes `figma:figma-generate-library`.
   - "A11y audit this component" — agent uses companion 04, returns WCAG 2.2 report.
7. Skills referenced in orchestration routes exist in the user's environment.
8. Clone manifest checked/updated if design-agent is referenced there.
9. This spec committed to git.
10. Implementation plan generated via `superpowers:writing-plans`.
11. Final commit: `feat(design): design-agent v4.0 full-stack rebuild`.

## 9. Rollback Plan

If v4.0 breaks something critical:

```bash
mv subagents/design-agent.md subagents/design-agent-v4.0-broken.md
mv subagents/design-agent-v3.1-archive.md subagents/design-agent.md
```

Companions and templates can remain (they do not affect v3.1 behavior).

## 10. Out of Scope (v4.0)

- Executable Python scripts in `scripts/design/` — deferred to v4.1.
- Marketing OS-wide restructuring.
- Changes to other subagents.
- English translation (system remains in Portuguese).
- Custom design MCP server — deferred to v5+.
- Adobe/Sketch integration (stack is Figma-only officially).

## 11. Open Questions

None at spec time. All scope/architecture/ambition decisions resolved in brainstorming.

## 12. Next Step

Invoke `superpowers:writing-plans` to create a step-by-step implementation plan covering the extraction, authoring, and validation phases.
