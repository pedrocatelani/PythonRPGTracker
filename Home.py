import streamlit as st

from app import App

from app.utils import get_character_files


# minor Utils
def change_file():
    st.session_state["file"] = st.session_state.get("char_file")


# Setup
if "file" not in st.session_state:
    st.session_state["file"] = None

app = App(st.session_state["file"])
char = app.load_file()

characters = get_character_files()


st.set_page_config(page_title="Tracker Bonus T20", layout="wide")

st.header(":orange[T20] :red[Helper]", divider="red")
st.write("#### :red[by: @catelanirocha]")

st.selectbox(
    "Selecione seu personagem",
    characters,
    index=None,
    on_change=change_file,
    key="char_file",
)

st.html("<br />")

col_1, col_2 = st.columns([1, 1])

with col_1:
    st.write("### :red[Personagem:]")
    st.write(char.get("name"))
    st.write(f"Nivel {char["level"]}")

with col_2:
    st.write("### :red[Descrição:]")
    st.write(char.get("description"))
