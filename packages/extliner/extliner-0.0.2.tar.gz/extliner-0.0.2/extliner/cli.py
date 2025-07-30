import argparse
from pathlib import Path
from tabulate import tabulate

from extliner.main import LineCounter


def main():
    parser = argparse.ArgumentParser(
        description="📦 Count lines in files grouped by extension (with/without empty lines)."
    )
    parser.add_argument(
        "-d", "--directory", type=Path, required=True,
        help="Input directory to count lines in (default: current directory)"
    )
    parser.add_argument(
        "-i", "--ignore", nargs="*", default=[],
        help="File extensions to ignore (e.g., .log .json)"
    )
    parser.add_argument(
        "-f", "--folders", nargs="*", default=[],
        help="Folder names to ignore (e.g., .venv __pycache__)"
    )
    parser.add_argument(
        "--format", choices=["table", "json", "csv", "md"], default="table",
        help="Output format: table (default), json, csv, or md (markdown)"
    )

    args = parser.parse_args()

    if not args.directory.is_dir():
        print(f"❌ Error: {args.directory} is not a valid directory.")
        return

    counter = LineCounter(
        ignore_extensions=args.ignore,
        ignore_folder=args.folders,
    )
    result = counter.count_lines(args.directory)

    # Remove extensions with 0 lines
    result = {
        ext: counts for ext, counts in result.items()
        if counts["with_spaces"] > 0 or counts["without_spaces"] > 0
    }

    # Sort by line count (with spaces) in descending order
    result = dict(sorted(result.items(), key=lambda item: item[1]["with_spaces"], reverse=True))

    total_with_spaces = sum(counts["with_spaces"] for counts in result.values())

    if args.format == "json":
        print(counter.to_json(result))
    elif args.format == "csv":
        print(counter.to_csv(result))
    elif args.format == "md":
        print(counter.to_markdown(result))
    else:
        # Default: tabular CLI output
        table = []
        for ext, counts in result.items():
            with_spaces = counts["with_spaces"]
            without_spaces = counts["without_spaces"]
            percent = (with_spaces / total_with_spaces * 100) if total_with_spaces else 0
            table.append([ext, with_spaces, without_spaces, counts["file_count"], f"{percent:.2f}%"])

        print(tabulate(
            table,
            headers=["Extension", "With Spaces", "Without Spaces", "Files", "% of Total"],
            tablefmt="grid"
        ))


if __name__ == "__main__":
    main()
