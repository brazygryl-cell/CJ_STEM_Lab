# CJ STEM Lab SaaS Visual Revamp Design

Date: 2026-09-12
Status: Approved for implementation
Repository: `brazygryl-cell/CJ_STEM_Lab`

## Goal

Reposition the current CJ STEM Lab GitHub Pages site from a personal teacher-resource hub into the public-facing website for the CJ STEM Lab curriculum and learning platform described in the September 2026 strategic proposal.

This phase is visual and structural only. It must remain plain HTML/CSS/JavaScript on GitHub Pages. It will not add authentication, billing, databases, student accounts, district integrations, or collection of personally identifiable information.

## Product Positioning

The website should feel balanced between classroom teachers and school/district decision-makers. Teachers should immediately recognize the preparation-time problem the product solves, while principals, supervisors, and district staff should see standards alignment, implementation flexibility, accessibility, and a credible phased product roadmap.

The primary message is that CJ STEM Lab provides complete, adaptable Grades 6-8 STEM, computer literacy, and computer science curriculum built for real classroom conditions.

The website should not present CJ STEM Lab primarily as a printable-resource shop. Direct digital products remain a secondary revenue and discovery channel.

## Primary Audiences

1. Grades 6-8 STEM, technology, computer literacy, and computer science teachers.
2. Principals, instructional supervisors, curriculum leaders, and district administrators.
3. Prospective New Jersey pilot educators and school partners.
4. Secondary audiences: families, community programs, and educators looking for standalone resources.

## Public Site Architecture

Primary navigation:

- Home
- Curriculum
- For Teachers
- Schools & Districts
- Pilot Program
- Resources
- About
- Sign In

`Sign In` links to a static Teacher Hub concept page. It must be visibly labeled as a preview/demo experience rather than a functioning account system.

Build Lab, Code Lab, and Create Lab remain part of the brand but no longer define the top-level website architecture. They become learning modes/pathways inside the curriculum and Teacher Hub experience:

- Build Lab: engineering, physical STEM, scientific investigation
- Code Lab: programming, computational thinking, web development
- Create Lab: design thinking, digital media, AI literacy, creative problem-solving

The existing standalone Build Lab, Code Lab, Create Lab, and Student Zone pages may remain available for backward compatibility but should use the new global navigation and should no longer dominate the homepage.

## Homepage Structure

1. Hero
   - Product-first brand identity: `CJ STEM Lab`
   - Headline direction: curriculum that helps teachers teach STEM and computer science without building the course from scratch
   - Supporting copy: Grades 6-8, classroom-tested, New Jersey-first, adaptable for real schedules
   - Primary CTA: Explore Curriculum
   - Secondary CTA: Join the NJ Pilot
   - Visual: a polished static mockup of the Teacher Hub, not a shop/product card

2. Implementation gap/problem section
   - Broad standards do not automatically become day-to-day curriculum
   - Emphasize planning burden, pacing, differentiation, assessments, and realistic classroom constraints

3. Three course pathways
   - Grade 6 STEM Foundations
   - Grade 7 Computer Literacy & Digital Systems
   - Grade 8 Computer Science Foundations
   - Each card shows representative units and implementation format

4. What teachers receive
   - Daily lesson plans
   - Instructional slides
   - Student materials
   - Assessments/rubrics/answer keys
   - Standards maps
   - Differentiation and schedule variants

5. Learning modes
   - Build Lab
   - Code Lab
   - Create Lab

6. For schools and districts
   - NJ standards mapping
   - flexible scheduling/implementation
   - Chromebook-friendly and low-cost alternatives
   - accessibility-first product direction
   - future district readiness without implying current district software exists

7. Pilot CTA
   - NJ Grades 6-8 educator focus
   - 2-4 week future pilot concept
   - application/interest CTA only; no claim that a pilot is actively running unless the page copy clearly says recruitment/planning stage

8. Founder credibility
   - built by a practicing STEM/computer science educator
   - classroom-tested perspective
   - professional, not personality-led

9. Secondary resources teaser
   - small section near the bottom
   - standalone printables and classroom resources
   - `Browse Resources` CTA

10. Final CTA
   - Explore Curriculum
   - Pilot Program

## Curriculum Page

The Curriculum page is the public catalog of the core Grades 6-8 pathways.

### Grade 6 STEM Foundations
Illustrative sequence:
- What Is STEM
- scientific questions and fair tests
- reliable evidence
- engineering design
- structures and forces
- water and environment
- technology and systems
- math in design
- integrated capstone

### Grade 7 Computer Literacy & Digital Systems
Illustrative sequence:
- computer systems
- files and cloud organization
- Internet and Web
- search and source evaluation
- productivity and collaboration
- data representation
- cybersecurity
- digital citizenship
- algorithms
- introductory web creation
- AI literacy

