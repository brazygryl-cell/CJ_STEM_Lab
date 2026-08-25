# CJ STEM Lab Visual + Commerce Refresh Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Refresh CJ STEM Lab into a polished, colorful STEM education brand with a playful product storefront that shows real resources and routes shoppers through internal product-detail pages before Etsy/TPT.

**Architecture:** Keep the current GitHub Pages site as plain HTML/CSS/vanilla JavaScript. Add a small centralized `products.js` catalog used by the homepage and Shop & Resources page, while keeping individual static product HTML pages for stable URLs and future migration. Preserve the current navigation/reveal/filter/accessibility patterns, then layer the approved balanced global design and playful/bold product design on top.

**Tech Stack:** HTML5, CSS3, vanilla JavaScript, Python 3 standard-library tests, GitHub Pages

**Spec:** `docs/superpowers/specs/2026-08-25-cj-stem-lab-visual-commerce-refresh-design.md`

## Global Constraints

- Stay on plain HTML/CSS/vanilla JavaScript.
- Do not introduce React, Next.js, bundlers, package managers, or build tooling in this phase.
- Keep the implementation easy to host on GitHub Pages under the repository subpath.
- Global site aesthetic: balanced, polished modern STEM brand with playful accents.
- Product-card and product-detail aesthetic: playful and bold.
- Navigation label: `Shop & Resources`.
- Product flow: Shop & Resources -> internal product-detail page -> verified Etsy/TPT purchase button.
- Do not fabricate prices, reviews, marketplace URLs, customer counts, popularity claims, or standards-alignment claims.
- Marketplace buttons must render only when the corresponding URL is verified and non-empty.
- Preserve skip-link behavior, semantic heading order, keyboard navigation, visible focus states, reduced-motion support, and practical mobile tap targets.
- Product/category/status meaning must not rely on color alone.
- Keep Build Lab, Code Lab, Create Lab, Student Zone, About, and Contact content accessible throughout the refresh.

---

## File Structure

### Existing files to modify

- `index.html` — homepage structure, hero, lab cards, featured products, audience/about/CTA ordering
- `resources.html` — active Shop & Resources catalog and filters
- `build-lab.html` — global navigation/footer visual markup updates only
- `code-lab.html` — global navigation/footer visual markup updates only
- `create-lab.html` — global navigation/footer visual markup updates only
- `student-zone.html` — global navigation/footer visual markup updates only; preserve current Student Zone filter behavior
- `about.html` — global navigation/footer visual markup updates only
- `contact.html` — global navigation/footer visual markup updates only
- `style.css` — global design system, product cards, shop, product-detail pages, responsive behavior
- `script.js` — preserve current UI behavior; add product rendering, Shop filtering, and conditional marketplace-link rendering

### New files/directories

- `products.js` — centralized catalog metadata for homepage/shop cards and purchase-link lookup
- `products/back-to-school-stem.html` — internal Back to School STEM & Technology product page
- `products/computer-science-stem-posters.html` — internal 13-poster product page
- `assets/products/back-to-school-stem/cover.png`
- `assets/products/back-to-school-stem/preview-1.png`
- `assets/products/back-to-school-stem/preview-2.png`
- `assets/products/back-to-school-stem/preview-3.png`
- `assets/products/computer-science-stem-posters/cover.png`
- `assets/products/computer-science-stem-posters/preview-1.png`
- `assets/products/computer-science-stem-posters/preview-2.png`
- `assets/products/computer-science-stem-posters/preview-3.png`
- `tests/test_static_site.py` — structural regression checks for static pages, catalog, navigation, and product pages

---

### Task 1: Establish the static-site regression harness

**Files:**
- Create: `tests/test_static_site.py`

**Interfaces:**
- Consumes: current repository files only
- Produces: `read_text(relative_path: str) -> str`, `PRIMARY_PAGES`, and baseline `unittest` checks used by later tasks

- [ ] **Step 1: Create the baseline test file**

```python
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

PRIMARY_PAGES = [
    "index.html",
    "build-lab.html",
    "code-lab.html",
    "create-lab.html",
    "student-zone.html",
    "resources.html",
    "about.html",
    "contact.html",
]


def read_text(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


class StaticSiteBaselineTests(unittest.TestCase):
    def test_primary_pages_exist(self):
        for page in PRIMARY_PAGES:
            with self.subTest(page=page):
                self.assertTrue((ROOT / page).is_file())

    def test_primary_pages_keep_skip_link(self):
        for page in PRIMARY_PAGES:
            with self.subTest(page=page):
                self.assertIn('class="skip-link"', read_text(page))

    def test_root_pages_load_shared_stylesheet_and_script(self):
        for page in PRIMARY_PAGES:
            html = read_text(page)
            with self.subTest(page=page):
                self.assertIn('href="style.css"', html)
                self.assertIn('src="script.js"', html)

    def test_reduced_motion_rule_exists(self):
        self.assertIn("@media (prefers-reduced-motion: reduce)", read_text("style.css"))


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the baseline tests**

Run:

```bash
python3 -m unittest tests.test_static_site -v
```

Expected: all four baseline tests pass before any visual/product changes.

- [ ] **Step 3: Syntax-check the existing JavaScript**

Run:

```bash
node --check script.js
```

Expected: no output and exit code 0. If `node` is not installed in the execution environment, record that limitation and continue using browser/manual JavaScript verification in Task 8; do not add Node/npm to the project.

- [ ] **Step 4: Commit the test harness**

```bash
git add tests/test_static_site.py
git commit -m "test: add static site regression checks"
```

---

### Task 2: Add centralized product data and rendering primitives

**Files:**
- Create: `products.js`
- Modify: `script.js`
- Modify: `tests/test_static_site.py`

**Interfaces:**
- Consumes: `window.CJ_STEM_PRODUCTS`
- Produces: `getProductById(id)`, `createProductCard(product)`, `renderProductGrid(container, products)`, `renderFeaturedProducts()`, `renderShopProducts()`, `renderPurchaseLinks()`
- Product records expose: `id`, `title`, `shortTitle`, `description`, `categories`, `gradeRange`, `format`, `details`, `price`, `thumbnail`, `detailUrl`, `featured`, `badges`, `etsyUrl`, `tptUrl`

- [ ] **Step 1: Add failing catalog tests**

Append these methods to `StaticSiteBaselineTests`:

```python
    def test_product_catalog_defines_real_products(self):
        catalog = read_text("products.js")
        self.assertIn('id: "back-to-school-stem"', catalog)
        self.assertIn('id: "computer-science-stem-posters"', catalog)
        self.assertIn('gradeRange: "Grades 3–6"', catalog)
        self.assertIn('details: "10 pages • 9 student activities"', catalog)
        self.assertIn('details: "13 posters • 8.5×11, 8.5×14, and 11×17"', catalog)

    def test_script_has_product_rendering_interfaces(self):
        script = read_text("script.js")
        for name in [
            "getProductById",
            "createProductCard",
            "renderProductGrid",
            "renderFeaturedProducts",
            "renderShopProducts",
            "renderPurchaseLinks",
        ]:
            with self.subTest(name=name):
                self.assertIn(f"function {name}", script)
