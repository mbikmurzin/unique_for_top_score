# Уники подписчиков TopScore

Streamlit-приложение собирает публичные таблицы SaleBot, объединяет их столбцы и создаёт Excel с уникальными подписчиками.

## Логика

- Учебный год 26: март 2026 года.
- Учебный год 27: апрель 2026 — апрель 2027 года.
- Группа уникальности: `client_id + учебный год`.
- В группе сохраняется самая ранняя запись по `current_date`, затем `current_time`.
- При полном совпадении сохраняется строка, которая была раньше в списке таблиц и исходном CSV.
- Воронка, UTM, `tag` и `tamtam_user_id` на выбор строки не влияют.

Приложение использует публичный CSV-экспорт SaleBot. API-ключи, секреты и вход в SaleBot не нужны.

## Локальный запуск

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

## Проверка

```bash
python -m pip install pytest
pytest -q
```

## Streamlit Community Cloud

- Repository: `mbikmurzin/unique_for_top_score`
- Branch: `main`
- Main file: `streamlit_app.py` (также поддерживается `app.py`)
- App URL: `https://uniquefortopscore1.streamlit.app`
