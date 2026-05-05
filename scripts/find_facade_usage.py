from pathlib import Path


def main():
    root = Path(__file__).resolve().parent.parent
    src_dir = root / "src"
    target = "legacy_facade"

    matches = []
    for file_path in src_dir.rglob("*.py"):
        try:
            lines = file_path.read_text(encoding="utf-8", errors="ignore").splitlines()
        except OSError:
            continue

        for idx, line in enumerate(lines, start=1):
            if target in line:
                relative = file_path.relative_to(root).as_posix()
                snippet = line.strip()
                matches.append((relative, idx, snippet))

    print("=== LEGACY FACADE USAGE ===")
    print(f"total_matches: {len(matches)}")
    for relative, idx, snippet in matches:
        print(f"{relative}:{idx}: {snippet}")


if __name__ == "__main__":
    main()
