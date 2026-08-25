# CJ STEM Lab Visual + Commerce Refresh Design

Date: 2026-08-25
Status: Approved design, awaiting spec review before implementation planning
Repository: `brazygryl-cell/CJ_STEM_Lab`

## 1. Goal

Refresh the existing CJ STEM Lab static website so it matches the current CJ STEM Lab visual identity and supports real resource discovery and product browsing without turning the site into a generic ecommerce storefront.

The site should feel like a polished STEM education brand with playful classroom energy. The main website uses a balanced visual treatment; product cards and product-detail pages use a bolder, more playful treatment.

The refresh must preserve the current plain HTML/CSS/JavaScript architecture for GitHub Pages while preparing the structure for a later migration to a framework, custom domain, direct checkout, user accounts, and subscriptions.

## 2. Current Architecture

Keep the existing static pages and shared assets as the starting point:

- `index.html`
- `build-lab.html`
- `code-lab.html`
- `create-lab.html`
- `student-zone.html`
- `resources.html`
- `about.html`
- `contact.html`
- `style.css`
- `script.js`

The site already has semantic navigation, responsive behavior, accessibility affordances, resource filtering, and clear Build/Code/Create content pathways. These patterns should be preserved and improved rather than replaced.

## 3. Scope

### In scope

- Global visual-system refresh
- Updated navigation label: `Resources` -> `Shop & Resources`
- Homepage visual refresh and section reordering
- Real featured product cards on the homepage
- Redesign of `resources.html` into an active Shop & Resources catalog
- Individual static product-detail pages
- Shared product data in JavaScript for catalog cards
- Real product descriptions, grade ranges, formats, and preview imagery
- Etsy and TPT purchase destinations from product-detail pages
- Related-resource sections
- Responsive and accessible styling across desktop/tablet/mobile
- Structure that can later support direct CJ STEM Lab checkout and membership access

### Out of scope for this phase

- Framework migration
- Custom domain setup
- Direct payments or checkout
- Authentication/accounts
- Subscription billing
- Member-only downloads
- Database/CMS
- Automated inventory or license fulfillment

## 4. Brand Direction

### Overall website: balanced

The global site should be modern, polished, colorful, and welcoming without looking juvenile or like a worksheet enlarged into a website.

Use:

- Deep navy as the visual anchor
- White/warm-white content surfaces
- Bright teal, blue, green, yellow, orange, coral, and limited purple accents
- Rounded cards and controls
- Stronger borders and cleaner shadows than the current soft SaaS treatment
- Playful display typography for headings paired with a highly readable sans-serif body font
- Sparse STEM doodle motifs such as gears, stars, code brackets, lightbulbs, rulers, dotted paths, and robot accents
- Clear whitespace and strong content hierarchy

### Product areas: playful + bold

Product cards and product-detail pages use a more expressive treatment:

- Strong category-colored borders
- Sticker/badge treatments such as `NEW`, `PRINTABLE`, grade tags, or category tags
- Bright CTA buttons
- Larger product preview imagery
- Small playful doodle accents
- Clear price/format/grade metadata
- White space retained so the content still feels polished and trustworthy

## 5. Color Roles

Base palette should be implemented as CSS variables so the system is easy to migrate later.

Suggested semantic roles:

- Navy: navigation, headings, primary anchors, footer
- Teal/blue: Code / technology / general action accents
- Orange/yellow: Build / engineering accents
- Purple/coral: Create / design accents
- Green: success, grade/availability, positive metadata
- Warm white: page backgrounds and product surfaces

Exact values may be refined during implementation for WCAG contrast and visual consistency.

## 6. Typography

Use a two-font system:

- Rounded/playful display font for large headings and selected labels
- Clean sans-serif for body copy, navigation, forms, metadata, and long descriptions

Typography must remain legible across all screen sizes and must not rely on decorative fonts for dense instructional text.

## 7. Global Navigation

Keep a sticky responsive header.

Navigation order:

- Home
- Build Lab
- Code Lab
- Create Lab
- Student Zone
- Shop & Resources
- About
- Contact

