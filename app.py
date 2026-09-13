from __future__ import annotations

import runpy
from pathlib import Path

# Emergency restore: run the preserved pre-mascot polished app exactly as before.
runpy.run_path(str(Path(__file__).with_name("app_core.py")), run_name="__main__")
