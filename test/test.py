from pathlib import Path                # Needed
import sys                              # just
path_root = Path(__file__).parents[1]   # for
sys.path.append(str(path_root))         # tests

import streamlit as st
from st_oauth import st_oauth

st.markdown("## OAuth")

id = st_oauth()

st.markdown(f"## Congratulations {id}")

st.markdown("Just something to show what happens when widgets are updated.")
x = st.slider("x")
st.metric("WOW", value=x)
