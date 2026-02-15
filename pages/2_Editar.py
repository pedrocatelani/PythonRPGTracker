import streamlit as st

from app import App
from app.utils import write_changes


# Setup
app = App(st.session_state["file"])
char = app.load_file()
atr_list = ["for", "des", "con", "int", "sab", "car"]

file = st.session_state["file"] if st.session_state["file"] else "generic.json"


st.header("Editar Personagem", divider="orange")
st.write(f"## :orange[{char.get("name")}] no arquivo {file}")

st.write(f"Criado em : {char.get("created")}")
st.write(f"Modificado : {char.get("modified")}")

st.html("<br />")


col_1, col_2, col_3, col_4 = st.columns([0.6, 0.2, 1, 0.2])

with col_1:
    strenght = st.number_input(
        "Força", -5, 15, step=1, value=char["attributes"].get("for"), icon="⚔️"
    )
    dexteriry = st.number_input(
        "Destreza", -5, 15, step=1, value=char["attributes"].get("des"), icon="🥾"
    )
    constitution = st.number_input(
        "Constituição", -5, 15, step=1, value=char["attributes"].get("con"), icon="❤️"
    )
    intelligence = st.number_input(
        "Inteligência", -5, 15, step=1, value=char["attributes"].get("int"), icon="🧠"
    )
    wisdom = st.number_input(
        "Sabedoria", -5, 15, step=1, value=char["attributes"].get("sab"), icon="🧠"
    )
    charisma = st.number_input(
        "Carisma", -5, 15, step=1, value=char["attributes"].get("car"), icon="🫦"
    )

    if st.button("Salvar Atributos"):
        attributes = {
            "for": strenght,
            "des": dexteriry,
            "con": constitution,
            "int": intelligence,
            "car": charisma,
            "sab": wisdom,
        }

        write_changes(file, "attributes", attributes)


with col_3:
    st.text_input(
        "Nome",
        char.get("name"),
        key="char_name",
        on_change=write_changes,
        args=(file, "name", "char_name"),
    )

    st.text_input(
        "Descrição",
        char.get("description"),
        key="char_description",
        on_change=write_changes,
        args=(file, "description", "char_description"),
    )

    ecol_1, ecol_2 = st.columns([1, 1])

    with ecol_1:
        st.selectbox(
            "Atributo chave do Ataque",
            atr_list,
            placeholder=char.get("atk_atr"),
            key="atr_select",
            on_change=write_changes,
            args=(file, "atk_atr", "atr_select"),
        )

    with ecol_2:
        st.number_input(
            "Nível",
            min_value=1,
            max_value=20,
            step=1,
            value=char.get("level"),
            key="level_select",
            on_change=write_changes,
            args=(file, "level", "level_select"),
        )

    st.html("<br />")
    ecol_1, ecol_2 = st.columns([1, 1])

    with ecol_1:
        pv = st.number_input("Vida", step=1)
        defense = st.number_input("Armadura/Escudo", step=1)

    with ecol_2:
        pm = st.number_input("Mana", step=1)
        atack = st.number_input("Bônus Ataque Arma", step=1)

    if st.button("Salvar Status", width="stretch"):
        status = {
            "pv": pv,
            "pvt": 0,
            "current_pv": pv,
            "pm": pm,
            "pmt": 0,
            "current_pm": pm,
            "attack": atack,
            "defense": defense,
            "damage": 0,
        }

        write_changes(file, "status", status)
