from __future__ import annotations

import runpy
from pathlib import Path

from src.mascot_patch import render_mascots

# Keep the verified Round 2 app implementation intact in app_core.py and execute
# it on every Streamlit rerun. The mascot layer below is decorative only.
runpy.run_path(str(Path(__file__).with_name("app_core.py")), run_name="__main__")
render_mascots()
