import streamlit as st
from math import floor, ceil

from app import App
from app.constants import BUFF_TARGET
from app.utils import (
    create_buffs_dict,
    get_train_modifier,
    change_status,
    add_a_buff,
    delete_a_buff,
    change_buff,
)


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
        attributes_show("Força", (char["attributes"].get("for") + buffs["for"]))
    with c2:
        attributes_show("Destreza", (char["attributes"].get("des") + buffs["des"]))
    with c3:
        attributes_show("Constituição", (char["attributes"].get("con") + buffs["con"]))
    with c4:
        attributes_show("Inteligência", (char["attributes"].get("int") + buffs["int"]))
    with c5:
        attributes_show("Carisma", (char["attributes"].get("car") + buffs["car"]))
    with c6:
        attributes_show("Sabedoria", (char["attributes"].get("sab") + buffs["sab"]))


def render_buff(buff_data: dict):
    st.header(f":blue[{buff_data.get("name")}]")
    st.text_input(
        "Desc:",
        value=buff_data.get("description"),
        key=buff_data.get("key"),
        on_change=change_buff,
        args=(
            st.session_state["file"],
            buff_data.get("key"),
            "description",
            buff_data.get("key"),
        ),
    )
    ub1, ub2 = st.columns([1, 1])
    with ub1:
        st.number_input(
            "Valor",
            step=1,
            key=f"v_{buff_data.get("key")}",
            value=buff_data.get("value"),
            on_change=change_buff,
            args=(
                st.session_state["file"],
                buff_data.get("key"),
                "value",
                f"v_{buff_data.get("key")}",
            ),
        )
        st.button(
            "🗑️ Deletar esse Buff",
            key=f"d_{buff_data.get("key")}",
            width="stretch",
            on_click=delete_a_buff,
            args=(st.session_state["file"], buff_data.get("key")),
        )

    with ub2:
        st.selectbox(
            "Alvo",
            BUFF_TARGET,
            key=f"t_{buff_data.get("key")}",
            index=None,
            placeholder=buff_data.get("target"),
            on_change=change_buff,
            args=(
                st.session_state["file"],
                buff_data.get("key"),
                "target",
                f"t_{buff_data.get("key")}",
            ),
        )
        st.toggle(
            "Ativo?",
            key=f"a_{buff_data.get("key")}",
            value=buff_data.get("is_active"),
            on_change=change_buff,
            args=(
                st.session_state["file"],
                buff_data.get("key"),
                "is_active",
                f"a_{buff_data.get("key")}",
            ),
        )


def render_all_buffs():
    b1, b2, b3 = st.columns([1, 0.1, 1])

    buff_list = char.get("bonuses")

    if buff_list:
        middle = ceil(len(buff_list) / 2)

        with b1:
            for buff in buff_list[0:middle]:
                render_buff(buff)

        with b3:
            for buff in buff_list[middle:]:
                render_buff(buff)


# Setup
app = App(st.session_state["file"])
char = app.load_file()

buffs = create_buffs_dict(st.session_state["file"])

st.header("Buff Tracker 👁️", divider="violet")

render_attributes()

st.header("", divider="violet")

# Main Status setup
col_1, col_2, col_3, col_4, col_5 = st.columns([1, 1, 1, 1, 1])

main_atr = char["atk_atr"]
attack = (
    floor(char.get("level") / 2)
    + char["attributes"][main_atr]
    + buffs[main_atr]
    + buffs["ataque"]
    + get_train_modifier(char.get("level"))
)
defense = (
    10
    + char["attributes"]["des"]
    + buffs["des"]
    + char["status"]["defense"]
    + buffs["defesa"]
)
damage = char["attributes"][main_atr] + buffs["dano"] + buffs[main_atr]

# Render Status
with col_1:
    status_show("Vida", char["status"]["pv"], char["status"]["current_pv"])

with col_2:
    status_show("Mana", char["status"]["pm"], char["status"]["current_pm"])

with col_3:
    status_show("Ataque Final", attack)

with col_4:
    status_show("Defesa Final", defense)

with col_5:
    status_show("Soma Dano", damage)

# Options and buffs
st.header("", divider="red")
col_1, col_2, col_3 = st.columns([1, 1, 1])

with col_1:
    new_name = st.text_input("Criar um novo Buff", placeholder="Nome")
    st.button(
        "Adicionar Buff",
        width="stretch",
        help="To com preguiça demais de fazer modal, ou validação, ent, por obséquio, coloca o nome antes.",
        on_click=add_a_buff,
        args=(st.session_state["file"], new_name),
    )

with col_2:
    hp_value = st.number_input("Alterar sua vida atual", step=1)
    st.button(
        "Aplicar",
        width="stretch",
        help="Aceita valores negativos, e além do maximo para PVT",
        on_click=change_status,
        args=(st.session_state["file"], "current_pv", hp_value),
    )

with col_3:
    mp_value = st.number_input("Alterar sua mana atual", step=1)
    st.button(
        "Aplicar",
        width="stretch",
        help="Aceita valores negativos, e além do maximo para PMT",
        on_click=change_status,
        args=(st.session_state["file"], "current_pm", mp_value),
    )

render_all_buffs()
