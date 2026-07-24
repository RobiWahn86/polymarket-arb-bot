# 🤖 Polymarket Arbitrage Bot

> **Vollautomatischer Arbitrage-Bot für Polymarket Prediction Markets**
> Finde und trade mathematisch garantierte Arbitrage-Gelegenheiten – automatisch, 24/7.

[![Python](https://img.shields.io/badge/Python-3.10%2B-39ff14)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-ff00ff)](LICENSE)

---

## 🚀 Was ist das?

Ein Python-Bot der **risikofreie Arbitrage** auf Polymarket Prediction Markets identifiziert und automatisch traded.

**Das Prinzip:** In Single-Winner-Märkten (z.B. "Wer wird US-Präsident?") sind die Preise von YES + NO oft < 1.00. Der Bot kauft die NO-Positionen aller Kandidaten → egal wer gewinnt → garantierte Auszahlung von 1.00 → **risikofreier Gewinn**.

## ✨ Features

| Feature | Beschreibung |
|---------|-------------|
| 🔍 **Multi-Level Orderbook** | Scannt top 10 Ask-Levels, matched über mehrere Ebenen |
| 🛡️ **Slippage-Schutz** | Konfigurierbares Limit + automatischer Abbruch |
| 🔄 **Retry-Logik** | 3 Versuche mit Preis-Anpassung bei Fehlern |
| 📊 **Live-Dashboard** | Flask + Chart.js – P&L, Win-Rate, Trade-History |
| 📝 **CSV-Trade-Log** | Jeder Trade wird geloggt (Event, Preis, Slippage, Profit) |
| 🧪 **Simulations-Modus** | Teste ohne echtes Geld (DRY_RUN=True) |
| 📈 **Performance-Tracking** | Wochenberichte, KPIs, Event-Analyse |

## 📦 Installation

```bash
# 1. Paket installieren
pip install polymarket-arb-bot

# 2. Konfiguration anlegen
polymarket-bot --setup

# 3. .env-Datei bearbeiten (API-Key etc. eintragen)
nano .env

# 4. Bot starten (Simulation)
polymarket-bot

# 5. Dashboard öffnen
polymarket-dashboard
# → http://localhost:5000
```

## 🎯 Quick Start

```python
from polymarket_arb_bot import ArbitrageBot

bot = ArbitrageBot(dry_run=True)
opportunities = bot.scan_markets()

for opp in opportunities:
    print(f"{opp['title']}: {opp['best_roi']:.2f}% ROI")
    bot.execute_arbitrage(opp)
```

## 📊 Dashboard

Das Live-Dashboard zeigt dir in Echtzeit:
- Kumulierter Gewinn/Verlust (Chart)
- Win/Loss-Ratio
- Trade-History mit Slippage
- Top-Events nach Profit
- 24h-Statistik

## 🧠 Mathematik

Für k sich gegenseitig ausschließende Outcomes:

```
Kaufe NO auf Outcome₁...Outcomeₖ

Kosten = Σ(NO-Preise)  <  1.00  →  Arbitrage!
Gewinn = 1.00 - Kosten  (risikofrei)
ROI   = Gewinn / Kosten * 100
```

## 🔧 Konfiguration

```ini
# .env
DRY_RUN=True                    # True = Simulation, False = Live
MIN_ROI_THRESHOLD=0.10          # Minimale Rendite in %
TRADE_AMOUNT_USD=10.0           # Einsatz pro Set
SLIPPAGE_LIMIT=0.005            # Max. 0.5% Slippage
```

## 📹 Video-Tutorials

Der gesamte Code wird in meinem YouTube-Kanal **Argo.cashflow** Schritt für Schritt erklärt:

1. [Arbitrage erklärt – wie Bots Geld verdienen](https://youtu.be/T4dIL3-BR8Q)
2. [Trading Bot in 30 Zeilen Python](https://youtu.be/lK-EQJbMTEk)
3. [Polymarket API einrichten](https://youtu.be/rgyMLefGKfI)
4. [Live Coding: Bot von Null programmiert](https://youtu.be/Ii9JBOwZbm8)
5. [Live-Trading aktivieren](https://youtu.be/VIDEO_5)
6. [Bot-Performance tracken](https://youtu.be/svr2386dCzY)

## 🛡️ Lizenz

MIT – frei für private und kommerzielle Nutzung.

---

<div align="center">
  <p><b>Argo.cashflow</b> – Automatisiertes Trading mit Python</p>
  <p>
    <a href="https://youtube.com/@argo.cashflow">YouTube</a> •
    <a href="https://github.com/argo-cashflow">GitHub</a>
  </p>
</div>
