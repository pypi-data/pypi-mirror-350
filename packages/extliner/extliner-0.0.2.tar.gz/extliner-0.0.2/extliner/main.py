import os
import json
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Optional


class LineCounter:
    def __init__(self, ignore_extensions: Optional[List[str]] = None, ignore_folder: Optional[List[str]] = None, encoding: str = "utf-8"):
        self.encoding = encoding
        self.ignore_folder = set(ignore_folder or [])
        self.ignore_extensions = set(ignore_extensions or [])
        self.with_spaces: Dict[str, int] = defaultdict(int)
        self.without_spaces: Dict[str, int] = defaultdict(int)
        self.file_count: Dict[str, int] = defaultdict(int)

    def count_lines(self, directory: Path) -> Dict[str, Dict[str, int]]:
        directory = Path(directory)
        if not directory.is_dir():
            raise ValueError(f"{directory} is not a valid directory")
        
        for root, dirs, files in os.walk(directory):
            # Remove ignored folders from traversal
            dirs[:] = [d for d in dirs if d not in self.ignore_folder]
            for file in files:
                filepath = Path(root) / file
                ext = (filepath.suffix or "NO_EXT").lower()

                if ext in self.ignore_extensions:
                    continue

                try:
                    with open(filepath, "r", encoding=self.encoding, errors="ignore") as f:
                        lines = f.readlines()
                        self.file_count[ext] += 1
                        self.with_spaces[ext] += len(lines)
                        self.without_spaces[ext] += sum(1 for line in lines if line.strip())
                except Exception as e:
                    print(f"Error reading {filepath}: {e}")

        return self._build_result()

    def _build_result(self) -> Dict[str, Dict[str, int]]:
        return {
            ext: {
                "with_spaces": self.with_spaces[ext],
                "without_spaces": self.without_spaces[ext],
                "file_count": self.file_count[ext],
            }
            for ext in sorted(set(self.with_spaces) | set(self.without_spaces))
        }

    @staticmethod
    def to_json(data: Dict) -> str:
        return json.dumps(data, indent=2)
    
    @staticmethod
    def to_csv(data: Dict) -> str:
        import csv
        from io import StringIO

        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(["Extension", "With Spaces", "Without Spaces", "File Count"])

        for ext, counts in data.items():
            writer.writerow([ext, counts["with_spaces"], counts["without_spaces"], counts["file_count"]])

        return output.getvalue()
        
    @staticmethod
    def to_markdown(data: Dict) -> str:
        output = "| Extension | With Spaces | Without Spaces | File Count |\n"
        output += "|-----------|-------------|----------------|------------|\n"
        for ext, counts in data.items():
            output += f"| {ext} | {counts['with_spaces']} | {counts['without_spaces']} | {counts['file_count']} |\n"

        return output
