from __future__ import annotations

import runpy
from pathlib import Path

import streamlit as st

from src.mascot_patch import render_mascots

runpy.run_path(str(Path(__file__).with_name("app_core.py")), run_name="__main__")

st.markdown("<style>.b2a-bot-stage{display:none!important}</style>", unsafe_allow_html=True)
render_mascots()
