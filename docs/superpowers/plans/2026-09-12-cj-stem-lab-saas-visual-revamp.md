# CJ STEM Lab SaaS Visual Revamp Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reposition CJ STEM Lab as a balanced teacher- and district-facing Grades 6-8 curriculum platform while keeping the current GitHub Pages static architecture and existing resource catalog.

**Architecture:** Preserve the existing plain HTML/CSS/JavaScript site. Add four public product-positioning pages plus a static Teacher Hub preview, replace the homepage hierarchy, extend the shared visual system in `brand.css`, and use `script.js` to normalize legacy-page navigation so older Build/Code/Create/Student pages remain usable without hand-editing every page immediately.

**Tech Stack:** HTML5, CSS3, vanilla JavaScript, Python `unittest`, GitHub Pages.

**Spec:** `docs/superpowers/specs/2026-09-12-cj-stem-lab-saas-visual-revamp-design.md`

## Global Constraints

- Keep plain HTML, CSS, and JavaScript.
- Keep GitHub Pages compatibility.
- No framework migration.
- No external database, CMS, authentication provider, payment provider, analytics SDK, or student-data collection.
- `teacher-hub.html` is a static preview and must say so explicitly.
- Retain the existing `resources.html`, `products.js`, and product-detail pages.
- Use accurate standards language: `mapped to` / `designed around`; do not claim formal CSTA validation.
- Future student/district capabilities must be visibly described as roadmap items, not current functionality.
- Preserve keyboard navigation, skip links, semantic headings, responsive behavior, reduced-motion handling, and visible focus treatment.

---

### Task 1: Update regression tests for the new product architecture

**Files:**
- Modify: `tests/test_static_site.py`

**Interfaces:**
- Consumes: static HTML/CSS/JS files in repository root.
- Produces: regression checks that define the new required pages, global navigation, homepage hierarchy, Teacher Hub preview labeling, and retention of the resource catalog.

- [ ] **Step 1: Replace the old homepage/shop-first architecture assertions with new failing assertions**

Add `curriculum.html`, `teachers.html`, `schools.html`, `pilot.html`, and `teacher-hub.html` to the required page set. Assert the homepage contains, in order, `home-hero`, `implementation-gap`, `course-pathways`, `teacher-system`, `learning-modes`, `district-readiness`, `pilot-preview`, `founder-preview`, `resource-preview`, and `home-cta`.

Assert the homepage contains links to `curriculum.html` and `pilot.html`, does not contain `data-product-grid="featured"`, and contains a Teacher Hub mockup panel.

Assert every primary public page contains nav destinations for `curriculum.html`, `teachers.html`, `schools.html`, `pilot.html`, `resources.html`, `about.html`, and `teacher-hub.html`.

Assert `teacher-hub.html` contains `Preview` or `Concept`, and does not contain a password input.

Assert the resource catalog still contains `data-product-grid="shop"`.

- [ ] **Step 2: Run the regression test and verify it fails**

Run: `python -m unittest tests/test_static_site.py`

Expected: FAIL because the new public pages and homepage structure do not yet exist.

- [ ] **Step 3: Commit the test contract**

Commit message: `test: define SaaS visual site architecture`

---

### Task 2: Build the new homepage and public navigation

**Files:**
- Modify: `index.html`
- Modify: `script.js`

**Interfaces:**
- Consumes: shared `style.css`, `brand.css` and existing responsive nav-toggle behavior.
- Produces: new homepage section IDs and a standard primary navigation model that legacy pages can be normalized into.

- [ ] **Step 1: Replace homepage navigation and hero**

Use primary nav labels/destinations:

`Home`, `Curriculum`, `For Teachers`, `Schools & Districts`, `Pilot Program`, `Resources`, `About`, `Sign In`.

Hero copy must identify CJ STEM Lab as a Grades 6-8 curriculum platform, use `Explore Curriculum` as the primary CTA, and `Join the NJ Pilot` as the secondary CTA.

- [ ] **Step 2: Replace shop-first homepage content with the approved product story**

Add the section sequence required by Task 1. Include three course cards, six teacher-system deliverables, Build/Code/Create as learning modes, a district-readiness block, planned pilot block, founder block, and a small resources teaser near the bottom.

- [ ] **Step 3: Update `normalizeGlobalChrome()` in `script.js`**

Change legacy navigation normalization so older pages receive the new top-level destinations and `Resources` label instead of `Shop & Resources`. Keep current menu-toggle, reveal, resource filtering, purchase-link, and year behaviors intact.

- [ ] **Step 4: Commit homepage/navigation changes**

Commit message: `feat: reposition homepage for curriculum platform`

---

### Task 3: Add the Curriculum and For Teachers public pages

**Files:**
- Create: `curriculum.html`
- Create: `teachers.html`

**Interfaces:**
- Consumes: global header/footer patterns, new navigation, shared curriculum card classes from `brand.css`.
- Produces: public course catalog and teacher-value pages linked from the homepage/nav.

- [ ] **Step 1: Create `curriculum.html`**

Include the three proposal-backed course pathways and representative unit sequences. Add a common instructional model section: explicit instruction -> guided practice -> application -> testing/revision -> explanation/reflection. Include New Jersey standards language and an explicit note that national mappings are informational until external validation.

- [ ] **Step 2: Create `teachers.html`**

Show the complete lesson package: objective/standards, vocabulary, bell ringer, direct instruction, guided practice, application, checks for understanding, closure, extension, slides, student materials, assessment/rubric, answer materials, and differentiation. Show schedule models and teacher support for varied CS backgrounds. Link to `teacher-hub.html` as a preview.

- [ ] **Step 3: Commit curriculum/teacher pages**

Commit message: `feat: add curriculum and teacher value pages`

