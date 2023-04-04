from pathlib import Path
import sys
path_root = Path(__file__).parents[1]
sys.path.append(str(path_root))

import streamlit as st
from st_oauth import st_oauth

st.markdown("## OAuth")

id = st_oauth()

st.markdown(f"## Congratulations {id}")

st.markdown("Just something to show what happens when widgets are updated.")
x = st.slider("x")
st.metric("WOW", value=x)
