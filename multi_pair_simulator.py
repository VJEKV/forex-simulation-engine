import pandas as pd
import numpy as np

class MultiPairEngine:
    def __init__(self, pairs, initial_balance=10000):
        self.balance = initial_balance
        self.initial_balance = initial_balance
        self.pairs = pairs
        self.positions = {pair: None for pair in pairs}
        self.history = []
        
    def process_tick(self, pair, date, price, open_price, high_impact_news=False):
        if high_impact_news:
            return f"⚠️ {pair} [{date}]: Skip due to FA (News)"

        lot_size = 20000  # Smaller lot for multi-pair risk management
        sma_period = 3
        
        # Simple TA state (in a real app we'd keep a rolling window)
        # For this sim, we'll assume 'sma' is passed or calculated externally
        # Here we just use price > open as a proxy for the trend in this tick
        
        if price > open_price and self.positions[pair] is None:
            self.positions[pair] = {'open_price': price, 'date': date, 'side': 'BUY'}
            return f"📈 {pair} [{date}]: BUY at {price}"
            
        elif price < open_price and self.positions[pair] is not None:
            pos = self.positions[pair]
            profit = (price - pos['open_price']) * lot_size
            self.balance += profit
            self.history.append({'pair': pair, 'profit': profit, 'date': date})
            self.positions[pair] = None
            return f"📉 {pair} [{date}]: CLOSE at {price} | Profit: ${profit:.2f}"
            
        return None

# --- Simulated Data for 5 Pairs (Feb 25-26, 2026) ---
market_data = {
    "EUR/USD": [
        {"Date": "Feb 25", "Open": 1.1773, "Price": 1.1811, "News": True},
        {"Date": "Feb 26", "Open": 1.1816, "Price": 1.1795, "News": False}
    ],
    "GBP/USD": [
        {"Date": "Feb 25", "Open": 1.2510, "Price": 1.2580, "News": True},
        {"Date": "Feb 26", "Open": 1.2585, "Price": 1.2560, "News": False}
    ],
    "USD/JPY": [
        {"Date": "Feb 25", "Open": 149.50, "Price": 150.20, "News": False},
        {"Date": "Feb 26", "Open": 150.25, "Price": 149.80, "News": False}
    ],
    "AUD/USD": [
        {"Date": "Feb 25", "Open": 0.6540, "Price": 0.6510, "News": True},
        {"Date": "Feb 26", "Open": 0.6515, "Price": 0.6535, "News": False}
    ],
    "USD/CAD": [
        {"Date": "Feb 25", "Open": 1.3620, "Price": 1.3680, "News": False},
        {"Date": "Feb 26", "Open": 1.3685, "Price": 1.3710, "News": False}
    ]
}

engine = MultiPairEngine(list(market_data.keys()))

print("--- START MULTI-PAIR SIMULATION ---")
for day_idx in range(2):
    for pair, ticks in market_data.items():
        tick = ticks[day_idx]
        res = engine.process_tick(pair, tick['Date'], tick['Price'], tick['Open'], tick['News'])
        if res: print(res)

print("\n--- FINAL MULTI-PAIR REPORT ---")
print(f"Initial Balance: ${engine.initial_balance}")
print(f"Final Balance:   ${engine.balance:.2f}")
print(f"Total P&L:       ${engine.balance - engine.initial_balance:.2f}")

if engine.history:
    df_hist = pd.DataFrame(engine.history)
    print("\nPerformance by Pair:")
    print(df_hist.groupby('pair')['profit'].sum())