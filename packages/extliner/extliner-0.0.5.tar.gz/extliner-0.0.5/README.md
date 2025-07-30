# 📦 extliner

**extliner** is a lightweight Python package that recursively counts lines in files — distinguishing between total lines and non-empty lines — grouped by file extension. It's perfect for analyzing codebases, writing statistics, or cleaning up documentation-heavy directories.

---

## 🚀 Features

- 📂 Recursive directory scanning
- 🧮 Counts:
  - Total lines (with whitespace)
  - Non-empty lines (ignores blank lines)
- 🔠 Groups results by file extension (`.py`, `.js`, `NO_EXT`, etc.)
- 🚫 Support for ignoring specific extensions or folders
- 📊 Output formats:
  - Pretty CLI table
  - JSON / CSV / Markdown exports
- 🧩 Clean, extensible class-based design
- 🧪 Fully tested with `unittest`
- 🔧 CLI and Python API support

---

## 📥 Installation

Install via pip:

```bash
pip install extliner
```

Or install locally for development:

```bash
git clone https://github.com/extliner/extliner.git
cd extliner
pip install -e .
```

---

## ⚙️ CLI Usage

### ✅ Basic

```bash
extliner -d <directory_path>
```

### 🔍 Ignoring Extensions

```bash
extliner -d ./myproject --ignore .md .log
```

### Ignoring Folders

```bash
extliner -d ./myproject --folders .venv __pycache__
```

### 🧾 Output Example

```
+-------------+---------------+------------------+---------+--------------+
| Extension   |   With Spaces |   Without Spaces |   Files | % of Total   |
+=============+===============+==================+=========+==============+
| .py         |           443 |              362 |       7 | 32.15%       |
+-------------+---------------+------------------+---------+--------------+
| no_ext      |           361 |              287 |       8 | 26.20%       |
+-------------+---------------+------------------+---------+--------------+
| .pyc        |           151 |              125 |       3 | 10.96%       |
+-------------+---------------+------------------+---------+--------------+
```

---
## 🧱 Python API

### ✅ Count Lines Programmatically

```python
from extliner.main import LineCounter
from pathlib import Path

counter = LineCounter(ignore_extensions=[".log", ".json"])
result = counter.count_lines(Path("./your_directory"))

# Output as JSON
print(counter.to_json(result))

# Output as Markdown
print(counter.to_markdown(result))

# Output as CSV
print(counter.to_csv(result))
```

---

## 🛠️ Configuration Options

| Flag        | Description                       | Example                       | Optioal/Required |
| ----------- | --------------------------------- | ----------------------------- | ---------------- |
| `-d`        | Directory to scan      | `-d ./src`                    |  Required         |
| `--ignore`  | File extensions to ignore         | `--ignore .log .md .json`     | Optional         |
| `--folders` | Folder names to ignore | `--folders .venv __pycache__` | Optional         |

---

## 📂 Supported Formats

| Output Method       | Description            |
| ------------------- | ---------------------- |
| `to_json(data)`     | Returns JSON string    |
| `to_csv(data)`      | Returns CSV string     |
| `to_markdown(data)` | Returns Markdown table |

---

## ✅ Testing

To run tests:

```bash
python -m unittest discover tests
```

Or using `pytest` (if installed):

```bash
pytest
```

---

## 📄 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

Made with ❤️ by [Deepak Raj](https://github.com/extliner)

