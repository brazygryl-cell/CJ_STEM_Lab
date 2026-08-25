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
