import argparse
from pathlib import Path
from tabulate import tabulate

from extliner.main import LineCounter

def main():
    parser = argparse.ArgumentParser(description="Count lines in files by extension.")
    parser.add_argument(
        "-d", "--directory", type=Path, required=True,
        help="Directory to count lines in."
    )
    parser.add_argument(
        "--ignore", nargs="*", default=[],
        help="List of file extensions to ignore (e.g., .log .json)"
    )

    args = parser.parse_args()

    if not args.directory.is_dir():
        print(f"Error: {args.directory} is not a valid directory")
        return

    counter = LineCounter(ignore_extensions=args.ignore)
    result = counter.count_lines(args.directory)

    # Remove extensions with 0 lines
    result = {
        ext: counts for ext, counts in result.items()
        if counts["with_spaces"] > 0 or counts["without_spaces"] > 0
    }

    # Sort result by extension
    result = dict(sorted(result.items()))

    total_with_spaces = sum(counts["with_spaces"] for counts in result.values())
    
    # sort the result by the number of lines with spaces
    result = dict(sorted(result.items(), key=lambda item: item[1]["with_spaces"], reverse=True))

    table = []
    for ext, counts in result.items():
        with_spaces = counts["with_spaces"]
        without_spaces = counts["without_spaces"]
        percent = (with_spaces / total_with_spaces * 100) if total_with_spaces else 0
        table.append([ext, with_spaces, without_spaces, f"{percent:.2f}%"])

    print(tabulate(
        table,
        headers=["Extension", "With Spaces", "Without Spaces", "% of Total"],
        tablefmt="grid"
    ))


if __name__ == "__main__":
    main()
