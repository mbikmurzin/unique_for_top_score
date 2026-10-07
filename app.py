from __future__ import annotations

from datetime import date
from uuid import uuid4

import streamlit as st

from core import build_unique_workbook, parse_sources


DEFAULT_SOURCES = [
    ("7 материалов", "https://salebot.pro/shared/table/JHB45bhtrRG1qMYpoExqFDF4h-hncNrYcgvtZf3Z7wI"),
    ("Тест на готовность к ЕГЭ", "https://salebot.pro/shared/table/3kR3e9vGKW4WsHsSfLcd3UfljgcEJPVpJKPzoCXuf88"),
    ("Пробные варианты", "https://salebot.pro/shared/table/Y9jj6-B7eQVc-aPjozwLjLh95zCVxqxxgGFkWiJGhxQ"),
    ("Калькулятор поступления", "https://salebot.pro/shared/table/W4pc5dUPavqz4Pi5zfLMngDKmTJtPs5T9UjQggiCfxQ"),
    ("Генератор плана", "https://salebot.pro/shared/table/J45s5XNX5XTf2Z7SWhF7l11LxGUMJ_KzfkgjNq4ahqM"),
    ("Вся теория для сдачи ЕГЭ", "https://salebot.pro/shared/table/ZS-P5fAx7kQh-TOVidgZ6puE-enzAbfU4EkEV4t-0lU"),
    ("Набор для родителя", "https://salebot.pro/shared/table/cPNWh8sBjDli9Y0gR4S8QPRv4BSHgQvg4XwNh0YNikI"),
    ("Книги для сочинений", "https://salebot.pro/shared/table/jGIb_CoS2zXrdYPgZhQIqm1lMgZswALlMKivbkuEVc8"),
    ("Курсы", "https://salebot.pro/shared/table/LyhO3dX29BqjKwIXIn3XrdAUBTKpyGAQJkgFmOZPzTE"),
]


def fresh_source_rows():
    return [
        {"id": uuid4().hex, "name": name, "url": url}
        for name, url in DEFAULT_SOURCES
    ]


def clear_source_widget_state(rows):
    for row in rows:
        st.session_state.pop(f"source_name_{row['id']}", None)
        st.session_state.pop(f"source_url_{row['id']}", None)


st.set_page_config(
    page_title="Уники подписчиков · TopScore",
    page_icon="✦",
    layout="centered",
)

