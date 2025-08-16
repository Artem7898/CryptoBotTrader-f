from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime, timedelta
import pandas as pd
import uuid

from ..settings import settings
from ..services import exchange, storage, forecasting, optimizer, execution

def job_sync_candles():
    ex = settings.EXCHANGE_NAME
    for sym in settings.SYMBOLS:
        rows = exchange.fetch_ohlcv(sym, settings.TIMEFRAME, limit=500)
        storage.upsert_candles(ex, sym, settings.TIMEFRAME, rows)
    print("[sync] candles ok", datetime.utcnow())

def job_forecast_and_optimize():
    # 1) соберём историю закрытий
    close_history = {}
    for sym in settings.SYMBOLS:
        candles = storage.last_candles(sym, settings.TIMEFRAME, limit=500)
        if not candles:
            continue
        close_history[sym] = pd.Series([c.c for c in candles], index=[c.ts for c in candles])

    if not close_history:
        print("[forecast] no data yet")
        return

    # 2) прогноз на H шагов по каждому символу
    run_id = uuid.uuid4().hex[:12]
    exp_last = {}
    for sym, ser in close_history.items():
        df = forecasting.arima_returns_forecast(ser, settings.FORECAST_HORIZON)
        # сохраним прогноз по шагам
        rows = []
        t0 = ser.index[-1]
        for i, r in df.iterrows():
            rows.append({
                "horizon": settings.FORECAST_HORIZON,
                "ts_gen": datetime.utcnow(),
                "ts_pred": t0 + timedelta(hours=(i+1)),  # грубо для 1h
                "yhat": float(r["yhat"]),
                "yhat_lo": float(r["yhat_lo"]),
                "yhat_hi": float(r["yhat_hi"]),
            })
        storage.save_forecasts(settings.EXCHANGE_NAME, sym, "arima", run_id, rows)
        exp_last[sym] = float(df["yhat"].iloc[-1])  # ожидаемая цена на последний шаг

    # 3) оптимизация портфеля (Max Sharpe)
    weights = optimizer.optimize_from_expected(close_history, exp_last, settings.WEIGHT_MAX)
    storage.save_weights(run_id, weights, datetime.utcnow())
    print("[forecast] run", run_id, "weights", weights)

def job_rebalance_paper():
    # текущие рыночные цены — берём последние закрытия
    prices = {}
    for sym in settings.SYMBOLS:
        candles = storage.last_candles(sym, settings.TIMEFRAME, limit=1)
        if candles:
            prices[sym] = candles[-1].c
    if not prices:
        print("[rebalance] no prices")
        return
    # берём последние рассчитанные веса из forecasts/weights — для демо используем job_forecast_and_optimize, которая их пишет.
    # здесь для простоты просто равные если нет записей
    weights = {sym: 1.0/len(prices) for sym in prices}
    orders = execution.rebalance_paper(prices, weights, equity_usdt=10000.0)
    print("[rebalance] orders", orders)

def main():
    # убедимся, что таблицы есть (без alembic — для первого запуска)
    storage.create_all()
    sch = BlockingScheduler(timezone="UTC")
    sch.add_job(job_sync_candles, "interval", minutes=5, id="sync")
    sch.add_job(job_forecast_and_optimize, "interval", hours=1, id="forecast")
    sch.add_job(job_rebalance_paper, "interval", hours=1, id="rebalance", next_run_time=None)
    print("[scheduler] started")
    sch.start()

if __name__ == "__main__":
    main()