`Shop & Resources` becomes the visually emphasized nav item rather than Contact.

The left side keeps a CJ STEM Lab brand mark/name treatment.

Mobile navigation remains simple, keyboard accessible, and controlled by the existing menu-toggle pattern unless implementation inspection reveals a reason to adjust it.

## 8. Homepage Structure

Reorder the homepage to support both the learning brand and the resource business.

### Section order

1. Hero
2. Build / Code / Create Lab cards
3. Featured Resources
4. Student Zone
5. For Educators, Families & Schools
6. About CJ STEM Lab
7. Final CTA

### Hero

Hero content should prioritize the brand itself:

- `CJ STEM Lab`
- `Build it. Code it. Create it.`
- A short supporting description of STEM, coding, design, and classroom resources
- Primary CTA: `Explore the Labs`
- Secondary CTA: `Shop Resources`

The visual panel should use restrained branded STEM motifs rather than a worksheet-style graphic.

### Lab cards

Each lab keeps a distinct accent family while sharing one component system:

- Build Lab: orange/yellow
- Code Lab: blue/teal
- Create Lab: purple/coral

### Featured Resources

Add a new section such as `Featured from CJ STEM Lab` or `Made for Real Classrooms` with 3-4 product cards and a `Shop All Resources` CTA.

## 9. Shop & Resources Page

Convert `resources.html` from a future-placeholder page into an active catalog.

### Hero

Suggested headline direction:

`Resources Built for Teaching, Learning & Creating`

The page should clearly communicate that CJ STEM Lab currently offers real digital resources.

### Filters

Initial filters:

- All
- STEM
- Computer Science
- Classroom Decor
- Activities
- Free

The filtering system should reuse or adapt the current JavaScript filtering pattern.

Future-compatible categories may include Membership and Bundles, but they are not required now.

### Product cards

Each card should include:

- Product preview image
- Product name
- Short description
- Grade range
- Format/page-count metadata where appropriate
- Price if provided
- Optional status badge (`NEW`, `PRINTABLE`, etc.)
- `View Resource` CTA

Cards should open an internal CJ STEM Lab product-detail page, not Etsy/TPT directly.

### Free resource strip

Include a small Freebies/free-resources area so the page supports discovery and value, not only sales.

## 10. Initial Real Products

At minimum, the refreshed catalog should support the products already created:

### Back to School STEM & Technology Activity Bundle

- Grades 3-6
- Printable PDF
- 10 total pages
- 9 student activities
- Topics include STEM awareness, technology, algorithms, sequencing, debugging, and engineering design

Product-detail page should include:

- Hero preview image
- Grade/format/category chips
- Short description
- `What's Included`
- `Students Practice`
- Preview gallery using watermarked sample images
- Etsy purchase button
- TPT purchase button
- Related Resources section
- Reserved future location for `Buy Direct from CJ STEM Lab`
- Reserved future membership state such as `Included with CJ STEM Lab Membership`

### Computer Science / STEM Poster Products

Support the existing poster product listings as real products in the catalog. If multiple size-specific listings remain separate on marketplaces, the internal CJ STEM Lab product structure may either represent them as separate products or as one product page with size/purchase options depending on the exact listings available at implementation time.

No marketplace URL should be invented. Exact Etsy/TPT URLs must come from real listing data before final purchase buttons are activated.

## 11. Product Architecture

Use a hybrid static architecture.

Suggested structure:

```text
CJ_STEM_Lab/
├── index.html
├── build-lab.html
├── code-lab.html
├── create-lab.html
├── student-zone.html
├── resources.html
├── about.html
├── contact.html
├── products/
│   ├── back-to-school-stem.html
│   └── stem-posters.html
├── assets/
│   ├── products/
│   ├── icons/
│   └── brand/
├── products.js
├── script.js
└── style.css
```

### `products.js`

Use one central product-data structure for catalog cards and featured-resource sections.

Product records should be able to hold:

- id/slug
- title
- short title
- category/categories
- grade range
- format
- page count/item count
- price display
- thumbnail path
- featured flag
- badges
- product-detail URL
- Etsy URL
- TPT URL

