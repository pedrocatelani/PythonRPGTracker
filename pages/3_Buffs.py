import streamlit as st

from app import App


# Components
def status_show(name: str, value: int, second_value: int = None):
    st.write(f"### :red[{name}]")
    if not second_value:
        st.write(str(value))
    else:
        st.write(f"{value} / {second_value}")


def attributes_show(name: str, value: int):
    st.write(f"#### :violet[{name}]")
    st.write(str(value))


def render_attributes():
    c1, c2, c3, c4, c5, c6 = st.columns([1, 1, 1, 1, 1, 1])

    with c1:
        attributes_show("Força", char["attributes"].get("for"))
    with c2:
        attributes_show("Destreza", char["attributes"].get("des"))
    with c3:
        attributes_show("Constituição", char["attributes"].get("con"))
    with c4:
        attributes_show("Inteligência", char["attributes"].get("int"))
    with c5:
        attributes_show("Carisma", char["attributes"].get("car"))
    with c6:
        attributes_show("Sabedoria", char["attributes"].get("sab"))


# Setup
app = App(st.session_state["file"])
char = app.load_file()

atack = 0
defense = 0


st.header("Buff Tracker", divider="violet")

render_attributes()

st.header("", divider="violet")

col_1, col_2, col_3, col_4 = st.columns([1, 1, 1, 1])

with col_1:
    status_show("Vida", char["status"]["pv"], char["status"]["current_pv"])

with col_2:
    status_show("Mana", char["status"]["pm"], char["status"]["current_pm"])

with col_3:
    status_show("Ataque Final", atack)

with col_4:
    status_show("Defesa Final", defense)
