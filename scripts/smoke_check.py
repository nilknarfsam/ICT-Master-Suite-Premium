import importlib
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def check_file(path_rel):
    path = ROOT / path_rel
    ok = path.exists()
    status = "ok" if ok else "fail"
    return status, f"arquivo: {path_rel}"


def check_import(module_name, allow_missing_pyqt=False):
    try:
        importlib.import_module(module_name)
        return "ok", f"import: {module_name}"
    except Exception as exc:
        if allow_missing_pyqt and "No module named 'PyQt5'" in str(exc):
            return "warn", f"import: {module_name} (PyQt5 ausente no ambiente)"
        return "fail", f"import: {module_name} ({exc})"


def main():
    checks = [
        check_file("run_desktop.py"),
        check_file("src/app_desktop/ui_main.py"),
        check_file("src/app_desktop/threads.py"),
        check_file("src/app_desktop/legacy_facade.py"),
        check_file("src/app_desktop/style.qss"),
        check_import("src.app_desktop.ui_main", allow_missing_pyqt=True),
        check_import("src.app_desktop.threads", allow_missing_pyqt=True),
        check_import("src.app_desktop.legacy_facade"),
        check_import("src.core.config.config_service"),
        check_import("src.core.database.database_connection"),
        check_import("src.core.auth.auth_service"),
        check_import("src.core.parsers.parser_factory"),
        check_import("src.core.failures.failure_repository"),
        check_import("src.core.wiki.wiki_repository"),
        check_import("src.core.reports.report_service"),
        check_import("src.core.sync.offline_sync_service"),
    ]

    ok_count = 0
    warn_count = 0
    fail_count = 0

    print("=== SMOKE CHECK: DESKTOP PREMIUM ===")
    for result, label in checks:
        if result == "ok":
            print(f"[OK] {label}")
            ok_count += 1
        elif result == "warn":
            print(f"[WARN] {label}")
            warn_count += 1
        else:
            print(f"[FAIL] {label}")
            fail_count += 1

    print("------------------------------------")
    print(f"Total: {len(checks)} | OK: {ok_count} | WARN: {warn_count} | FAIL: {fail_count}")
    if fail_count == 0:
        print("Resultado final: APROVADO")
        return 0

    print("Resultado final: REPROVADO")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