### Grade 8 Computer Science Foundations
Illustrative sequence:
- computational thinking
- HTML and CSS
- JavaScript interaction
- Python programming
- data and visualization
- networks and security
- human-centered design
- application development
- portfolio capstone

The page should also show the common instructional model: explicit instruction -> guided practice -> creation/investigation -> testing/revision -> explanation/reflection.

Standards language should say mapped to/designed around applicable New Jersey standards; it must not claim formal CSTA validation.

## For Teachers Page

Focus on practical classroom usability.

Sections:
- What is included in a complete lesson
- multiple pacing/schedule models
- differentiation and access
- assessment model
- teacher confidence/support for educators with varied CS backgrounds
- static Teacher Hub preview CTA

## Schools & Districts Page

Focus on adoption and implementation credibility.

Sections:
- implementation models: dedicated course, semester/quarter, rotation, enrichment, interdisciplinary
- standards and assessed evidence
- device/material flexibility
- accessibility posture: WCAG 2.1 AA as a design requirement
- privacy/security phased approach, explicitly noting this static phase does not collect student data
- future roadmap: teacher curriculum hub -> interactive student learning -> district system
- contact/pilot CTA

Do not present future rostering, analytics, SSO, or administrator controls as currently available.

## Pilot Program Page

This is a recruitment/readiness page, not a claim of an active completed pilot.

Present:
- intended participants: 5-10 NJ teachers across at least two contexts
- intended duration: 2-4 instructional weeks
- one complete Grade 6, 7, or 8 unit
- teacher orientation/support
- feedback and implementation evidence
- low-risk technology model that avoids unnecessary student PII
- interest CTA

Use language such as `Founding Educator Pilot`, `Pilot Interest`, `Planned Pilot`, or `Join the Pilot Interest List` until actual pilot recruitment is underway.

## Teacher Hub Preview

Create a static `teacher-hub.html` page that looks like an authenticated product while clearly labeled `Preview` or `Concept`.

Dashboard contents:
- welcome/header area
- course cards for Grades 6, 7, and 8
- progress/continue-learning visual treatments that are nonfunctional/demo-only
- recent resources
- standards/search/filter UI treatments

Course preview panels should demonstrate the intended flow:
- course overview
- units
- standards
- assessments
- resources

A unit preview should show:
- duration
- grade/course
- essential question
- learning targets
- lesson cards
- teacher guide/slides/student notes/activity/exit ticket/answer key labels

No login form should collect credentials. `Sign In` can route directly to the preview with a visible demo notice.

## Resources Strategy

Keep the current Shop & Resources catalog and product detail pages, but demote them from the homepage and main positioning.

Rename top-level language from `Shop & Resources` to `Resources` where appropriate. The Resources page may retain purchase links and catalog filtering.

Homepage product cards should be replaced by a small secondary resources teaser; products remain discoverable on `resources.html`.

## Brand Direction

Retain the recognizable Pastel Pop/CJ STEM Lab identity, but mature the buyer-facing presentation.

Use:
- deep navy as the professional anchor
- warm white/white surfaces
- pastel teal, blue, coral, yellow, green, and limited purple accents
- clean cards and spacing
- rounded details without making the interface juvenile
- student-facing areas can be more colorful than district-facing areas
- screenshots/mock interface panels instead of decorative-only doodles as the primary visual evidence

The visual result should feel like an education technology/curriculum company with classroom warmth, not a TPT storefront and not a generic gray enterprise site.

## Accessibility

Preserve and extend existing skip links, keyboard-accessible navigation, focus states, semantic headings, responsive layout, and readable contrast.

All new pages must use semantic landmarks and logical heading order. Decorative emoji/icons must not carry essential meaning.

## Technical Constraints

- Keep plain HTML, CSS, and JavaScript.
- Keep GitHub Pages compatibility.
- No framework migration.
- No external database, CMS, auth provider, payment provider, or analytics SDK in this phase.
- Reuse `style.css`, `brand.css`, and `script.js` rather than introducing a second design system.
- Existing product data in `products.js` remains intact unless a copy/navigation adjustment is required.
- Keep existing product detail pages functional.

## Testing

Extend static regression tests to verify:
- new required pages exist
- homepage primary CTAs point to Curriculum and Pilot Program
- global nav includes Curriculum, For Teachers, Schools & Districts, Pilot Program, Resources, About, and Sign In
- homepage no longer leads with Shop/Student Zone CTAs
- Teacher Hub page includes an explicit preview/demo label
- future capabilities are not mislabeled as currently available
- existing product catalog pages remain present

Run the complete static regression suite before merge.
