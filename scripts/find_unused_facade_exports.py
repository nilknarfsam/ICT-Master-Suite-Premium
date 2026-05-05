from pathlib import Path
import re


def _read_text(path):
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""


def _extract_exports(legacy_facade_path):
    text = _read_text(legacy_facade_path)
    match = re.search(r"__all__\s*=\s*\[(.*?)\]", text, flags=re.DOTALL)
    if not match:
        return []
    raw = match.group(1)
    return re.findall(r"['\"]([A-Za-z_][A-Za-z0-9_]*)['\"]", raw)


def _find_used_exports(src_dir, exports):
    used = set()
    for file_path in src_dir.rglob("*.py"):
        text = _read_text(file_path)
        if "legacy_facade" not in text:
            continue
        for export in exports:
            if re.search(rf"\b{re.escape(export)}\b", text):
                used.add(export)
    return used


def main():
    root = Path(__file__).resolve().parent.parent
    src_dir = root / "src"
    legacy_facade_path = src_dir / "app_desktop" / "legacy_facade.py"

    exports = _extract_exports(legacy_facade_path)
    used = _find_used_exports(src_dir, exports)
    unused = sorted(set(exports) - used)

    print("=== LEGACY FACADE EXPORT AUDIT ===")
    print(f"total_exports: {len(exports)}")
    print(f"used_exports: {len(used)}")
    print(f"apparently_unused_exports: {len(unused)}")
    print()
    print("exports_usados:")
    for name in sorted(used):
        print(f"- {name}")
    print()
    print("exports_aparentemente_nao_usados:")
    for name in unused:
        print(f"- {name}")


if __name__ == "__main__":
    main()