```

- [ ] **Step 2: Run the new tests to verify they fail**

Run:

```bash
python3 -m unittest tests.test_static_site.StaticSiteBaselineTests.test_product_catalog_defines_real_products tests.test_static_site.StaticSiteBaselineTests.test_script_has_product_rendering_interfaces -v
```

Expected: FAIL because `products.js` does not exist and the new functions are not in `script.js`.

- [ ] **Step 3: Create `products.js` with the approved initial catalog**

```javascript
window.CJ_STEM_PRODUCTS = [
  {
    id: "back-to-school-stem",
    title: "Back to School STEM & Technology Activity Bundle",
    shortTitle: "Back to School STEM & Technology",
    description:
      "Nine print-and-go activities that introduce STEM, technology, algorithms, debugging, and engineering design during the first days of school.",
    categories: ["stem", "computer-science", "activities"],
    gradeRange: "Grades 3–6",
    format: "Printable PDF",
    details: "10 pages • 9 student activities",
    price: "$3.99",
    thumbnail: "assets/products/back-to-school-stem/cover.png",
    detailUrl: "products/back-to-school-stem.html",
    featured: true,
    badges: ["NEW", "PRINTABLE"],
    etsyUrl: "",
    tptUrl: ""
  },
  {
    id: "computer-science-stem-posters",
    title: "Computer Science & STEM Poster Bundle",
    shortTitle: "Computer Science & STEM Posters",
    description:
      "A 13-poster classroom set covering engineering design, computational thinking, debugging, hardware and software, data, internet and web concepts, AI literacy, digital citizenship, web development, binary, cybersecurity, algorithms, and STEM careers.",
    categories: ["stem", "computer-science", "classroom-decor"],
    gradeRange: "Middle School",
    format: "Printable PDF",
    details: "13 posters • 8.5×11, 8.5×14, and 11×17",
    price: "",
    thumbnail: "assets/products/computer-science-stem-posters/cover.png",
    detailUrl: "products/computer-science-stem-posters.html",
    featured: true,
    badges: ["13 POSTERS", "PRINTABLE"],
    etsyUrl: "",
    tptUrl: ""
  }
];
```

`etsyUrl` and `tptUrl` are intentionally empty until exact listing URLs are verified. Do not substitute search URLs or guessed shop URLs.

- [ ] **Step 4: Add product helpers near the top of `script.js` inside the `DOMContentLoaded` callback**

```javascript
  const products = Array.isArray(window.CJ_STEM_PRODUCTS)
    ? window.CJ_STEM_PRODUCTS
    : [];

  function getProductById(id) {
    return products.find((product) => product.id === id) || null;
  }

  function createProductCard(product) {
    const card = document.createElement("article");
    card.className = `product-card product-card--${product.categories[0] || "general"} reveal`;
    card.dataset.categories = product.categories.join(" ");

    const badges = product.badges
      .map((badge) => `<span class="product-badge">${badge}</span>`)
      .join("");

    const price = product.price
      ? `<p class="product-price">${product.price}</p>`
      : "";

    card.innerHTML = `
      <div class="product-image-wrap">
        <img src="${product.thumbnail}" alt="Preview of ${product.title}" loading="lazy">
        <div class="product-badges">${badges}</div>
      </div>
      <div class="product-card-body">
        <p class="product-grade">${product.gradeRange}</p>
        <h3>${product.title}</h3>
        <p>${product.description}</p>
        <p class="product-meta">${product.details} • ${product.format}</p>
        ${price}
        <a class="btn btn-product" href="${product.detailUrl}">View Resource</a>
      </div>
    `;

    return card;
  }

  function renderProductGrid(container, productList) {
    if (!container) return;
    container.replaceChildren(...productList.map(createProductCard));
  }

  function renderFeaturedProducts() {
    const container = document.querySelector('[data-product-grid="featured"]');
    if (!container) return;
    renderProductGrid(container, products.filter((product) => product.featured));
  }

  function renderShopProducts() {
    const container = document.querySelector('[data-product-grid="shop"]');
    if (!container) return;

    renderProductGrid(container, products);

    const buttons = document.querySelectorAll("[data-product-filter]");
    buttons.forEach((button) => {
      button.addEventListener("click", () => {
        const filter = button.dataset.productFilter;
        buttons.forEach((item) => item.classList.remove("active"));
        button.classList.add("active");

        const filtered = filter === "all"
          ? products
          : products.filter((product) => product.categories.includes(filter));

        renderProductGrid(container, filtered);
      });
    });
  }

  function renderPurchaseLinks() {
    document.querySelectorAll("[data-purchase-links]").forEach((container) => {
      const product = getProductById(container.dataset.purchaseLinks);
      if (!product) return;

      const links = [
        product.etsyUrl
          ? `<a class="btn marketplace-btn marketplace-btn--etsy" href="${product.etsyUrl}" target="_blank" rel="noopener">Buy on Etsy</a>`
          : "",
        product.tptUrl
          ? `<a class="btn marketplace-btn marketplace-btn--tpt" href="${product.tptUrl}" target="_blank" rel="noopener">Buy on TPT</a>`
          : ""
      ].filter(Boolean);

      container.innerHTML = links.length
        ? links.join("")
        : '<p class="purchase-note">Marketplace purchase links are being verified.</p>';
    });
  }
```

- [ ] **Step 5: Call the new rendering functions at the end of the existing `DOMContentLoaded` callback**

```javascript
  renderFeaturedProducts();
  renderShopProducts();
  renderPurchaseLinks();
```

Do not remove the current year, mobile-nav, back-to-top, reveal, or Student Zone/resource-preview filtering logic yet.

- [ ] **Step 6: Run tests and JavaScript syntax checks**

```bash
python3 -m unittest tests.test_static_site -v
node --check products.js
node --check script.js
```

Expected: all Python tests pass; Node checks exit 0 when Node is available.

- [ ] **Step 7: Commit the catalog layer**

```bash
git add products.js script.js tests/test_static_site.py
git commit -m "feat: add product catalog rendering"
```

---

### Task 3: Apply the global brand system, navigation, and footer

**Files:**
- Modify: `style.css`
- Modify: `index.html`
- Modify: `build-lab.html`
- Modify: `code-lab.html`
- Modify: `create-lab.html`
- Modify: `student-zone.html`
- Modify: `resources.html`
- Modify: `about.html`
- Modify: `contact.html`
- Modify: `tests/test_static_site.py`

**Interfaces:**
- Consumes: existing `.site-header`, `.navbar`, `.logo`, `.nav-menu`, `.site-footer` markup patterns
- Produces: shared brand variables, `nav-shop` emphasis, dark branded footer, consistent global card/button system

- [ ] **Step 1: Add failing navigation/footer tests**

```python
    def test_all_primary_pages_use_shop_resources_label(self):
        for page in PRIMARY_PAGES:
            html = read_text(page)
            with self.subTest(page=page):
                self.assertIn("Shop &amp; Resources", html)
                self.assertNotIn(">Resources</a>", html)

    def test_all_primary_pages_have_shop_nav_class(self):
        for page in PRIMARY_PAGES:
            with self.subTest(page=page):
                self.assertIn('class="nav-shop', read_text(page))

    def test_footer_has_brand_tagline_and_tiktok_area(self):
        for page in PRIMARY_PAGES:
            html = read_text(page)
            with self.subTest(page=page):
                self.assertIn("Build it. Code it. Create it.", html)
                self.assertIn('class="footer-social"', html)
                self.assertIn("TikTok", html)