This prevents catalog metadata from being duplicated across the homepage and Shop & Resources page.

### Product-detail HTML pages

Keep individual static HTML product pages for:

- Stable, readable URLs
- SEO/indexing
- Easy GitHub Pages hosting
- Straightforward later migration to framework routes

The product-detail page may contain richer descriptive copy directly in HTML while shared card metadata remains in `products.js`.

## 12. Footer

Use a deep navy footer with:

- CJ STEM Lab name/logo treatment
- `Build it. Code it. Create it.`
- Quick navigation
- Shop & Resources link
- Social link area including TikTok
- Contact link
- Copyright

Reserve future footer space for:

- Membership
- Terms
- Privacy
- Digital-download/refund policy

## 13. Accessibility

Preserve and improve current accessibility patterns:

- Keep skip link
- Maintain semantic heading order
- Maintain keyboard-accessible navigation and filters
- Visible `:focus-visible` states
- Sufficient contrast for all accent colors and text
- Do not rely on color alone to communicate product/category/status meaning
- Use descriptive alt text for product images
- Respect reduced-motion preferences for reveal/hover effects
- Ensure mobile controls meet practical tap-target sizing

## 14. Responsive Behavior

Design mobile-first behavior intentionally rather than simply shrinking desktop cards.

- Hero stacks cleanly on small screens
- Product cards use one column on phones and expand responsively
- Product-detail purchase CTAs remain easy to reach
- Preview galleries remain readable without tiny thumbnails
- Navigation collapses using the existing responsive pattern
- Decorative doodles reduce or disappear when they interfere with content

## 15. Migration Strategy

The static site is an intermediate platform, not the permanent commerce stack.

Future migration mapping:

- `products.js` -> product API/database/CMS
- Static `products/*.html` -> dynamic framework product routes
- Etsy/TPT buttons -> direct checkout
- Public visitor -> account/session
- Purchase -> download entitlement/library
- Membership placeholder -> subscription access

The current implementation should avoid unnecessary framework-like abstractions while keeping naming and data boundaries clean enough to migrate later.

## 16. Content Rules

- Remove outdated primary messaging that says digital resources are merely `coming soon`
- Keep `coming soon` only for genuinely unreleased items/features
- Product cards should describe real products accurately
- No fabricated prices, reviews, marketplace links, customer counts, popularity claims, or standards-alignment claims
- Keep the main website educational first; product promotion should be visible but not dominate every page

## 17. Testing and Acceptance Criteria

Implementation is complete when:

- All existing primary pages still load and navigate correctly
- Navigation consistently uses `Shop & Resources`
- The homepage reflects the approved balanced brand direction
- The Shop & Resources page displays real products instead of placeholder-only catalog content
- Product cards link to internal product-detail pages
- Product-detail pages display real metadata and preview content
- Etsy/TPT buttons use only verified listing URLs or remain intentionally disabled/omitted until URLs are supplied
- Existing filters continue to work or are replaced with equivalent tested behavior
- Mobile navigation works
- Keyboard navigation and focus states work
- Layout is usable at phone, tablet, and desktop widths
- No console errors are introduced
- Existing Build/Code/Create/Student Zone content remains accessible

## 18. Implementation Constraints

- Stay on plain HTML/CSS/vanilla JavaScript
- Do not introduce React, Next.js, bundlers, package managers, or build tooling in this phase
- Do not rewrite unrelated content solely for code cleanliness
- Reuse existing semantic structure where it remains useful
- Favor shared CSS components and data-driven product cards over repeated one-off styling
- Keep the implementation easy to host on GitHub Pages

## 19. Final Approved Design Summary

The approved direction is:

- Global website aesthetic: balanced, polished modern STEM brand with playful accents
- Product-card aesthetic: playful and bold
- Product-detail aesthetic: playful and bold
- Navigation label: `Shop & Resources`
- Product flow: Shop & Resources -> internal product-detail page -> Etsy/TPT purchase button
- Architecture: plain HTML/CSS/JS now, framework/custom domain later
- Real products shown now
- Direct checkout and subscriptions deferred but structurally anticipated
