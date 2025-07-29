Here’s a clean and informative `README.md` for your package **`extliner`**:

---

## 📦 extliner

**extliner** is a lightweight Python package that counts lines in files (with and without empty lines) grouped by file extension — perfect for analyzing codebases or text-heavy directories.

---

### 🚀 Features

* 📂 Recursive directory traversal
* 🔍 Counts:

  * Total lines **with** whitespace
  * Total lines **excluding** empty lines
* 🎯 Extension-based grouping (`.py`, `.txt`, `NO_EXT`, etc.)
* 🚫 Option to **ignore specific file extensions**
* 📊 Beautiful **tabulated output**
* 🧩 Easily extensible class-based design
* 🧪 CLI support

---

### 📥 Installation

```bash
pip install extliner
```

(Or if using locally during development:)

```bash
git clone https://github.com/extliner/extliner.git
cd extliner
pip install -e .
```

---

### 🧑‍💻 Usage

#### ✅ CLI

```bash
extliner -d <directory_path> --ignore .log .json
```

#### Example

```bash
extliner -d ./myproject --ignore .md .log
```

#### Output

```
+------------+---------------+-------------------+--------------+
| Extension  | With Spaces   | Without Spaces    | % of Total   |
+------------+---------------+-------------------+--------------+
| .py        | 320           | 280               | 65.31%       |
| .txt       | 170           | 150               | 34.69%       |
+------------+---------------+-------------------+--------------+
```

---

### 🧱 Python API

```python
from linecountx.main import LineCounter
from pathlib import Path

counter = LineCounter(ignore_extensions=[".log", ".json"])
result = counter.count_lines(Path("./your_directory"))

print(counter.to_json(result))
```

---

### ⚙️ Options

| Flag       | Description                  | Example                   |
| ---------- | ---------------------------- | ------------------------- |
| `-d`       | Directory to scan (required) | `-d ./src`                |
| `--ignore` | File extensions to ignore    | `--ignore .log .md .json` |


### 📄 License

MIT License

---

### 👨‍💻 Author

Made with ❤️ by [Deepak Raj](https://github.com/extliner)

