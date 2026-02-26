import pandas as pd
import numpy as np

class RiskManagedEngine:
    def __init__(self, pairs, initial_balance=10000, risk_per_trade=0.10):
        self.balance = initial_balance
        self.initial_balance = initial_balance
        self.pairs = pairs
        self.risk_per_trade = risk_per_trade # 10% risk per trade
        self.positions = {pair: None for pair in pairs}
        self.history = []
        
    def calculate_lot_size(self, entry_price, stop_loss_price):
        # Risk 10% of CURRENT balance
        risk_amount = self.balance * self.risk_per_trade
        price_diff = abs(entry_price - stop_loss_price)
        if price_diff == 0: return 0
        return risk_amount / price_diff

    def process_tick(self, pair, date, price, open_price, high_impact_news=False):
        if high_impact_news:
            return f"⚠️ {pair} [{date}]: Skip (News Risk)"

        # Strategy Parameters
        atr_multiplier = 1.5 # Volatility factor for SL
        tp_multiplier = 2.0  # Reward/Risk ratio 1:2
        
        # TA Signal: Bullish Candle
        if price > open_price and self.positions[pair] is None:
            # Set Stop Loss below open price (assuming volatility room)
            sl_price = open_price * 0.995 # 0.5% stop loss for example
            tp_price = price + (price - sl_price) * tp_multiplier
            
            lot_size = self.calculate_lot_size(price, sl_price)
            
            self.positions[pair] = {
                'open_price': price, 
                'sl': sl_price, 
                'tp': tp_price,
                'volume': lot_size,
                'date': date
            }
            return f"🚀 {pair} [{date}]: BUY at {price} | SL: {sl_price:.4f} | TP: {tp_price:.4f} | Risk: 10%"
            
        elif self.positions[pair] is not None:
            pos = self.positions[pair]
            
            # Check Stop Loss
            if price <= pos['sl']:
                profit = (price - pos['open_price']) * pos['volume']
                self.balance += profit
                self.history.append({'pair': pair, 'profit': profit, 'date': date, 'type': 'SL'})
                self.positions[pair] = None
                return f"🛑 {pair} [{date}]: STOP LOSS hit at {price} | Loss: ${profit:.2f}"
            
            # Check Take Profit
            elif price >= pos['tp']:
                profit = (price - pos['open_price']) * pos['volume']
                self.balance += profit
                self.history.append({'pair': pair, 'profit': profit, 'date': date, 'type': 'TP'})
                self.positions[pair] = None
                return f"💰 {pair} [{date}]: TAKE PROFIT hit at {price} | Profit: ${profit:.2f}"
            
            # Close manually if trend reverses (TA signal)
            elif price < open_price:
                profit = (price - pos['open_price']) * pos['volume']
                self.balance += profit
                self.history.append({'pair': pair, 'profit': profit, 'date': date, 'type': 'Manual'})
                self.positions[pair] = None
                return f"📉 {pair} [{date}]: Manual Exit at {price} | P/L: ${profit:.2f}"
            
        return None

# --- Market Data ---
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

engine = RiskManagedEngine(list(market_data.keys()))

print("--- START PROFIT-ORIENTED SIMULATION (10% Risk) ---")
for day_idx in range(2):
    for pair, ticks in market_data.items():
        tick = ticks[day_idx]
        res = engine.process_tick(pair, tick['Date'], tick['Price'], tick['Open'], tick['News'])
        if res: print(res)

print("\n--- PERFORMANCE SUMMARY ---")
print(f"Final Balance: ${engine.balance:.2f}")
print(f"ROI:           {((engine.balance/engine.initial_balance)-1)*100:.1f}%")