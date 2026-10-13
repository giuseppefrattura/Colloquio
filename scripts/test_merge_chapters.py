"""Regressioni per la raccolta dei capitoli e degli approfondimenti."""
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from merge_chapters import load_chapters, lower_headings, plain_text


class LoadChaptersTests(unittest.TestCase):
    def setUp(self):
        self.temporary = TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.directory = self.root / "03. Database"
        self.directory.mkdir()

    def write(self, name, content):
        (self.directory / name).write_text(content, encoding="utf-8")

    def test_includes_supplements_after_main_in_alphabetical_order(self):
        self.write("Database.md", "# Database\n\nIntroduzione.")
        self.write("Neo4j.md", "# Neo4j\n\nGrafi.")
        self.write("MongoDB.md", "# MongoDB\n\n## Documenti\n\n```text\n# codice\n```")
        chapters = load_chapters(self.root)
        self.assertEqual(len(chapters), 1)
        number, title, content = chapters[0]
        self.assertEqual((number, title), ("03", "Database"))
        self.assertLess(content.index("# Database"), content.index("## MongoDB"))
        self.assertLess(content.index("## MongoDB"), content.index("## Neo4j"))
        rendered = lower_headings(content)
        self.assertIn("### MongoDB\n", rendered)
        self.assertIn("#### Documenti\n", rendered)
        self.assertIn("```text\n# codice\n```", rendered)
        self.assertIn("Grafi.", plain_text(rendered))

    def test_accepts_single_source_with_different_filename(self):
        self.write("Altro nome.md", "# Titolo\n\nTesto.")
        self.assertEqual(load_chapters(self.root)[0][1], "Titolo")

    def test_rejects_ambiguous_main_source(self):
        self.write("Uno.md", "# Uno")
        self.write("Due.md", "# Due")
        with self.assertRaisesRegex(ValueError, "principale"):
            load_chapters(self.root)

    def test_rejects_empty_chapter_directory(self):
        with self.assertRaises(ValueError):
            load_chapters(self.root)

    def test_rejects_supplement_without_title(self):
        self.write("Database.md", "# Database")
        self.write("MongoDB.md", "Testo senza titolo")
        with self.assertRaisesRegex(ValueError, "MongoDB.md"):
            load_chapters(self.root)


if __name__ == "__main__":
    unittest.main()
