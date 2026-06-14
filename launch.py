from __future__ import annotations

import traceback
import time
from pathlib import Path


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    log_dir = base_dir / "data"
    log_dir.mkdir(parents=True, exist_ok=True)
    boot_log = log_dir / "boot_error.log"
    trace_log = log_dir / "boot_trace.log"

    def log(message: str) -> None:
        with trace_log.open("a", encoding="utf-8") as f:
            f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {message}\n")

    try:
        log("launch.py start")
        from server import main as server_main
        log("server import ok")

        log("enter server main")
        server_main()
        log("server main returned")
    except SystemExit as exc:
        log(f"system exit: {exc}")
        boot_log.write_text(f"SystemExit: {exc}", encoding="utf-8")
        raise
    except Exception:
        log("launch exception")
        boot_log.write_text(traceback.format_exc(), encoding="utf-8")
        raise


if __name__ == "__main__":
    main()
