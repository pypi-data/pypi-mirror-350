import unittest
import tempfile
from pathlib import Path
from extliner.main import LineCounter


class TestLineCounter(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.base_path = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def create_file(self, relative_path: str, content: str):
        file_path = self.base_path / relative_path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding="utf-8")

    def test_single_file_with_and_without_spaces(self):
        self.create_file("hello.py", "print('Hello')\n\nprint('World')\n")
        counter = LineCounter()
        result = counter.count_lines(self.base_path)

        self.assertIn(".py", result)
        self.assertEqual(result[".py"]["with_spaces"], 3)
        self.assertEqual(result[".py"]["without_spaces"], 2)
        self.assertEqual(result[".py"]["file_count"], 1)

    def test_multiple_extensions(self):
        self.create_file("a.py", "print('a')\n\n")
        self.create_file("b.js", "console.log('b');\n")
        self.create_file("c.txt", "\n\ntext\n\n")

        counter = LineCounter()
        result = counter.count_lines(self.base_path)

        self.assertEqual(result[".py"]["file_count"], 1)
        self.assertEqual(result[".txt"]["without_spaces"], 1)

    def test_ignore_extensions(self):
        self.create_file("a.py", "code\ncode\n")
        self.create_file("b.txt", "text\ntext\n")

        counter = LineCounter(ignore_extensions=[".txt"])
        result = counter.count_lines(self.base_path)

        self.assertIn(".py", result)
        self.assertNotIn(".txt", result)

    def test_ignore_folder(self):
        self.create_file("visible/script.py", "a\nb\n")
        self.create_file("ignore_me/script.py", "x\ny\n")

        counter = LineCounter(ignore_folder=["ignore_me"])
        result = counter.count_lines(self.base_path)

        self.assertIn(".py", result)
        self.assertEqual(result[".py"]["with_spaces"], 2)  # only visible/script.py counted

    def test_no_extension_file(self):
        self.create_file("README", "line1\nline2\n")
        counter = LineCounter()
        result = counter.count_lines(self.base_path)

        self.assertIn("no_ext", result)
        self.assertEqual(result["no_ext"]["file_count"], 1)

    def test_empty_file(self):
        self.create_file("empty.py", "")
        counter = LineCounter()
        result = counter.count_lines(self.base_path)

        self.assertEqual(result[".py"]["with_spaces"], 0)
        self.assertEqual(result[".py"]["without_spaces"], 0)
        self.assertEqual(result[".py"]["file_count"], 1)

    def test_nested_directories(self):
        self.create_file("nested/dir/file.py", "line\n\nline\n")
        self.create_file("nested/another/file.js", "x\n")

        counter = LineCounter()
        result = counter.count_lines(self.base_path)

        self.assertIn(".py", result)
        self.assertIn(".js", result)
        self.assertEqual(result[".py"]["file_count"], 1)
        self.assertEqual(result[".js"]["file_count"], 1)

    def test_to_json_format(self):
        self.create_file("sample.py", "x = 1\n\ny = 2\n")
        counter = LineCounter()
        data = counter.count_lines(self.base_path)
        json_str = counter.to_json(data)

        self.assertTrue(json_str.startswith("{"))
        self.assertIn('"with_spaces":', json_str)
        self.assertIn('"file_count":', json_str)

    def test_to_markdown_format(self):
        self.create_file("sample.py", "x = 1\ny = 2\n")
        counter = LineCounter()
        data = counter.count_lines(self.base_path)
        md_str = counter.to_markdown(data)

        self.assertIn("| Extension |", md_str)
        self.assertIn("| .py |", md_str)
        self.assertIn("File Count", md_str)

    def test_to_csv_format(self):
        self.create_file("sample.py", "x = 1\ny = 2\n")
        counter = LineCounter()
        data = counter.count_lines(self.base_path)
        csv_str = counter.to_csv(data)

        self.assertIn("Extension,With Spaces,Without Spaces,File Count", csv_str)
        self.assertIn(".py", csv_str)


if __name__ == "__main__":
    unittest.main()
