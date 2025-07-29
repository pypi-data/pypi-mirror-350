import os
import json
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Optional


class LineCounter:
    def __init__(self, ignore_extensions: Optional[List[str]] = None):
        self.ignore_extensions = set(ignore_extensions or [])
        self.with_spaces: Dict[str, int] = defaultdict(int)
        self.without_spaces: Dict[str, int] = defaultdict(int)

    def count_lines(self, directory: Path) -> Dict[str, Dict[str, int]]:
        directory = Path(directory)
        if not directory.is_dir():
            raise ValueError(f"{directory} is not a valid directory")

        for root, _, files in os.walk(directory):
            for file in files:
                filepath = Path(root) / file
                ext = filepath.suffix or "NO_EXT"

                if ext in self.ignore_extensions:
                    continue

                try:
                    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                        lines = f.readlines()
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
            }
            for ext in sorted(set(self.with_spaces) | set(self.without_spaces))
        }

    def to_json(self, data: Dict) -> str:
        return json.dumps(data, indent=2)
