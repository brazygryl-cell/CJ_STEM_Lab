from pathlib import Path
from html.parser import HTMLParser
import unittest

ROOT = Path(__file__).resolve().parents[1]
PAGES = [
    "index.html",
    "resources.html",
    "products/back-to-school-stem.html",
    "products/computer-science-stem-posters.html",
]


def read_text(path):
    return (ROOT / path).read_text(encoding="utf-8")


class ImgAltParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.missing = []

    def handle_starttag(self, tag, attrs):
        if tag != "img":
            return
        data = dict(attrs)
        if not data.get("alt", "").strip():
            self.missing.append(data.get("src", "<unknown>"))


class StaticSiteTests(unittest.TestCase):
    def test_primary_new_files_exist(self):
        for path in ["brand.css", "script.js", "products.js", *PAGES]:
            with self.subTest(path=path):
                self.assertTrue((ROOT / path).is_file())

    def test_product_catalog_has_two_real_products(self):
        catalog = read_text("products.js")
        self.assertIn('id: "back-to-school-stem"', catalog)
        self.assertIn('id: "computer-science-stem-posters"', catalog)
        self.assertIn('gradeRange: "Grades 3–6"', catalog)
        self.assertIn('details: "10 pages • 9 student activities"', catalog)
        self.assertIn('details: "13 posters • 8.5×11, 8.5×14, and 11×17"', catalog)

    def test_homepage_structure(self):
        html = read_text("index.html")
        markers = [
            'id="home-hero"', 'id="labs"', 'id="featured-resources"',
            'id="student-zone-preview"', 'id="audiences"',
            'id="about-preview"', 'id="home-cta"'
        ]
        positions = [html.index(marker) for marker in markers]
        self.assertEqual(positions, sorted(positions))
        self.assertIn('data-product-grid="featured"', html)
        self.assertLess(html.index('src="products.js"'), html.index('src="script.js"'))

    def test_shop_page_is_active_catalog(self):
        html = read_text("resources.html")
        self.assertIn("Resources Built for Teaching, Learning &amp; Creating", html)
        self.assertIn('data-product-grid="shop"', html)
        self.assertNotIn("Digital downloads and resource packs are coming soon.", html)
        for value in ["all", "stem", "computer-science", "classroom-decor", "activities", "free"]:
            self.assertIn(f'data-product-filter="{value}"', html)

    def test_product_pages_have_purchase_mounts_and_related_resources(self):
        back = read_text("products/back-to-school-stem.html")
        posters = read_text("products/computer-science-stem-posters.html")
        self.assertIn('data-purchase-links="back-to-school-stem"', back)
        self.assertIn('data-purchase-links="computer-science-stem-posters"', posters)
        self.assertIn("Related Resources", back)
        self.assertIn("Related Resources", posters)
        self.assertIn("9 student activities", back)
        self.assertIn("13 classroom visuals", posters)

    def test_product_images_exist_and_have_alt_text(self):
        for page in ["products/back-to-school-stem.html", "products/computer-science-stem-posters.html"]:
            parser = ImgAltParser()
            parser.feed(read_text(page))
            self.assertEqual(parser.missing, [], page)

    def test_no_empty_anchor_hrefs(self):
        for page in PAGES:
            with self.subTest(page=page):
                self.assertNotIn('href=""', read_text(page))

    def test_unverified_marketplace_urls_are_not_faked(self):
        catalog = read_text("products.js")
        self.assertNotIn("etsy.com/search", catalog)
        self.assertNotIn("teacherspayteachers.com/Browse", catalog)
        self.assertIn('etsyUrl: ""', catalog)
        self.assertIn('tptUrl: ""', catalog)

    def test_global_script_normalizes_existing_pages(self):
        script = read_text("script.js")
        self.assertIn("normalizeGlobalChrome", script)
        self.assertIn('link.textContent = "Shop & Resources"', script)
        self.assertIn('link.classList.add("nav-shop")', script)
        self.assertIn('link.classList.remove("nav-cta")', script)
        self.assertIn("ensureBrandStyles", script)

    def test_reduced_motion_and_responsive_product_rules(self):
        css = read_text("brand.css")
        self.assertIn("@media (max-width: 980px)", css)
        self.assertIn("@media (max-width: 640px)", css)
        self.assertIn("@media (prefers-reduced-motion: reduce)", css)
        self.assertIn(":focus-visible", css)


if __name__ == "__main__":
    unittest.main()
