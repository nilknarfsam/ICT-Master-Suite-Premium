import os
import sys
import time
import traceback

from src.shared.startup_profiler import mark as startup_mark


def _crash_log_path() -> str:
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "crash_log.txt")


def _append_crash_log(title: str, detail: str):
    with open(_crash_log_path(), "a", encoding="utf-8") as f:
        f.write(f"\n[{time.strftime('%Y-%m-%d %H:%M:%S')}] {title}\n{detail}\n")


def main():
    start_ts = time.perf_counter()
    try:
        startup_mark("run_desktop: inicio")
        startup_mark("run_desktop: antes importar ui_main")
        from src.app_desktop.ui_main import main as run_ui_main
        startup_mark("run_desktop: depois importar ui_main")
        exit_code = run_ui_main()
        elapsed = time.perf_counter() - start_ts

        # Se encerrar rápido demais, registra diagnóstico para facilitar suporte local.
        if elapsed < 1.0:
            _append_crash_log(
                "ENCERRAMENTO RAPIDO DO RUNNER",
                f"run_desktop.py terminou em {elapsed:.3f}s com exit_code={exit_code!r}.",
            )
        return exit_code if isinstance(exit_code, int) else 0
    except Exception:
        _append_crash_log("ERRO CRITICO NO RUNNER", traceback.format_exc())
        raise


if __name__ == "__main__":
    sys.exit(main())
