from pathlib import Path                # Needed
import sys                              # just
path_root = Path(__file__).parents[1]   # for
sys.path.append(str(path_root))         # tests

import streamlit as st
from st_oauth import st_oauth

st.markdown("## Hello there")

session = st_oauth()

st.markdown("## Welcome")
st.json(st.session_state)
