                                 Крипто бот
# CryptoBotTrader

Интерактивный крипто-трейдинговый бот и дашборд **(Flask + WebSocket + APScheduler)** с:
- сбором рыночных данных через **ccxt**,
- прогнозированием цен (ARIMA/pmdarima, Statsmodels),
- расчётом «идеального портфеля» (**PyPortfolioOpt**: Max Sharpe / Min Vol / HRP),
- фоновой оркестрацией задач (APScheduler),
- хранением данных в **PostgreSQL** (возможна **TimescaleDB**) или SQLite,
- web-UI (Bootstrap + TradingView), live-обновлениями (**Flask-SocketIO**).

> ⚠️ Отказ от ответственности: это инженерный/исследовательский проект. Не является финансовой рекомендацией. Используйте на свой риск.

---

## Возможности

- **Сбор свечей OHLCV** по символам и таймфреймам (ccxt).
- **Прогнозирование** краткосрочного движения (горизонт H=24..72 баров; лог-доходности).
- **Оценка метрик** (sMAPE/MAE — легко добавить) и кросс-валидация по временным сплитам.
- **Оптимизация портфеля** на основе ожидаемой доходности и ковариации: Max Sharpe, Min Vol, HRP; ограничения по весам (например, 0–30%).
- **Исполнение (paper)**: план ребалансировки и бумажные ордера; хранение ордеров/балансов.
- **Веб-панель**: график TradingView, последние цены, новости (опционально), **виджеты** целевых весов и прогноза `/api/weights`, `/api/forecast`.
- **Экспорт в CSV** можно добавить кнопкой в UI.
- **Миграции БД** через Alembic.

---

## Технологии

- **Backend**: Python 3.12, Flask 3, Flask-SocketIO, eventlet, APScheduler  
- **Data/ML**: pandas, numpy, statsmodels, pmdarima, PyPortfolioOpt  
- **Exchanges**: ccxt  
- **Storage**: SQLAlchemy 2.x, Alembic; PostgreSQL (**рекомендовано**) / SQLite (**быстрый старт**)  
- **UI**: Bootstrap 4.5, TradingView widget, Jinja2  
- **Конфиги**: python-dotenv, Pydantic Settings

---

## Структура проекта



Запустить проект python app.p
запустить веб: python server.py (или PORT=8050 python server.py).

