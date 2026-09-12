from pathlib import Path
from html.parser import HTMLParser
import unittest

ROOT = Path(__file__).resolve().parents[1]
PUBLIC_PAGES = [
    "index.html",
    "curriculum.html",
    "teachers.html",
    "schools.html",
    "pilot.html",
    "resources.html",
    "about.html",
    "teacher-hub.html",
]
PRODUCT_PAGES = [
    "products/back-to-school-stem.html",
    "products/computer-science-stem-posters.html",
]
PAGES = [*PUBLIC_PAGES, *PRODUCT_PAGES]
PRIMARY_NAV_HREFS = [
    "curriculum.html",
    "teachers.html",
    "schools.html",
    "pilot.html",
    "resources.html",
    "about.html",
    "teacher-hub.html",
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
    def test_primary_site_files_exist(self):
        for path in ["brand.css", "style.css", "script.js", "products.js", *PAGES]:
            with self.subTest(path=path):
                self.assertTrue((ROOT / path).is_file())

    def test_homepage_uses_curriculum_platform_story(self):
        html = read_text("index.html")
        markers = [
            'id="home-hero"',
            'id="implementation-gap"',
            'id="course-pathways"',
            'id="teacher-system"',
            'id="learning-modes"',
            'id="district-readiness"',
            'id="pilot-preview"',
            'id="founder-preview"',
            'id="resource-preview"',
            'id="home-cta"',
        ]
        positions = [html.index(marker) for marker in markers]
        self.assertEqual(positions, sorted(positions))
        self.assertIn('href="curriculum.html"', html)
        self.assertIn('href="pilot.html"', html)
        self.assertIn("Grades 6–8", html)
        self.assertIn("Teacher Hub", html)
        self.assertNotIn('data-product-grid="featured"', html)

    def test_primary_pages_share_new_navigation(self):
        for page in PUBLIC_PAGES:
            html = read_text(page)
            with self.subTest(page=page):
                for href in PRIMARY_NAV_HREFS:
                    self.assertIn(f'href="{href}"', html)
                self.assertIn("Sign In", html)

    def test_curriculum_page_contains_three_course_pathways(self):
        html = read_text("curriculum.html")
        self.assertIn("Grade 6 STEM Foundations", html)
        self.assertIn("Grade 7 Computer Literacy &amp; Digital Systems", html)
        self.assertIn("Grade 8 Computer Science Foundations", html)
        self.assertIn("explicit instruction", html.lower())
        self.assertIn("guided practice", html.lower())
        self.assertIn("mapped", html.lower())

    def test_teacher_page_describes_complete_instructional_package(self):
        html = read_text("teachers.html")
        for phrase in [
            "Daily lesson plans",
            "Instructional slides",
            "Assessments",
            "Answer materials",
            "Differentiation",
            "Schedule",
        ]:
            self.assertIn(phrase, html)
        self.assertIn('href="teacher-hub.html"', html)

    def test_schools_page_labels_future_capabilities_as_roadmap(self):
        html = read_text("schools.html")
        self.assertIn("Future roadmap", html)
        self.assertIn("Teacher curriculum hub", html)
        self.assertIn("Interactive student learning", html)
        self.assertIn("District system", html)
        self.assertIn("WCAG 2.1 AA", html)
        self.assertIn("does not collect student data", html)

    def test_pilot_page_is_planned_not_claimed_active(self):
        html = read_text("pilot.html")
        self.assertIn("Planned Pilot", html)
        self.assertIn("5–10", html)
        self.assertIn("2–4 instructional weeks", html)
        self.assertIn("Pilot Interest", html)
        self.assertNotIn("Apply now for an active pilot", html)

    def test_teacher_hub_is_explicit_static_preview_without_password_collection(self):
        html = read_text("teacher-hub.html")
        self.assertIn("Teacher Hub Preview", html)
        self.assertIn("visual concept only", html)
        self.assertIn("Grade 6 STEM Foundations", html)
        self.assertIn("Grade 7 Computer Literacy &amp; Digital Systems", html)
        self.assertIn("Grade 8 Computer Science Foundations", html)
        self.assertNotIn('type="password"', html)
        self.assertNotIn("<form", html.lower())

    def test_resources_page_remains_active_secondary_catalog(self):
        html = read_text("resources.html")
        self.assertIn("Standalone Classroom Resources", html)
        self.assertIn('data-product-grid="shop"', html)
        self.assertNotIn("Digital downloads and resource packs are coming soon.", html)
        for value in ["all", "stem", "computer-science", "classroom-decor", "activities", "free"]:
            self.assertIn(f'data-product-filter="{value}"', html)

    def test_product_catalog_has_two_real_products(self):
        catalog = read_text("products.js")
        self.assertIn('id: "back-to-school-stem"', catalog)
        self.assertIn('id: "computer-science-stem-posters"', catalog)
        self.assertIn('gradeRange: "Grades 3–6"', catalog)
        self.assertIn('details: "10 pages • 9 student activities"', catalog)
        self.assertIn('details: "13 posters • 8.5×11, 8.5×14, and 11×17"', catalog)

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
        for page in PRODUCT_PAGES:
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

    def test_global_script_normalizes_legacy_navigation(self):
        script = read_text("script.js")
        self.assertIn("normalizeGlobalChrome", script)
        self.assertIn('label: "Curriculum"', script)
        self.assertIn('label: "For Teachers"', script)
        self.assertIn('label: "Schools & Districts"', script)
        self.assertIn('label: "Pilot Program"', script)
        self.assertIn('label: "Resources"', script)
        self.assertIn('label: "Sign In"', script)
        self.assertIn("ensureBrandStyles", script)

    def test_reduced_motion_and_responsive_product_rules(self):
        css = read_text("brand.css")
        self.assertIn("@media (max-width: 980px)", css)
        self.assertIn("@media (max-width: 640px)", css)
        self.assertIn("@media (prefers-reduced-motion: reduce)", css)
        self.assertIn(":focus-visible", css)


if __name__ == "__main__":
    unittest.main()
