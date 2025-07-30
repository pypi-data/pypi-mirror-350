import os
import json
import mimetypes
from tqdm import tqdm
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Optional, Tuple, Union
from concurrent.futures import ProcessPoolExecutor, as_completed

def is_text_mimetype(path: str) -> bool:
    mime, _ = mimetypes.guess_type(path)
    return mime is not None and (mime.startswith("text/") or mime == "application/json")

def process_file(filepath: str, encoding: str) -> Optional[Tuple[str, int, int]]:
    ext = (Path(filepath).suffix or "NO_EXT").lower()

    try:
        with open(filepath, "r", encoding=encoding, errors="ignore") as f:
            with_spaces = sum(1 for _ in f)
            f.seek(0)
            without_spaces = sum(1 for line in f if line.strip())
        return ext, with_spaces, without_spaces
    except Exception:
        return None

def scan_files(directory: Path, ignore_folders: set, ignore_exts: set) -> List[str]:
    file_list = []

    def _recursive_scan(path: Path):
        for entry in os.scandir(path):
            entry_path = Path(entry.path)
            if entry.is_dir(follow_symlinks=False):
                if entry_path.name not in ignore_folders:
                    _recursive_scan(entry_path)
            elif entry.is_file(follow_symlinks=False):
                ext = entry_path.suffix.lower() or "NO_EXT"
                if ext not in ignore_exts:
                    if is_text_mimetype(entry_path): # type: ignore
                        file_list.append(str(entry_path))

    _recursive_scan(directory)
    return file_list


class LineCounter:
    def __init__(
        self,
        ignore_extensions: Optional[List[str]] = None,
        ignore_folder: Optional[List[str]] = None,
        encoding: str = "utf-8",
        use_progress: bool = True,
        max_workers: Optional[int] = None,
    ):
        self.encoding = encoding
        self.ignore_folder = set(ignore_folder or [])
        self.ignore_extensions = set(ignore_extensions or [])
        self.with_spaces: Dict[str, int] = defaultdict(int)
        self.without_spaces: Dict[str, int] = defaultdict(int)
        self.file_count: Dict[str, int] = defaultdict(int)
        self.use_progress = use_progress and tqdm is not None
        self.max_workers = max_workers

    def count_lines(self, directory: Union[str, Path]) -> Dict[str, Dict[str, int]]:
        directory = Path(directory)
        if not directory.is_dir():
            raise ValueError(f"{directory} is not a valid directory")

        filepaths = scan_files(directory, self.ignore_folder, self.ignore_extensions)

        with ProcessPoolExecutor(max_workers=self.max_workers) as executor:
            futures = [
                executor.submit(process_file, filepath, self.encoding)
                for filepath in filepaths
            ]
            iterator = as_completed(futures)

            if self.use_progress:
                iterator = tqdm(iterator, total=len(futures), desc="Counting lines")

            for future in iterator:
                result = future.result()
                if result:
                    ext, with_spaces, without_spaces = result
                    self.file_count[ext] += 1
                    self.with_spaces[ext] += with_spaces
                    self.without_spaces[ext] += without_spaces

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
