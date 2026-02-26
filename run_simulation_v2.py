import pandas as pd

# Forex Simulation V2: TA + FA Integration
# Strategy: Trend Following (SMA) + News Filter

data = [
    {"Date": "Feb 17, 2026", "Price": 1.1855, "Open": 1.1851},
    {"Date": "Feb 18, 2026", "Price": 1.1784, "Open": 1.1854},
    {"Date": "Feb 19, 2026", "Price": 1.1774, "Open": 1.1784},
    {"Date": "Feb 20, 2026", "Price": 1.1782, "Open": 1.1774},
    {"Date": "Feb 23, 2026", "Price": 1.1786, "Open": 1.1785},
    {"Date": "Feb 24, 2026", "Price": 1.1772, "Open": 1.1791},
    {"Date": "Feb 25, 2026", "Price": 1.1811, "Open": 1.1773},
    {"Date": "Feb 26, 2026", "Price": 1.1795, "Open": 1.1816},
]

# FA: High Impact News Events (Simulated/Scraped)
# On Feb 25, we had CPI data. Let's assume it was a "no trade" zone due to volatility.
high_impact_news = ["Feb 25, 2026"]

df = pd.DataFrame(data)
# TA: SMA 3 (Short period for this small sample)
df['SMA3'] = df['Price'].rolling(window=3).mean()

balance = 10000
lot_size = 100000
position = None
logs = []

print(f"--- СТАРТ СИМУЛЯЦИИ V2 (TA + FA) ---")
print(f"Депозит: ${balance} | Режим: Бесшовный (No Martingale)\n")

for i, row in df.iterrows():
    date = row['Date']
    price = row['Price']
    sma = row['SMA3']
    
    # Check FA Filter (News)
    if date in high_impact_news:
        print(f"⚠️ {date}: ПРОПУСК (FA: High Impact News detected)")
        continue

    if pd.isna(sma):
        continue

    # TA Logic: Buy if price > SMA3 (Trend is UP)
    if price > sma and position is None:
        position = {'open_price': price, 'date': date}
        print(f"📈 {date}: СИГНАЛ TA (Buy) -> ВХОД по {price}")

    # TA Logic: Close if price < SMA3 (Trend reversal)
    elif price < sma and position is not None:
        profit = (price - position['open_price']) * lot_size
        balance += profit
        status = "WIN" if profit > 0 else "LOSS"
        print(f"📉 {date}: СИГНАЛ TA (Exit) -> ВЫХОД по {price} | Result: {status} (${profit:.2f})")
        logs.append(profit)
        position = None

print(f"\n--- ИТОГОВЫЙ ОТЧЕТ V2 ---")
print(f"Конечный баланс: ${balance:.2f}")
print(f"Чистая прибыль: ${balance - 10000:.2f}")
print(f"Всего сделок: {len(logs)}")
if logs:
    win_rate = (pd.Series(logs) > 0).mean() * 100
    print(f"Win Rate: {win_rate:.1f}%")