from src.shared.startup_profiler import mark as startup_mark


def main():
    startup_mark("run_desktop: inicio")
    startup_mark("run_desktop: antes importar ui_main")
    from src.app_desktop.ui_main import main as run_ui_main
    startup_mark("run_desktop: depois importar ui_main")
    run_ui_main()


if __name__ == "__main__":
    main()