```

- [ ] **Step 2: Run the tests to verify they fail**

```bash
python3 -m unittest tests.test_static_site.StaticSiteBaselineTests.test_all_primary_pages_use_shop_resources_label tests.test_static_site.StaticSiteBaselineTests.test_all_primary_pages_have_shop_nav_class tests.test_static_site.StaticSiteBaselineTests.test_footer_has_brand_tagline_and_tiktok_area -v
```

Expected: FAIL on the current `Resources` nav/footer labels and missing `nav-shop`/`footer-social` markup.

- [ ] **Step 3: Replace the top `:root` palette and font roles in `style.css`**

```css
:root {
  --bg: #fffdf8;
  --bg-soft: #f4fbfc;
  --bg-warm: #fff7e8;
  --card: #ffffff;

  --text: #26384a;
  --text-muted: #607184;
  --navy: #17385f;
  --navy-deep: #0f2948;

  --teal: #18b8b2;
  --blue: #3c8ed8;
  --green: #67b84f;
  --yellow: #f6c744;
  --orange: #f4873f;
  --coral: #ee675f;
  --purple: #7d69c8;

  --border: #d7e2ea;
  --border-strong: #b9cad7;
  --shadow: 0 12px 28px rgba(15, 41, 72, 0.13);
  --soft-shadow: 0 7px 0 rgba(15, 41, 72, 0.05), 0 14px 24px rgba(15, 41, 72, 0.08);

  --radius-sm: 12px;
  --radius-md: 20px;
  --radius-lg: 30px;

  --font-display: "Arial Rounded MT Bold", "Trebuchet MS", system-ui, sans-serif;
  --font-body: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;

  --max-width: 1180px;
  --header-height: 78px;
}
```

Update body/headings to use the roles:

```css
body {
  min-height: 100vh;
  background:
    radial-gradient(circle at 8% 4%, rgba(24, 184, 178, 0.12), transparent 24rem),
    radial-gradient(circle at 92% 7%, rgba(246, 199, 68, 0.18), transparent 23rem),
    linear-gradient(180deg, var(--bg) 0%, #ffffff 52%, var(--bg-soft) 100%);
  color: var(--text);
  font-family: var(--font-body);
  line-height: 1.6;
}

h1,
h2,
h3,
.logo-text strong,
.eyebrow,
.btn,
.product-badge {
  font-family: var(--font-display);
}
```

- [ ] **Step 4: Restyle the header/nav so Shop & Resources is the emphasized nav item**

```css
.site-header {
  position: sticky;
  top: 0;
  z-index: 100;
  min-height: var(--header-height);
  background: rgba(255, 253, 248, 0.94);
  backdrop-filter: blur(18px);
  border-bottom: 2px solid rgba(23, 56, 95, 0.1);
  box-shadow: 0 6px 20px rgba(15, 41, 72, 0.06);
}

.logo-mark {
  border: 2px solid var(--navy);
  background: linear-gradient(135deg, var(--teal), var(--blue));
  box-shadow: 4px 4px 0 rgba(23, 56, 95, 0.14);
}

.nav-menu a {
  border: 2px solid transparent;
  background: transparent;
}

.nav-menu a:hover,
.nav-menu a:focus-visible,
.nav-menu a.active {
  color: var(--navy);
  border-color: rgba(24, 184, 178, 0.28);
  background: rgba(24, 184, 178, 0.1);
}

.nav-menu .nav-shop {
  color: #ffffff;
  border-color: var(--navy-deep);
  background: var(--navy);
  box-shadow: 3px 3px 0 rgba(246, 199, 68, 0.75);
}

.nav-menu .nav-shop:hover,
.nav-menu .nav-shop:focus-visible,
.nav-menu .nav-shop.active {
  color: #ffffff;
  border-color: var(--navy-deep);
  background: var(--navy-deep);
  box-shadow: 4px 4px 0 rgba(246, 199, 68, 0.9);
}
```

- [ ] **Step 5: Update the nav markup on all eight root pages**

Use this exact link form in every nav; apply `active` in addition to `nav-shop` on `resources.html` only:

```html
<li><a href="resources.html" class="nav-shop">Shop &amp; Resources</a></li>
```

On `resources.html`:

```html
<li><a href="resources.html" class="nav-shop active">Shop &amp; Resources</a></li>
```

Keep Contact as a normal navigation link rather than the old `nav-cta` treatment:

```html
<li><a href="contact.html">Contact</a></li>
```

- [ ] **Step 6: Replace the footer markup on all eight root pages with the shared branded structure**

```html
<footer class="site-footer">
  <div class="footer-brand-block">
    <a href="index.html" class="logo footer-brand">
      <span class="logo-mark">CJ</span>
      <span class="logo-text">
        <strong>CJ STEM Lab</strong>
        <small>Build it. Code it. Create it.</small>
      </span>
    </a>
    <p>STEM, coding, design, and classroom-ready resources for curious learners.</p>
  </div>

  <div class="footer-links" aria-label="Footer navigation">
    <a href="build-lab.html">Build Lab</a>
    <a href="code-lab.html">Code Lab</a>
    <a href="create-lab.html">Create Lab</a>
    <a href="student-zone.html">Student Zone</a>
    <a href="resources.html">Shop &amp; Resources</a>
    <a href="about.html">About</a>
    <a href="contact.html">Contact</a>
  </div>

  <div class="footer-social" aria-label="Social links">
    <span>TikTok</span>
  </div>

  <p class="footer-copy">© <span id="year"></span> CJ STEM Lab by Ms. CJ. All rights reserved.</p>
</footer>
```

Do not create a fake TikTok `href`. Convert the `<span>` to an anchor only after the exact account URL is known.

- [ ] **Step 7: Replace footer styles with the dark branded footer**

```css
.site-footer {
  width: 100%;
  margin: 0;
  padding: 3rem max(1rem, calc((100vw - var(--max-width)) / 2));
  display: grid;
  grid-template-columns: minmax(260px, 1.2fr) minmax(260px, 1fr) auto;
  align-items: start;
  gap: 2rem;
  border-top: 0;
  background: var(--navy-deep);
  color: #ffffff;
}

.site-footer p,
.site-footer small,
.site-footer span,
.site-footer a {
  color: rgba(255, 255, 255, 0.82);
}

.site-footer .logo-text strong {
  color: #ffffff;
}

.footer-brand-block {
  display: grid;
  gap: 1rem;
}

.footer-links {
  display: grid;
  grid-template-columns: repeat(2, minmax(120px, 1fr));
  gap: 0.65rem 1rem;
}

.footer-links a,
.footer-social span {
  font-weight: 800;
  text-decoration: none;
}

.footer-links a:hover,
.footer-links a:focus-visible {
  color: var(--yellow);
}

.footer-social {
  display: flex;
  gap: 0.75rem;
}

.footer-copy {
  grid-column: 1 / -1;
  padding-top: 1.25rem;
  border-top: 1px solid rgba(255, 255, 255, 0.16);
}
```

- [ ] **Step 8: Run tests and commit global brand changes**

```bash
python3 -m unittest tests.test_static_site -v
git add style.css index.html build-lab.html code-lab.html create-lab.html student-zone.html resources.html about.html contact.html tests/test_static_site.py
git commit -m "feat: refresh global CJ STEM Lab branding"
```

---

### Task 4: Rebuild the homepage hierarchy and add Featured Resources

**Files:**
- Modify: `index.html`
- Modify: `style.css`
- Modify: `tests/test_static_site.py`

**Interfaces:**
- Consumes: `products.js`, `renderFeaturedProducts()`, existing Build/Code/Create/Student Zone content
- Produces: homepage section order `hero -> labs -> featured products -> student zone -> audiences -> about -> final CTA`

- [ ] **Step 1: Add failing homepage structure tests**

```python
    def test_homepage_loads_product_catalog_before_script(self):
        html = read_text("index.html")
        self.assertIn('src="products.js"', html)
        self.assertLess(html.index('src="products.js"'), html.index('src="script.js"'))

    def test_homepage_has_featured_product_mount(self):
        html = read_text("index.html")
        self.assertIn('data-product-grid="featured"', html)
        self.assertIn("Shop Resources", html)
        self.assertIn("Explore the Labs", html)

    def test_homepage_section_order(self):
        html = read_text("index.html")
        markers = [
            'id="home-hero"',
            'id="labs"',
            'id="featured-resources"',
            'id="student-zone-preview"',
            'id="audiences"',
            'id="about-preview"',
            'id="home-cta"',
        ]
        positions = [html.index(marker) for marker in markers]
        self.assertEqual(positions, sorted(positions))
```

- [ ] **Step 2: Run the homepage tests to verify they fail**

```bash
python3 -m unittest tests.test_static_site.StaticSiteBaselineTests.test_homepage_loads_product_catalog_before_script tests.test_static_site.StaticSiteBaselineTests.test_homepage_has_featured_product_mount tests.test_static_site.StaticSiteBaselineTests.test_homepage_section_order -v
```

Expected: FAIL because the current homepage has the old hero/resource preview order and no `products.js` mount.

- [ ] **Step 3: Replace the homepage hero with the approved brand-first hero**

```html
<section id="home-hero" class="hero section brand-hero">
  <div class="hero-content reveal">
    <p class="eyebrow">CJ STEM Lab</p>
    <h1>Build it. Code it. Create it.</h1>
    <p class="hero-subtitle">
      Hands-on STEM, coding, creative technology, and classroom-ready resources designed to help students think, make, test, and grow.
    </p>
    <div class="hero-actions">
      <a href="#labs" class="btn btn-primary">Explore the Labs</a>
      <a href="resources.html" class="btn btn-secondary">Shop Resources</a>
    </div>
  </div>

  <div class="brand-hero-art reveal" aria-label="CJ STEM Lab themes: engineering, coding, science, and design">
    <span class="hero-doodle hero-doodle--gear" aria-hidden="true">⚙</span>
    <span class="hero-doodle hero-doodle--code" aria-hidden="true">&lt;/&gt;</span>
    <span class="hero-doodle hero-doodle--idea" aria-hidden="true">💡</span>
    <div class="brand-hero-card">
      <p class="preview-label">Inside the Lab</p>
      <strong>STEM + Coding + Design</strong>
      <p>Projects, challenges, printable resources, and creative problem-solving.</p>
    </div>
  </div>
</section>
```

- [ ] **Step 4: Give the existing lab pathway section `id="labs"` and preserve the three existing cards**

The opening tag becomes:

```html
<section id="labs" class="section">
```

Keep the existing Build Lab, Code Lab, and Create Lab card copy and links.

- [ ] **Step 5: Replace the old “Resource Library / coming soon” homepage section with the real Featured Resources mount**

```html
<section id="featured-resources" class="section featured-products-section soft-section">
  <div class="section-heading reveal">
    <p class="eyebrow">Made for Real Classrooms</p>
    <h2>Featured from CJ STEM Lab</h2>
    <p>Print-and-go activities and classroom visuals created for STEM and Computer Science learning.</p>
  </div>

  <div class="product-grid" data-product-grid="featured" aria-live="polite"></div>

  <div class="section-action reveal">
    <a href="resources.html" class="btn btn-product">Shop All Resources</a>
  </div>
</section>
```

- [ ] **Step 6: Reorder the remaining existing sections without rewriting their educational substance**

Use these exact IDs on the corresponding existing sections:

```html
<section id="student-zone-preview" class="section student-zone-preview">
<section id="audiences" class="section audience-strip-section">
<section id="about-preview" class="section about-preview soft-section">
<section id="home-cta" class="section final-cta-section">
```

Move the current audience content after Student Zone. Remove the old standalone “Why CJ STEM Lab?” section only if its three messages are incorporated into the audience/about section; otherwise keep its three cards inside `#audiences` so no substantive value proposition is lost.

- [ ] **Step 7: Add homepage/product-grid styling**

```css
.brand-hero-art {
  position: relative;
  min-height: 430px;
  display: grid;
  place-items: center;
  border: 2px solid var(--navy);
  border-radius: var(--radius-lg);
  background:
    radial-gradient(circle at 20% 25%, rgba(246, 199, 68, 0.38), transparent 7rem),
    radial-gradient(circle at 80% 70%, rgba(125, 105, 200, 0.2), transparent 8rem),
    #ffffff;
  box-shadow: 8px 8px 0 rgba(24, 184, 178, 0.2);
  overflow: hidden;
}

.brand-hero-card {
  width: min(78%, 360px);
  padding: 2rem;
  border: 2px solid var(--navy);
  border-radius: 24px;
  background: #ffffff;
  box-shadow: 6px 6px 0 rgba(246, 199, 68, 0.75);
}

.hero-doodle {
  position: absolute;
  font-family: var(--font-display);
  font-weight: 900;
}

.hero-doodle--gear { top: 10%; left: 10%; color: var(--teal); font-size: 3rem; }
.hero-doodle--code { right: 9%; top: 18%; color: var(--orange); font-size: 2rem; }
.hero-doodle--idea { right: 13%; bottom: 11%; font-size: 2.5rem; }

.product-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 1.2rem;
}
```

- [ ] **Step 8: Load `products.js` before `script.js` on the homepage**

```html
<script src="products.js"></script>
<script src="script.js"></script>
```

- [ ] **Step 9: Run tests and commit the homepage**

```bash
python3 -m unittest tests.test_static_site -v
node --check products.js
node --check script.js
git add index.html style.css tests/test_static_site.py
git commit -m "feat: rebuild homepage around labs and resources"
```

---

### Task 5: Convert Resources into the active Shop & Resources catalog

**Files:**
- Modify: `resources.html`
- Modify: `style.css`
- Modify: `tests/test_static_site.py`

**Interfaces:**
- Consumes: `products.js`, `renderShopProducts()`
- Produces: filter buttons with `data-product-filter`, catalog mount `data-product-grid="shop"`, free-resource strip

- [ ] **Step 1: Add failing Shop & Resources tests**

```python
    def test_shop_page_is_active_catalog_not_placeholder(self):
        html = read_text("resources.html")
        self.assertIn("Resources Built for Teaching, Learning &amp; Creating", html)
        self.assertIn('data-product-grid="shop"', html)
        self.assertNotIn("Digital downloads and resource packs are coming soon.", html)

    def test_shop_page_has_required_filters(self):
        html = read_text("resources.html")
        for value in ["all", "stem", "computer-science", "classroom-decor", "activities", "free"]:
            with self.subTest(value=value):
                self.assertIn(f'data-product-filter="{value}"', html)

    def test_shop_page_loads_products_before_script(self):
        html = read_text("resources.html")
        self.assertLess(html.index('src="products.js"'), html.index('src="script.js"'))
```

- [ ] **Step 2: Run the tests to verify they fail**

```bash
python3 -m unittest tests.test_static_site.StaticSiteBaselineTests.test_shop_page_is_active_catalog_not_placeholder tests.test_static_site.StaticSiteBaselineTests.test_shop_page_has_required_filters tests.test_static_site.StaticSiteBaselineTests.test_shop_page_loads_products_before_script -v
```

Expected: FAIL on the old Resource Library placeholder content and missing catalog mount.

- [ ] **Step 3: Replace the Shop page hero and remove the old “coming soon” notice**

```html
<section class="page-hero section shop-hero">
  <div class="page-hero-content reveal">
    <p class="eyebrow">Shop &amp; Resources</p>
    <h1>Resources Built for Teaching, Learning &amp; Creating</h1>
    <p class="hero-subtitle">
      Browse printable STEM activities, Computer Science resources, and classroom visuals from CJ STEM Lab.
    </p>
    <div class="hero-actions">
      <a href="#shop-catalog" class="btn btn-primary">Browse Resources</a>
      <a href="#free-resources" class="btn btn-secondary">Find Freebies</a>
    </div>
  </div>

  <div class="page-hero-card shop-hero-card reveal">
    <p class="preview-label">CJ STEM Lab Resources</p>
    <ul class="check-list">
      <li>Print-and-go student activities</li>
      <li>STEM and Computer Science visuals</li>
      <li>Classroom-ready digital downloads</li>
      <li>More resources added over time</li>
    </ul>
  </div>
</section>
```

- [ ] **Step 4: Replace the old sample-resource grid with the catalog filters and mount**

```html
<section id="shop-catalog" class="section">
  <div class="section-heading reveal">
    <p class="eyebrow">Browse the Shop</p>
    <h2>Find a resource for your classroom.</h2>
    <p>Filter by resource type, then open a product page to see previews and purchase options.</p>
  </div>

  <div class="product-filter-bar reveal" aria-label="Product filters">
    <button class="filter-btn active" data-product-filter="all">All</button>
    <button class="filter-btn" data-product-filter="stem">STEM</button>
    <button class="filter-btn" data-product-filter="computer-science">Computer Science</button>
    <button class="filter-btn" data-product-filter="classroom-decor">Classroom Decor</button>
    <button class="filter-btn" data-product-filter="activities">Activities</button>
    <button class="filter-btn" data-product-filter="free">Free</button>
  </div>

  <div class="product-grid shop-product-grid" data-product-grid="shop" aria-live="polite"></div>
</section>
```

There are currently no `free` products in the initial catalog, so filtering to Free should intentionally render an empty grid rather than invent a free product.

- [ ] **Step 5: Add a non-product Freebies strip that does not falsely advertise a downloadable file**

```html
<section id="free-resources" class="section freebies-strip-section soft-section">
  <div class="freebies-strip reveal">
    <div>
      <p class="eyebrow">Freebies</p>
      <h2>Free CJ STEM Lab resources will live here.</h2>
      <p>Use this section for future free downloads, sample pages, and classroom challenges without mixing them into paid product cards before they exist.</p>
    </div>
    <a href="student-zone.html" class="btn btn-secondary">Try Student Challenges</a>
  </div>
</section>
```

- [ ] **Step 6: Add the playful/bold product-card styles**

```css
.product-card {
  position: relative;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  min-height: 100%;
  border: 2px solid var(--navy);
  border-radius: 22px;
  background: #ffffff;
  box-shadow: 6px 6px 0 rgba(23, 56, 95, 0.12);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.product-card:hover,
.product-card:focus-within {
  transform: translateY(-5px) rotate(-0.15deg);
  box-shadow: 8px 8px 0 rgba(23, 56, 95, 0.16);
}

.product-card--stem { border-top: 8px solid var(--orange); }
.product-card--computer-science { border-top: 8px solid var(--teal); }
.product-card--classroom-decor { border-top: 8px solid var(--purple); }

.product-image-wrap {
  position: relative;
  aspect-ratio: 4 / 3;
  overflow: hidden;
  background: var(--bg-warm);
  border-bottom: 2px solid var(--navy);
}

.product-image-wrap img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.product-badges {
  position: absolute;
  left: 0.75rem;
  top: 0.75rem;
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
}

.product-badge {
  display: inline-flex;
  padding: 0.32rem 0.62rem;
  border: 2px solid var(--navy);
  border-radius: 999px;
  background: var(--yellow);
  color: var(--navy-deep);
  font-size: 0.7rem;
  font-weight: 900;
}

.product-card-body {
  display: flex;
  flex: 1;
  flex-direction: column;
  padding: 1.2rem;
}

.product-grade {
  color: var(--coral);
  font-size: 0.78rem;
  font-weight: 900;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.product-meta {
  margin-top: 0.8rem;
  font-size: 0.88rem;
}

.product-price {
  margin-top: auto;
  padding-top: 1rem;
  color: var(--navy-deep);
  font-family: var(--font-display);
  font-size: 1.35rem;
  font-weight: 900;
}

.btn-product {
  margin-top: 1rem;
  color: #ffffff;
  border: 2px solid var(--navy-deep);
  background: var(--navy);
  box-shadow: 3px 3px 0 var(--yellow);
}

.btn-product:hover,
.btn-product:focus-visible {
  background: var(--navy-deep);
  box-shadow: 4px 4px 0 var(--yellow);
}

.freebies-strip {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1.5rem;
  padding: 2rem;
  border: 2px dashed var(--teal);
  border-radius: var(--radius-lg);
  background: #ffffff;
}
```

- [ ] **Step 7: Load `products.js` before `script.js` on `resources.html`**

```html
<script src="products.js"></script>
<script src="script.js"></script>
```

- [ ] **Step 8: Run tests and commit the catalog page**

```bash
python3 -m unittest tests.test_static_site -v
node --check products.js
node --check script.js
git add resources.html style.css tests/test_static_site.py
git commit -m "feat: turn resources into active product catalog"
```

---

### Task 6: Build the Back to School STEM product page with real previews

**Files:**
- Create: `products/back-to-school-stem.html`
- Create binary assets under: `assets/products/back-to-school-stem/`
- Modify: `style.css`
- Modify: `tests/test_static_site.py`

**Interfaces:**
- Consumes: product id `back-to-school-stem`, existing approved bundle images from the current workspace, `renderPurchaseLinks()`
- Produces: stable internal URL `products/back-to-school-stem.html`

- [ ] **Step 1: Add failing product-page tests**

```python
    def test_back_to_school_product_page_exists_and_is_complete(self):
        html = read_text("products/back-to-school-stem.html")
        self.assertIn("Back to School STEM &amp; Technology Activity Bundle", html)
        self.assertIn("Grades 3–6", html)
        self.assertIn("10 pages", html)
        self.assertIn("9 student activities", html)
        self.assertIn('data-purchase-links="back-to-school-stem"', html)
        self.assertIn("What’s Included", html)
        self.assertIn("Students Practice", html)
        self.assertIn("Related Resources", html)

    def test_back_to_school_product_assets_are_referenced(self):
        html = read_text("products/back-to-school-stem.html")
        for image in ["cover.png", "preview-1.png", "preview-2.png", "preview-3.png"]:
            with self.subTest(image=image):
                self.assertIn(f'../assets/products/back-to-school-stem/{image}', html)
```

- [ ] **Step 2: Run the tests to verify they fail**

```bash
python3 -m unittest tests.test_static_site.StaticSiteBaselineTests.test_back_to_school_product_page_exists_and_is_complete tests.test_static_site.StaticSiteBaselineTests.test_back_to_school_product_assets_are_referenced -v
```

Expected: FAIL because the product page and assets do not exist.

- [ ] **Step 3: Copy the approved real bundle imagery into web assets**

Use the current workspace images exactly as follows:

```bash
mkdir -p assets/products/back-to-school-stem
cp /mnt/data/colorful_back_to_school_stem_activity_bundle.png assets/products/back-to-school-stem/cover.png
cp /mnt/data/back_to_school_stem_activity_bundle.png assets/products/back-to-school-stem/preview-1.png
cp /mnt/data/back_to_school_stem_worksheet_bundle.png assets/products/back-to-school-stem/preview-2.png
cp /mnt/data/colorful_stem_printable_activity_bundle.png assets/products/back-to-school-stem/preview-3.png
```

If those `/mnt/data` files are not present in a later execution environment, stop this task and retrieve the same four approved images from the conversation/File Library. Do not replace them with generic stock or newly invented product previews.

- [ ] **Step 4: Create the product-detail page with correct relative paths**

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Back to School STEM & Technology Activity Bundle | CJ STEM Lab</title>
  <meta name="description" content="A printable Back to School STEM and Technology activity bundle for grades 3–6 with nine student activities covering STEM, technology, algorithms, debugging, and engineering design." />
  <link rel="stylesheet" href="../style.css" />
</head>
<body>
  <a class="skip-link" href="#main-content">Skip to main content</a>

  <header class="site-header">
    <nav class="navbar" aria-label="Main navigation">
      <a href="../index.html" class="logo" aria-label="CJ STEM Lab home">
        <span class="logo-mark">CJ</span>
        <span class="logo-text"><strong>CJ STEM Lab</strong><small>by Ms. CJ</small></span>
      </a>
      <button class="nav-toggle" aria-label="Open navigation menu" aria-expanded="false"><span></span><span></span><span></span></button>
      <ul class="nav-menu">
        <li><a href="../index.html">Home</a></li>
        <li><a href="../build-lab.html">Build Lab</a></li>
        <li><a href="../code-lab.html">Code Lab</a></li>
        <li><a href="../create-lab.html">Create Lab</a></li>
        <li><a href="../student-zone.html">Student Zone</a></li>
        <li><a href="../resources.html" class="nav-shop active">Shop &amp; Resources</a></li>
        <li><a href="../about.html">About</a></li>
        <li><a href="../contact.html">Contact</a></li>
      </ul>
    </nav>
  </header>

  <main id="main-content">
    <section class="section product-detail-hero">
      <div class="product-gallery reveal">
        <div class="product-main-image">
          <img src="../assets/products/back-to-school-stem/cover.png" alt="Cover of the Back to School STEM and Technology Activity Bundle" />
        </div>
        <div class="product-thumbnails" aria-label="Resource preview images">
          <img src="../assets/products/back-to-school-stem/preview-1.png" alt="Watermarked Back to School STEM bundle classroom-use preview" loading="lazy" />
          <img src="../assets/products/back-to-school-stem/preview-2.png" alt="Watermarked overview showing activities included in the bundle" loading="lazy" />
          <img src="../assets/products/back-to-school-stem/preview-3.png" alt="Watermarked print-and-go worksheet preview" loading="lazy" />
        </div>
      </div>

      <div class="product-detail-content reveal">
        <div class="product-badges product-badges--static">
          <span class="product-badge">NEW</span>
          <span class="product-badge">GRADES 3–6</span>
          <span class="product-badge">PRINTABLE PDF</span>
        </div>
        <h1>Back to School STEM &amp; Technology Activity Bundle</h1>
        <p class="hero-subtitle">Kick off the year with engaging STEM and technology activities that help students connect, explore, sequence, debug, and design.</p>
        <div class="product-facts">
          <span>9 Activities</span><span>10 pages</span><span>US Letter 8.5×11</span>
        </div>

        <div class="product-practice-box">
          <h2>Students Practice</h2>
          <ul class="check-list two-column-list">
            <li>STEM connections</li>
            <li>Technology literacy</li>
            <li>Algorithms &amp; sequencing</li>
            <li>Debugging</li>
            <li>Critical thinking</li>
            <li>Engineering design</li>
          </ul>
        </div>

        <aside class="purchase-box">
          <p class="product-price">$3.99</p>
          <p>One-time marketplace purchase</p>
          <div class="purchase-links" data-purchase-links="back-to-school-stem"></div>
          <p class="future-direct-note">Direct CJ STEM Lab checkout can be added here later without changing this product page.</p>
        </aside>
      </div>
    </section>

    <section class="section product-info-grid">
      <div class="product-info-card reveal">
        <p class="eyebrow">What’s Included</p>
        <h2>9 student activities</h2>
        <ul class="mini-list">
          <li>STEM About Me</li>
          <li>Where Is STEM Around Us?</li>
          <li>Technology Around Me</li>
          <li>Is It Technology?</li>
          <li>My Morning Algorithm</li>
          <li>How Did You Get to School?</li>
          <li>PB&amp;J Algorithm Challenge</li>
          <li>Debug the PB&amp;J!</li>
          <li>Design a Better School</li>
        </ul>
      </div>
      <div class="product-info-card reveal">
        <p class="eyebrow">Good For</p>
        <h2>Flexible first-week use</h2>
        <ul class="mini-list">
          <li>First week of school</li>
          <li>STEM or technology class</li>
          <li>Morning work</li>
          <li>Early finishers</li>
          <li>Independent practice</li>
        </ul>
      </div>
    </section>

    <section class="section related-resources-section soft-section">
      <div class="section-heading reveal"><p class="eyebrow">Related Resources</p><h2>Keep exploring CJ STEM Lab.</h2></div>
      <a class="related-resource-card reveal" href="computer-science-stem-posters.html">
        <strong>Computer Science &amp; STEM Poster Bundle</strong>
        <span>13 classroom posters</span>
      </a>
    </section>
  </main>

  <button class="back-to-top" aria-label="Back to top">↑</button>
  <footer class="site-footer">
    <div class="footer-brand-block">
      <a href="../index.html" class="logo footer-brand"><span class="logo-mark">CJ</span><span class="logo-text"><strong>CJ STEM Lab</strong><small>Build it. Code it. Create it.</small></span></a>
      <p>STEM, coding, design, and classroom-ready resources for curious learners.</p>
    </div>
    <div class="footer-links" aria-label="Footer navigation">
      <a href="../build-lab.html">Build Lab</a><a href="../code-lab.html">Code Lab</a><a href="../create-lab.html">Create Lab</a><a href="../student-zone.html">Student Zone</a><a href="../resources.html">Shop &amp; Resources</a><a href="../about.html">About</a><a href="../contact.html">Contact</a>
    </div>
    <div class="footer-social" aria-label="Social links"><span>TikTok</span></div>
    <p class="footer-copy">© <span id="year"></span> CJ STEM Lab by Ms. CJ. All rights reserved.</p>
  </footer>

  <script src="../products.js"></script>
  <script src="../script.js"></script>
</body>
</html>
```

- [ ] **Step 5: Add shared product-detail styles**

```css
.product-detail-hero {
  display: grid;
  grid-template-columns: minmax(300px, 0.9fr) minmax(0, 1.1fr);
  gap: 2.5rem;
  align-items: start;
}

.product-gallery,
.product-detail-content,
.product-info-card,
.purchase-box {
  border: 2px solid var(--navy);
  border-radius: var(--radius-lg);
  background: #ffffff;
  box-shadow: 6px 6px 0 rgba(23, 56, 95, 0.1);
}

.product-gallery,
.product-detail-content {
  padding: 1.25rem;
}

.product-main-image {
  overflow: hidden;
  border: 2px solid var(--navy);
  border-radius: 20px;
  background: var(--bg-warm);
}

.product-thumbnails {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 0.65rem;
  margin-top: 0.8rem;
}

.product-thumbnails img {
  aspect-ratio: 4 / 3;
  width: 100%;
  object-fit: cover;
  border: 2px solid var(--border-strong);
  border-radius: 14px;
}

.product-badges--static {
  position: static;
  margin-bottom: 1rem;
}

.product-facts {
  display: flex;
  flex-wrap: wrap;
  gap: 0.6rem;
  margin: 1rem 0;
}

.product-facts span {
  padding: 0.5rem 0.75rem;
  border: 2px solid var(--border-strong);
  border-radius: 999px;
  background: var(--bg-soft);
  color: var(--navy);
  font-weight: 800;
}

.product-practice-box,
.purchase-box {
  margin-top: 1.2rem;
  padding: 1.2rem;
}

.two-column-list {
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.purchase-links {
  display: grid;
  gap: 0.7rem;
  margin-top: 0.8rem;
}

.marketplace-btn--etsy { background: var(--orange); color: #ffffff; border-color: var(--navy); }
.marketplace-btn--tpt { background: var(--green); color: var(--navy-deep); border-color: var(--navy); }
.purchase-note,
.future-direct-note { font-size: 0.9rem; }

.product-info-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 1.2rem;
}

.product-info-card { padding: 1.5rem; }
.related-resource-card {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  width: min(100%, 520px);
  padding: 1.25rem;
  border: 2px solid var(--purple);
  border-radius: 20px;
  background: #ffffff;
  text-decoration: none;
  box-shadow: 5px 5px 0 rgba(125, 105, 200, 0.16);
}
```

- [ ] **Step 6: Run tests and commit the product page**

```bash
python3 -m unittest tests.test_static_site -v
node --check products.js
node --check script.js
git add products/back-to-school-stem.html assets/products/back-to-school-stem style.css tests/test_static_site.py
git commit -m "feat: add back to school STEM product page"
```

---

### Task 7: Build the 13-poster product page from the real poster set

**Files:**
- Create: `products/computer-science-stem-posters.html`
- Create binary assets under: `assets/products/computer-science-stem-posters/`
- Modify: `tests/test_static_site.py`

**Interfaces:**
- Consumes: product id `computer-science-stem-posters`, real source PDF titled `Pastel_Pop_STEM_Posters_Legal.pdf`
- Produces: stable internal URL `products/computer-science-stem-posters.html`

- [ ] **Step 1: Add failing poster-page tests**

```python
    def test_poster_product_page_exists_and_is_complete(self):
        html = read_text("products/computer-science-stem-posters.html")
        self.assertIn("Computer Science &amp; STEM Poster Bundle", html)
        self.assertIn("13 posters", html)
        self.assertIn("8.5×11", html)
        self.assertIn("8.5×14", html)
        self.assertIn("11×17", html)
        self.assertIn('data-purchase-links="computer-science-stem-posters"', html)
        self.assertIn("Poster Topics", html)
        self.assertIn("Related Resources", html)

    def test_poster_product_assets_are_referenced(self):
        html = read_text("products/computer-science-stem-posters.html")
        for image in ["cover.png", "preview-1.png", "preview-2.png", "preview-3.png"]:
            with self.subTest(image=image):
                self.assertIn(f'../assets/products/computer-science-stem-posters/{image}', html)
```

- [ ] **Step 2: Run the tests to verify they fail**

```bash
python3 -m unittest tests.test_static_site.StaticSiteBaselineTests.test_poster_product_page_exists_and_is_complete tests.test_static_site.StaticSiteBaselineTests.test_poster_product_assets_are_referenced -v
```

Expected: FAIL because the poster detail page/assets do not exist.

- [ ] **Step 3: Materialize the real 13-page poster PDF and render web previews**

Use the existing File Library asset titled exactly `Pastel_Pop_STEM_Posters_Legal.pdf`. Confirm it has 13 pages before creating thumbnails. Render page 1 as `cover.png`, page 2 as `preview-1.png`, page 7 as `preview-2.png`, and page 9 as `preview-3.png` at a web-friendly width of roughly 1400 px.

Expected page mapping:

```text
cover.png    -> page 1: The Engineering Design Process
preview-1.png -> page 2: Computational Thinking
preview-2.png -> page 7: AI Literacy
preview-3.png -> page 9: HTML • CSS • JavaScript
```

If the execution environment cannot access the File Library bytes directly, stop this task and request that exact PDF upload. Do not substitute the moodboard mockup or fabricate a poster preview.

- [ ] **Step 4: Create the poster product page using the shared product-detail components**

Use the same header/footer structure and relative paths as Task 6. The product-specific main content must include this exact structure:

```html
<section class="section product-detail-hero">
  <div class="product-gallery reveal">
    <div class="product-main-image">
      <img src="../assets/products/computer-science-stem-posters/cover.png" alt="Engineering Design Process poster from the CJ STEM Lab Computer Science and STEM poster bundle" />
    </div>
    <div class="product-thumbnails" aria-label="Poster preview images">
      <img src="../assets/products/computer-science-stem-posters/preview-1.png" alt="Computational Thinking poster preview" loading="lazy" />
      <img src="../assets/products/computer-science-stem-posters/preview-2.png" alt="AI Literacy poster preview" loading="lazy" />
      <img src="../assets/products/computer-science-stem-posters/preview-3.png" alt="HTML CSS JavaScript poster preview" loading="lazy" />
    </div>
  </div>

  <div class="product-detail-content reveal">
    <div class="product-badges product-badges--static">
      <span class="product-badge">13 POSTERS</span>
      <span class="product-badge">PRINTABLE PDF</span>
      <span class="product-badge">MIDDLE SCHOOL</span>
    </div>
    <h1>Computer Science &amp; STEM Poster Bundle</h1>
    <p class="hero-subtitle">A classroom-ready visual set for core STEM and Computer Science concepts, designed for display, reference, and discussion.</p>
    <div class="product-facts">
      <span>13 posters</span><span>8.5×11</span><span>8.5×14</span><span>11×17</span>
    </div>

    <aside class="purchase-box">
      <p>Choose the marketplace listing that matches the print size you want when verified links are available.</p>
      <div class="purchase-links" data-purchase-links="computer-science-stem-posters"></div>
      <p class="future-direct-note">Direct CJ STEM Lab checkout and size selection can replace this marketplace panel later.</p>
    </aside>
  </div>
</section>

<section class="section product-info-grid">
  <div class="product-info-card reveal">
    <p class="eyebrow">Poster Topics</p>
    <h2>13 classroom visuals</h2>
    <ul class="mini-list">
      <li>The Engineering Design Process</li>
      <li>Computational Thinking</li>
      <li>Debugging 101</li>
      <li>Hardware vs. Software</li>
      <li>How Computers Handle Data</li>
      <li>Internet ≠ Web</li>
      <li>AI Literacy</li>
      <li>Your Digital Footprint</li>
      <li>HTML • CSS • JavaScript</li>
      <li>Binary Basics</li>
      <li>Cybersecurity Basics</li>
      <li>What Is an Algorithm?</li>
      <li>STEM Careers</li>
    </ul>
  </div>
  <div class="product-info-card reveal">
    <p class="eyebrow">Print Options</p>
    <h2>Choose the size that fits your space.</h2>
    <ul class="mini-list">
      <li>8.5×11 — standard letter</li>
      <li>8.5×14 — legal</li>
      <li>11×17 — tabloid</li>
    </ul>
  </div>
</section>

<section class="section related-resources-section soft-section">
  <div class="section-heading reveal"><p class="eyebrow">Related Resources</p><h2>Pair your classroom visuals with student activities.</h2></div>
  <a class="related-resource-card reveal" href="back-to-school-stem.html">
    <strong>Back to School STEM &amp; Technology Activity Bundle</strong>
    <span>Grades 3–6 • 9 activities</span>
  </a>
</section>
```

- [ ] **Step 5: Run tests and commit the poster page**

```bash
python3 -m unittest tests.test_static_site -v
git add products/computer-science-stem-posters.html assets/products/computer-science-stem-posters tests/test_static_site.py
git commit -m "feat: add computer science STEM poster product page"
```

---

### Task 8: Verify purchase-link safety, accessibility, responsive behavior, and deployment readiness

**Files:**
- Modify: `tests/test_static_site.py`
- Modify as required by failures: `style.css`, `script.js`, affected HTML pages, `products.js`

**Interfaces:**
- Consumes: all work from Tasks 1–7
- Produces: final tested static site ready for GitHub Pages deployment

- [ ] **Step 1: Add final structural safety tests**

```python
    def test_no_empty_anchor_hrefs(self):
        html_files = PRIMARY_PAGES + [
            "products/back-to-school-stem.html",
            "products/computer-science-stem-posters.html",
        ]
        for page in html_files:
            html = read_text(page)
            with self.subTest(page=page):
                self.assertNotIn('href=""', html)

    def test_product_pages_use_correct_relative_shared_assets(self):
        for page in [
            "products/back-to-school-stem.html",
            "products/computer-science-stem-posters.html",
        ]:
            html = read_text(page)
            with self.subTest(page=page):
                self.assertIn('href="../style.css"', html)
                self.assertIn('src="../products.js"', html)
                self.assertIn('src="../script.js"', html)

    def test_product_images_have_alt_text(self):
        for page in [
            "products/back-to-school-stem.html",
            "products/computer-science-stem-posters.html",
        ]:
            html = read_text(page)
            self.assertNotIn("<img src=", html.replace(' alt="', ' data-alt-present="'))

    def test_styles_keep_focus_and_reduced_motion_rules(self):
        css = read_text("style.css")
        self.assertIn(":focus-visible", css)
        self.assertIn("@media (prefers-reduced-motion: reduce)", css)

    def test_catalog_does_not_contain_unverified_fake_marketplace_urls(self):
        catalog = read_text("products.js")
        self.assertNotIn("etsy.com/search", catalog)
        self.assertNotIn("teacherspayteachers.com/Browse", catalog)
```

For the image-alt test, if the string approach proves too brittle after formatting, replace it with a small `html.parser.HTMLParser` helper rather than weakening the requirement.

- [ ] **Step 2: Run the complete automated suite**

```bash
python3 -m unittest tests.test_static_site -v
node --check products.js
node --check script.js
```

Expected: all tests pass and JavaScript syntax checks exit 0 when Node is available.

- [ ] **Step 3: Add/confirm responsive rules for product and footer layouts**

Ensure these rules exist after the current responsive blocks:

```css
@media (max-width: 980px) {
  .product-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .product-detail-hero,
  .product-info-grid {
    grid-template-columns: 1fr;
  }

  .site-footer {
    grid-template-columns: 1fr 1fr;
  }

  .footer-copy {
    grid-column: 1 / -1;
  }
}

@media (max-width: 640px) {
  .product-grid,
  .product-info-grid,
  .two-column-list,
  .site-footer {
    grid-template-columns: 1fr;
  }

  .product-thumbnails {
    grid-template-columns: 1fr;
  }

  .product-thumbnails img {
    aspect-ratio: auto;
  }

  .freebies-strip {
    display: grid;
  }

  .brand-hero-art {
    min-height: 330px;
  }

  .hero-doodle {
    opacity: 0.45;
    transform: scale(0.8);
  }

  .footer-copy {
    grid-column: 1;
  }
}
```

Keep the existing `@media (prefers-reduced-motion: reduce)` block intact.

- [ ] **Step 4: Start a local static server for manual verification**

```bash
python3 -m http.server 8000
```

Open:

```text
http://localhost:8000/
http://localhost:8000/resources.html
http://localhost:8000/products/back-to-school-stem.html
http://localhost:8000/products/computer-science-stem-posters.html
```

Verify at approximately 375 px, 768 px, and 1440 px viewport widths:

```text
- sticky navigation remains usable
- mobile menu opens, closes, and closes with Escape
- Shop & Resources is visually emphasized
- hero does not overflow
- product cards remain readable and clickable
- filters show the expected subset and Free shows an intentional empty grid
- product-detail image galleries do not create horizontal scroll
- all internal links resolve under the GitHub Pages repository subpath
- back-to-top still works
- reveal animation does not hide content when reduced motion is enabled
- no browser console errors
```

- [ ] **Step 5: Verify marketplace URLs before enabling purchase buttons**

Inspect `products.js`.

For each marketplace URL that has been independently confirmed from the user's actual listing, set the exact URL:

```javascript
etsyUrl: "https://www.etsy.com/listing/<verified-listing-id>/<verified-slug>",
tptUrl: "https://www.teacherspayteachers.com/Product/<verified-product-slug-and-id>"
```

The strings above describe the required URL shapes only; do **not** literally commit angle-bracket values. If the exact listing URL is not available, leave that field as `""`; `renderPurchaseLinks()` must omit that button and show the verification note instead.

- [ ] **Step 6: Re-run automated checks after any final fixes**

```bash
python3 -m unittest tests.test_static_site -v
node --check products.js
node --check script.js
```

Expected: all tests pass.

- [ ] **Step 7: Commit final responsive/accessibility fixes**

```bash
git add style.css script.js products.js index.html resources.html build-lab.html code-lab.html create-lab.html student-zone.html about.html contact.html products tests/test_static_site.py
git commit -m "fix: polish responsive shop and accessibility"
```

- [ ] **Step 8: Final repository status check**

```bash
git status --short
git log --oneline -8
```

Expected: working tree clean; recent commits show the incremental test/catalog/brand/home/shop/product/polish sequence.

---

## Self-Review Checklist

Before execution is considered complete, confirm the plan covers every approved spec requirement:

- Global balanced brand refresh: Tasks 3, 4, 8
- Playful/bold product cards: Task 5
- Playful/bold product pages: Tasks 6, 7
- `Shop & Resources` navigation: Task 3
- Real homepage products: Tasks 2, 4, 6, 7
- Active Shop & Resources catalog: Task 5
- Internal product-detail flow: Tasks 2, 5, 6, 7
- Conditional verified Etsy/TPT purchase buttons: Tasks 2, 6, 7, 8
- Back to School grades 3–6 / 10 pages / 9 activities: Tasks 2 and 6
- Real 13-poster set and three print sizes: Tasks 2 and 7
- Free-resources area without inventing a free product: Task 5
- Future direct checkout/membership-compatible structure: Tasks 2, 6, 7
- GitHub Pages-safe relative paths: Tasks 6, 7, 8
- Accessibility/reduced motion/mobile behavior: Tasks 1, 3, 8
- No framework/build-tool migration: Global Constraints