st.markdown(
    """
    <style>
      .stApp { background: #f4f1ea; }
      .block-container { max-width: 920px; padding-top: 2.5rem; }
      h1 { color: #183c35; letter-spacing: -0.04em; }
      div[data-testid="stMetric"] {
        background: white; border: 1px solid #ded8cc; border-radius: 14px; padding: 14px;
      }
      .stButton > button, .stDownloadButton > button {
        border-radius: 10px; font-weight: 700; min-height: 46px;
      }
      .stButton > button[kind="primary"], .stDownloadButton > button {
        background: #226a5a; color: white; border-color: #226a5a;
      }
      .hint {
        padding: 14px 16px; border-radius: 12px; background: #e6eee9;
        border: 1px solid #c7d8d0; color: #294a42; margin: 1rem 0;
      }
      .source-head { color: #61756f; font-size: .82rem; font-weight: 700; }
      div[data-testid="stTextInput"] input { border-radius: 9px; }
      div[data-testid="column"] .stButton > button[kind="secondary"] {
        min-height: 40px; border-color: #d7cec0; color: #8c463e;
      }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Уники подписчиков")
st.caption("Сбор публичных таблиц SaleBot и готовый Excel без дублей")
st.markdown(
    '<div class="hint">Добавляйте воронки отдельными строками. Название попадёт в Excel, '
    "а по публичной ссылке загрузятся данные SaleBot.</div>",
    unsafe_allow_html=True,
)

if "source_rows" not in st.session_state:
    st.session_state["source_rows"] = fresh_source_rows()

st.subheader("Таблицы SaleBot")
header_name, header_url, header_delete = st.columns([3, 7, 0.8])
header_name.markdown('<span class="source-head">Название воронки</span>', unsafe_allow_html=True)
header_url.markdown('<span class="source-head">Публичная ссылка SaleBot</span>', unsafe_allow_html=True)

row_to_delete = None
for row in st.session_state["source_rows"]:
    name_column, url_column, delete_column = st.columns([3, 7, 0.8])
    row["name"] = name_column.text_input(
        "Название воронки",
        value=row["name"],
        key=f"source_name_{row['id']}",
        label_visibility="collapsed",
        placeholder="Например: Генератор плана",
    )
    row["url"] = url_column.text_input(
        "Публичная ссылка SaleBot",
        value=row["url"],
        key=f"source_url_{row['id']}",
        label_visibility="collapsed",
        placeholder="https://salebot.pro/shared/table/…",
    )
    if delete_column.button(
        "×",
        key=f"delete_source_{row['id']}",
        help=f"Удалить «{row['name'] or 'воронку'}»",
        use_container_width=True,
    ):
        row_to_delete = row["id"]

if row_to_delete:
    deleted = [row for row in st.session_state["source_rows"] if row["id"] == row_to_delete]
    clear_source_widget_state(deleted)
    st.session_state["source_rows"] = [
        row for row in st.session_state["source_rows"] if row["id"] != row_to_delete
    ]
    st.session_state.pop("result", None)
    st.rerun()

add_column, reset_column, spacer = st.columns([2.5, 3, 4.5])
if add_column.button("＋ Добавить воронку", use_container_width=True):
    st.session_state["source_rows"].append(
        {"id": uuid4().hex, "name": "", "url": ""}
    )
    st.session_state.pop("result", None)
    st.rerun()
if reset_column.button("Вернуть исходный список", use_container_width=True):
    clear_source_widget_state(st.session_state["source_rows"])
    st.session_state["source_rows"] = fresh_source_rows()
    st.session_state.pop("result", None)
    st.rerun()

with st.expander("Как удаляются дубли"):
    st.markdown(
        """
        - **26 учебный год:** март 2026 года.
        - **27 учебный год:** апрель 2026 — апрель 2027 года.
        - Уникальность определяется по паре **`client_id + учебный год`**.
        - Остаётся запись с самой ранней датой и временем. При полном совпадении — первая строка исходных таблиц.
        - Воронка, UTM, `tag` и `tamtam_user_id` на дедупликацию не влияют.
        """
    )

if st.button("Собрать таблицу", type="primary", use_container_width=True):
    try:
        source_lines = [
            f"{row['name'].strip()} | {row['url'].strip()}"
            for row in st.session_state["source_rows"]
            if row["name"].strip() or row["url"].strip()
        ]
        sources = parse_sources("\n".join(source_lines))
        progress_bar = st.progress(0.0)
        status = st.empty()

        def update_progress(done: int, total: int, message: str) -> None:
            progress_bar.progress(done / total if total else 0.0)
            status.write(message)

        result = build_unique_workbook(sources, progress=update_progress)
        progress_bar.progress(1.0)
        status.success("Готово")
        st.session_state["result"] = result
        st.session_state["filename"] = (
            f"Все_подписчики_уникальные_{date.today().strftime('%d.%m.%Y')}.xlsx"
        )
    except Exception as error:
        st.error(f"Не удалось собрать таблицу: {error}")

if "result" in st.session_state:
    result = st.session_state["result"]
    st.subheader("Результат")
    first, second, third = st.columns(3)
    first.metric("Собрано строк", f"{result.source_rows:,}".replace(",", " "))
    second.metric("Уникальных", f"{result.result_rows:,}".replace(",", " "))
    third.metric("Удалено дублей", f"{result.removed_duplicates:,}".replace(",", " "))
    st.caption(
        f"Учебный год 26: {result.years[26]:,} · "
        f"Учебный год 27: {result.years[27]:,} · "
        f"Столбцов: {len(result.columns)}".replace(",", " ")
    )
    if result.excluded_rows:
        st.warning(f"Пропущено строк вне периодов или без client_id: {result.excluded_rows}")
    with st.expander("Строки по воронкам"):
        for name, count in result.source_counts:
            st.write(f"**{name}:** {count:,}".replace(",", " "))
    st.download_button(
        "Скачать Excel",
        data=result.workbook,
        file_name=st.session_state["filename"],
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True,
    )

st.divider()
st.caption("TopScore · Для работы не нужны API-ключи и вход в SaleBot")
