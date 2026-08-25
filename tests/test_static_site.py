from html.parser import HTMLParser
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

PRODUCT_PAGES = [
    "products/back-to-school-stem.html",
    "products/computer-science-stem-posters.html",
]


def read_text(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


class ImageAltParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.images = []

    def handle_starttag(self, tag, attrs):
        if tag != "img":
            return
        attributes = dict(attrs)
        self.images.append((attributes.get("src", ""), attributes.get("alt", "")))


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
        self.assertIn("@media (prefers-reduced-motion: reduce)", read_text("theme.css"))

    def test_brand_theme_defines_focus_and_shop_styles(self):
        css = read_text("theme.css")
        self.assertIn(":focus-visible", css)
        self.assertIn(".nav-menu .nav-shop", css)
        self.assertIn(".product-grid", css)
        self.assertIn(".product-detail-hero", css)
        self.assertIn(".site-footer", css)

    def test_product_catalog_defines_real_products(self):
        catalog = read_text("products.js")
        self.assertIn('id: "back-to-school-stem"', catalog)
        self.assertIn('id: "computer-science-stem-posters"', catalog)
        self.assertIn('gradeRange: "Grades 3–6"', catalog)
        self.assertIn('details: "10 pages • 9 student activities"', catalog)
        self.assertIn('details: "13 posters • 8.5×11, 8.5×14, and 11×17"', catalog)
        self.assertIn('thumbnail: "assets/products/back-to-school-stem/cover.webp"', catalog)

    def test_catalog_does_not_contain_fake_marketplace_urls(self):
        catalog = read_text("products.js")
        self.assertNotIn("etsy.com/search", catalog)
        self.assertNotIn("teacherspayteachers.com/Browse", catalog)
        self.assertNotIn("<verified", catalog)

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

    def test_script_normalizes_legacy_navigation_and_loads_theme(self):
        script = read_text("script.js")
        self.assertIn("Shop & Resources", script)
        self.assertIn("nav-shop", script)
        self.assertIn("theme.css", script)
        self.assertIn("product-extras.css", script)

    def test_homepage_has_approved_section_order(self):
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

    def test_homepage_loads_catalog_before_main_script(self):
        html = read_text("index.html")
        self.assertIn('data-product-grid="featured"', html)
        self.assertIn("Shop Resources", html)
        self.assertIn("Explore the Labs", html)
        self.assertLess(html.index('src="products.js"'), html.index('src="script.js"'))

    def test_shop_page_is_active_catalog_not_placeholder(self):
        html = read_text("resources.html")
        self.assertIn("Resources Built for Teaching, Learning &amp; Creating", html)
        self.assertIn('data-product-grid="shop"', html)
        self.assertNotIn("Digital downloads and resource packs are coming soon.", html)
        self.assertLess(html.index('src="products.js"'), html.index('src="script.js"'))

    def test_shop_page_has_required_filters(self):
        html = read_text("resources.html")
        for value in ["all", "stem", "computer-science", "classroom-decor", "activities", "free"]:
            with self.subTest(value=value):
                self.assertIn(f'data-product-filter="{value}"', html)

    def test_back_to_school_product_page_is_complete(self):
        html = read_text("products/back-to-school-stem.html")
        self.assertIn("Back to School STEM &amp; Technology Activity Bundle", html)
        self.assertIn("Grades 3–6", html)
        self.assertIn("10 pages", html)
        self.assertIn("9 student activities", html)
        self.assertIn('data-purchase-links="back-to-school-stem"', html)
        self.assertIn("What’s Included", html)
        self.assertIn("Students Practice", html)
        self.assertIn("Related Resources", html)
        for image in ["cover.webp", "preview-1.webp", "preview-2.webp", "preview-3.webp"]:
            with self.subTest(image=image):
                self.assertIn(f'../assets/products/back-to-school-stem/{image}', html)

    def test_back_to_school_assets_exist(self):
        for image in ["cover.webp", "preview-1.webp", "preview-2.webp", "preview-3.webp"]:
            with self.subTest(image=image):
                self.assertTrue((ROOT / "assets" / "products" / "back-to-school-stem" / image).is_file())

    def test_poster_product_page_matches_current_13_poster_set(self):
        html = read_text("products/computer-science-stem-posters.html")
        self.assertIn("Computer Science &amp; STEM Poster Bundle", html)
        self.assertIn("13 posters", html)
        self.assertIn("8.5×11", html)
        self.assertIn("8.5×14", html)
        self.assertIn("11×17", html)
        self.assertIn('data-purchase-links="computer-science-stem-posters"', html)
        self.assertIn("Poster Topics", html)
        self.assertIn("Related Resources", html)

        topics = [
            "The Engineering Design Process",
            "Computational Thinking",
            "Debugging 101",
            "Hardware vs. Software",
            "How Computers Handle Data",
            "Internet ≠ Web",
            "AI Literacy",
            "Your Digital Footprint",
            "HTML • CSS • JavaScript",
            "Binary Basics",
            "Cybersecurity Basics",
            "What Is an Algorithm?",
            "STEM Careers",
        ]
        for topic in topics:
            with self.subTest(topic=topic):
                self.assertIn(topic, html)

    def test_poster_page_discloses_preview_placeholder(self):
        html = read_text("products/computer-science-stem-posters.html")
        self.assertIn("Exact poster thumbnails will replace this placeholder", html)
        self.assertIn("poster-bundle-placeholder", html)

    def test_product_pages_use_correct_relative_shared_assets(self):
        for page in PRODUCT_PAGES:
            html = read_text(page)
            with self.subTest(page=page):
                self.assertIn('href="../style.css"', html)
                self.assertIn('href="../theme.css"', html)
                self.assertIn('src="../products.js"', html)
                self.assertIn('src="../script.js"', html)

    def test_all_static_images_have_nonempty_alt_text(self):
        for page in PRIMARY_PAGES + PRODUCT_PAGES:
            parser = ImageAltParser()
            parser.feed(read_text(page))
            for src, alt in parser.images:
                with self.subTest(page=page, src=src):
                    self.assertTrue(src)
                    self.assertTrue(alt.strip())

    def test_no_empty_anchor_hrefs(self):
        for page in PRIMARY_PAGES + PRODUCT_PAGES:
            with self.subTest(page=page):
                self.assertNotIn('href=""', read_text(page))

    def test_product_placeholder_styles_exist(self):
        css = read_text("product-extras.css")
        self.assertIn(".product-image-placeholder", css)
        self.assertIn(".poster-bundle-placeholder", css)
        self.assertIn(".poster-topic-grid", css)


if __name__ == "__main__":
    unittest.main()
