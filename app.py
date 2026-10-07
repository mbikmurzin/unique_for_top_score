from __future__ import annotations

from datetime import date

import streamlit as st

from core import build_unique_workbook, parse_sources


DEFAULT_SOURCES = """7 материалов | https://salebot.pro/shared/table/JHB45bhtrRG1qMYpoExqFDF4h-hncNrYcgvtZf3Z7wI
Тест на готовность к ЕГЭ | https://salebot.pro/shared/table/3kR3e9vGKW4WsHsSfLcd3UfljgcEJPVpJKPzoCXuf88
Пробные варианты | https://salebot.pro/shared/table/Y9jj6-B7eQVc-aPjozwLjLh95zCVxqxxgGFkWiJGhxQ
Калькулятор поступления | https://salebot.pro/shared/table/W4pc5dUPavqz4Pi5zfLMngDKmTJtPs5T9UjQggiCfxQ
Генератор плана | https://salebot.pro/shared/table/J45s5XNX5XTf2Z7SWhF7l11LxGUMJ_KzfkgjNq4ahqM
Вся теория для сдачи ЕГЭ | https://salebot.pro/shared/table/ZS-P5fAx7kQh-TOVidgZ6puE-enzAbfU4EkEV4t-0lU
Набор для родителя | https://salebot.pro/shared/table/cPNWh8sBjDli9Y0gR4S8QPRv4BSHgQvg4XwNh0YNikI
Книги для сочинений | https://salebot.pro/shared/table/jGIb_CoS2zXrdYPgZhQIqm1lMgZswALlMKivbkuEVc8
Курсы | https://salebot.pro/shared/table/LyhO3dX29BqjKwIXIn3XrdAUBTKpyGAQJkgFmOZPzTE"""


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
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Уники подписчиков")
st.caption("Сбор публичных таблиц SaleBot и готовый Excel без дублей")
st.markdown(
    '<div class="hint">Одна строка — одна воронка: <b>Название | ссылка</b>. '
    "Можно менять список, удалять старые и добавлять новые таблицы.</div>",
    unsafe_allow_html=True,
)

sources_text = st.text_area(
    "Таблицы SaleBot",
    value=DEFAULT_SOURCES,
    height=330,
    help="Работают публичные ссылки вида https://salebot.pro/shared/table/…",
)

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
        sources = parse_sources(sources_text)
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