---

### Task 4: Add Schools & Districts and Pilot Program pages

**Files:**
- Create: `schools.html`
- Create: `pilot.html`

**Interfaces:**
- Consumes: proposal language on implementation, accessibility, privacy posture, pilot design, and roadmap.
- Produces: decision-maker credibility and a planned-pilot recruitment surface.

- [ ] **Step 1: Create `schools.html`**

Include flexible implementation models, standards/evidence, device/material flexibility, accessibility-first posture, privacy-by-phase language, and a three-phase roadmap. Label Phase 2 and Phase 3 features as future roadmap capabilities.

- [ ] **Step 2: Create `pilot.html`**

Use `Founding Educator Pilot` and `Planned Pilot` language. State intended participant count (5-10 NJ teachers), duration (2-4 weeks), one polished unit, support cycle, feedback/evidence expectations, and low-risk technology posture. CTA should express interest/contact rather than claim active enrollment infrastructure.

- [ ] **Step 3: Commit school/pilot pages**

Commit message: `feat: add district and pilot program pages`

---

### Task 5: Build the static Teacher Hub concept

**Files:**
- Create: `teacher-hub.html`

**Interfaces:**
- Consumes: course names and product visual system.
- Produces: a clickable, static product-concept page for visual demonstrations; it must not collect credentials or student data.

- [ ] **Step 1: Create a visible demo banner**

Use copy such as `Teacher Hub Preview — visual concept only. Accounts and subscriptions are not active yet.`

- [ ] **Step 2: Build the dashboard shell**

Add course cards for Grade 6 STEM Foundations, Grade 7 Computer Literacy & Digital Systems, and Grade 8 Computer Science Foundations, plus visual sections for standards, recent resources, and quick filters.

- [ ] **Step 3: Add a representative unit/lesson panel**

Show unit metadata, essential question, learning targets, and lesson cards with labels for Teacher Guide, Slides, Student Notes, Activity, Exit Ticket, and Answer Key.

- [ ] **Step 4: Commit Teacher Hub preview**

Commit message: `feat: add static teacher hub preview`

---

### Task 6: Mature the shared brand system and demote commerce visually

**Files:**
- Modify: `brand.css`

**Interfaces:**
- Consumes: all new semantic class names used by Tasks 2-5 plus existing product-card styles.
- Produces: responsive SaaS/curriculum visual system while retaining the current product catalog styling.

- [ ] **Step 1: Add public-site SaaS components**

Add styles for `platform-hero`, `product-shell`, `browser-bar`, `course-card`, `deliverable-grid`, `learning-mode-card`, `standards-strip`, `roadmap`, `pilot-card`, and `trust-grid` patterns. Use deep navy anchors, warm-white surfaces, pastel accents, restrained shadows, and larger white-space rhythm.

- [ ] **Step 2: Add Teacher Hub preview components**

Add styles for `hub-shell`, `hub-sidebar`, `hub-main`, `hub-course-grid`, `hub-unit-panel`, `lesson-row`, `demo-banner`, and responsive collapse behavior.

- [ ] **Step 3: Preserve catalog styling and accessibility rules**

Do not remove existing product cards, filter, purchase-box, reduced-motion, or focus-visible rules.

- [ ] **Step 4: Commit visual-system changes**

Commit message: `style: add curriculum platform visual system`

---

### Task 7: Align legacy and commerce pages with the new positioning

**Files:**
- Modify: `resources.html`
- Modify: `about.html`
- Modify only if needed for hard-coded conflicts: `build-lab.html`, `code-lab.html`, `create-lab.html`, `student-zone.html`, `contact.html`, `products/back-to-school-stem.html`, `products/computer-science-stem-posters.html`

**Interfaces:**
- Consumes: `normalizeGlobalChrome()` for shared navigation.
- Produces: consistent brand language without removing working legacy content.

- [ ] **Step 1: Reframe `resources.html` as a secondary educator-resource catalog**

Keep filters and product cards. Change top-of-page copy to distinguish standalone classroom resources from the core curriculum platform. Keep marketplace purchase mounts unchanged.

- [ ] **Step 2: Reframe `about.html`**

Lead with the company mission and classroom-origin story. Keep founder credibility but remove any framing that makes the site primarily `by Ms. CJ` rather than a scalable platform.

- [ ] **Step 3: Confirm normalized legacy navigation**

Verify Build/Code/Create/Student/Contact and product pages receive the new top-level nav through `script.js` without broken relative paths. For product subdirectory pages, use their existing relative-path handling if present.

- [ ] **Step 4: Commit legacy alignment**

Commit message: `refactor: align legacy pages with platform positioning`

---

### Task 8: Verification and merge readiness

**Files:**
- Test: `tests/test_static_site.py`
- Review: all changed HTML/CSS/JS files

**Interfaces:**
- Consumes: complete feature branch.
- Produces: verified static-site revision ready for pull request/merge.

- [ ] **Step 1: Run the complete regression suite**

Run: `python -m unittest tests/test_static_site.py`

Expected: all tests PASS.

- [ ] **Step 2: Run lightweight HTML link/content checks**

Verify no `href=""` appears on primary pages, all new local nav destinations exist, no password input exists on `teacher-hub.html`, and the homepage does not mount a featured product grid.

- [ ] **Step 3: Inspect responsive CSS contracts**

Confirm `@media (max-width: 980px)`, `@media (max-width: 640px)`, `@media (prefers-reduced-motion: reduce)`, and `:focus-visible` remain in `brand.css`.

- [ ] **Step 4: Open a pull request to `main`**

PR title: `Reposition CJ STEM Lab as curriculum platform`

PR body should summarize the public-site architecture, static Teacher Hub preview, commerce demotion, proposal alignment, and verification results.
