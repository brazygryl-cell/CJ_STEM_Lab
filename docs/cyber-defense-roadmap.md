# Cyber Defense Lab — October–December 2026 product roadmap

## Product goal
CJ STEM Lab is an educator-built cybersecurity and AI literacy platform. Cyber Defense Lab is its first flagship interactive learning product. December 1 is the target for a substantially fleshed-out demonstration website, not a production district SaaS rollout.

## Current build (October 14)
- Dedicated development branch `feature/cyber-defense-lab`, leaving public `main` unchanged.
- `cyber-defense.html`: mission selection dashboard.
- Phishing Investigation: 4 fictional email scenarios, 3 decisions each, immediate evidence-based feedback, total score /4, review report, and device-local best score.
- Homepage links and messaging updated within development branch.
- Missions 02–04 are visibly labeled in development.

## October acceptance gates
### Oct 14–18
- [x] Create development branch.
- [x] Add Cyber Defense Lab landing/dashboard and first interactive mission.
- [x] Link from homepage.
- [ ] Standardize navigation across student-facing legacy and updated curriculum pages.
- [ ] Test site on phone and Chromebook; fix overflow, keyboard and screen reader barriers.
### Oct 19–25
- [ ] Expand phishing to 8+ authored scenarios, with replay randomization.
- [ ] Introduce clear objectives, vocabulary, teacher notes, and assessment rubric.
- [ ] Add Account Security mission with 3–5 defensive decisions.
- [ ] Automated smoke tests for scenario data and completion flow.
### Oct 26–31
- [ ] Finish Account Security, browser-local progress and accessible report.
- [ ] Link Student Zone to missions and provide activity context.
- [ ] Build teacher-facing printable facilitator guide.
- [ ] QA pass: desktop, iPhone, Chromebook, keyboard, reduced motion.

## November acceptance gates
- Nov 1–7: Digital Footprint and Incident Response fictional defensive missions, each with guidance and feedback.
- Nov 8–14: One playable AI Investigation Lab demonstration with explanation and scoring.
- Nov 15–21: Usable Teacher Hub library/search and at least one complete AI/cyber educator PD module.
- Nov 22–30: Unified navigation, polished curriculum/district pages, product walkthrough, accessibility/functional QA, all demo links checked.

## Architectural principles
- Remain compatible with GitHub Pages (HTML/CSS/vanilla JavaScript), avoid migration for now.
- Separate authored scenarios and business rules from UI as complexity grows.
- Do not collect real student names, credentials, or email; simulations must use fictional examples and reserved .example domains.
- `localStorage` progress is demo-only, is browser/device-specific, and is not a student account or district reporting system.
- Never simulate real phishing collection or offer executable malicious downloads.
- Label planned features honestly; no fake login or misleading progress metrics.
- Target keyboard accessibility, responsive layout, contrast, and reduced motion.
- Keep original Build/Code/Create resources as secondary pathways; do not discard existing assets.

## December 1 definition of done
1. Public-facing product positioning and consistent navigation.
2. Four playable, fully reviewed Cyber Defense missions.
3. One AI Investigation Lab experience.
4. Teacher Hub with functional browse/search and downloadable sample materials.
5. One cybersecurity teaching unit and one educator PD demonstration.
6. Clearly explained privacy and demo limitations; no pretend production login.
7. Device and accessibility regression checklist completed.

## Buyer-readiness after December
Request educator feedback, establish IP provenance and district-employment separation, document measured usage only when legitimate, prepare a recorded walkthrough and outreach pack, then start targeted business-development conversations in January 2027.
