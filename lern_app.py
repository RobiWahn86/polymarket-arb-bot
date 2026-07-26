"""
Trading Bot Lern-App – interaktives Quiz + Flashcards
=====================================================
Usage:
  python lern_app.py
  → http://localhost:5001
"""
import os, json
from flask import Flask, render_template_string, jsonify, request

app = Flask(__name__)

# Quiz-Fragen
QUIZ = [
    {
        "id": 1,
        "frage": "Was ist Arbitrage?",
        "antworten": [
            "Der Kauf von Aktien an der Börse",
            "Das gleichzeitige Kaufen und Verkaufen desselben Guts zu unterschiedlichen Preisen",
            "Eine Strategie um Steuern zu sparen",
            "Das Halten von Kryptowährungen über einen langen Zeitraum",
        ],
        "richtig": 1,
        "erklärung": "Arbitrage nutzt Preisunterschiede zwischen Märkten aus. Du kaufst günstig und verkaufst teuer – gleichzeitig. Kein Risiko, garantierter Gewinn."
    },
    {
        "id": 2,
        "frage": "Wann existiert eine Arbitrage-Chance bei Prediction Markets?",
        "antworten": [
            "Wenn YES + NO > 1.00",
            "Wenn YES + NO < 1.00",
            "Wenn YES = NO",
            "Immer, wenn ein Event aktiv ist",
        ],
        "richtig": 1,
        "erklärung": "In Single-Winner-Märkten: Wenn die Summe aller NO-Preise < 1.00 ist, gibt es eine Arbitrage-Möglichkeit. Beispiel: NO auf A = 0.40 + NO auf B = 0.45 = 0.85 < 1.00 → Gewinn!"
    },
    {
        "id": 3,
        "frage": "Was ist Slippage?",
        "antworten": [
            "Die Gebühr die die Börse verlangt",
            "Der Unterschied zwischen erwartetem und tatsächlichem Ausführungspreis",
            "Die Zeit die eine Order braucht",
            "Ein Fehler im Bot-Code",
        ],
        "richtig": 1,
        "erklärung": "Slippage entsteht wenn der Preis zwischen Analyse und Order-Ausführung steigt. Ein guter Bot schützt sich davor mit einem Slippage-Limit (z.B. 0.5%)."
    },
    {
        "id": 4,
        "frage": "Was macht ein Multi-Level Orderbuch-Scanner?",
        "antworten": [
            "Er scannt nur den günstigsten Preis",
            "Er prüft die Top-10 Preis-Levels und matcht anteilig",
            "Er löscht alte Orders aus dem Buch",
            "Er berechnet den Durchschnittspreis aller Märkte",
        ],
        "richtig": 1,
        "erklärung": "Besonders in illiquiden Märkten reicht Level 1 nicht aus. Der Scanner nimmt die nächsten 10 Ask-Levels dazu und berechnet einen gewichteten Durchschnittspreis."
    },
    {
        "id": 5,
        "frage": "Wofür steht DRY_RUN=True?",
        "antworten": [
            "Der Bot läuft mit richtigem Geld",
            "Der Bot läuft im Simulationsmodus ohne echte Trades",
            "Der Bot trocknet die Daten",
            "Der Bot ist ausgeschaltet",
        ],
        "richtig": 1,
        "erklärung": "Im DRY_RUN-Modus werden alle Berechnungen und Logs geschrieben, aber keine echten Orders platziert. So testest du deinen Bot risikofrei."
    },
    {
        "id": 6,
        "frage": "Warum braucht ein Trading Bot ein Dashboard?",
        "antworten": [
            "Weil es schön aussieht",
            "Um Performance zu tracken und Probleme früh zu erkennen",
            "Weil YouTube es verlangt",
            "Um andere Händler zu beeindrucken",
        ],
        "richtig": 1,
        "erklärung": "Ohne Dashboard fliegt dir der Bot um die Ohren und du merkst es nicht. Ein gutes Dashboard zeigt: P&L-Chart, Win-Rate, offene Orders, Slippage und Fehler."
    },
]

HTML = """<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Trading Bot Lern-App – Argo.cashflow</title>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: 'Courier New', monospace; background: #050505; color: #f0f0f0; min-height: 100vh; }
.container { max-width: 700px; margin: 0 auto; padding: 40px 20px; }
h1 { font-size: 1.8rem; background: linear-gradient(135deg,#00f5ff,#39ff14); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 4px; }
.subtitle { color: #888; font-size: 0.9rem; margin-bottom: 30px; }

/* Progress */
.progress-bar { height: 4px; background: #1a1a2e; border-radius: 2px; margin-bottom: 30px; overflow: hidden; }
.progress-fill { height: 100%; background: linear-gradient(90deg,#00f5ff,#39ff14); border-radius: 2px; transition: width 0.5s; }

/* Card */
.card { background: #0a0a0f; border: 1px solid #1a1a2e; border-radius: 12px; padding: 32px; }
.card h2 { color: #00f5ff; font-size: 1.2rem; margin-bottom: 8px; }
.card .counter { color: #555; font-size: 0.8rem; margin-bottom: 20px; display: block; }

/* Answers */
.answers { display: flex; flex-direction: column; gap: 10px; margin-top: 20px; }
.answer-btn { background: #12121a; border: 1px solid #2a2a3e; border-radius: 8px; padding: 14px 20px; color: #ccc; font-size: 0.95rem; cursor: pointer; text-align: left; font-family: inherit; transition: all 0.2s; }
.answer-btn:hover { border-color: #00f5ff66; background: #1a1a2e; }
.answer-btn.correct { border-color: #39ff14; background: #0a1f0a; color: #39ff14; }
.answer-btn.wrong { border-color: #ff3333; background: #1f0a0a; color: #ff3333; }
.answer-btn:disabled { cursor: default; opacity: 0.8; }

/* Explanation */
.explanation { margin-top: 20px; padding: 16px; background: #0a1a1f; border-left: 3px solid #00f5ff; border-radius: 0 8px 8px 0; display: none; }
.explanation p { color: #aaa; font-size: 0.9rem; line-height: 1.5; }

/* Buttons */
.btn-row { display: flex; gap: 12px; margin-top: 24px; }
.btn { padding: 12px 32px; border: none; border-radius: 8px; font-family: inherit; font-size: 0.95rem; font-weight: bold; cursor: pointer; }
.btn-primary { background: linear-gradient(135deg,#00f5ff,#39ff14); color: #050505; }
.btn-primary:hover { transform: scale(1.02); }
.btn-secondary { background: #1a1a2e; color: #888; }
.btn-secondary:hover { background: #2a2a3e; }

/* Result page */
.result { text-align: center; }
.result .score { font-size: 4rem; color: #39ff14; font-weight: bold; margin: 20px 0; }
.result .score-label { color: #888; font-size: 1.1rem; }
.result .details { color: #888; font-size: 0.9rem; margin: 16px 0; line-height: 1.6; }

/* Stats */
.mini-stats { display: grid; grid-template-columns: repeat(3,1fr); gap: 12px; margin-bottom: 30px; }
.stat-box { background: #0a0a0f; border: 1px solid #1a1a2e; border-radius: 8px; padding: 16px; text-align: center; }
.stat-box .num { font-size: 1.5rem; color: #00f5ff; font-weight: bold; }
.stat-box .lbl { font-size: 0.75rem; color: #666; margin-top: 4px; }

.hidden { display: none; }
</style>
</head>
<body>
<div class="container">
    <h1>🤖 Trading Bot Lern-App</h1>
    <p class="subtitle">Teste dein Wissen – 6 Fragen zu Arbitrage, Bots & Trading</p>

    <div class="mini-stats">
        <div class="stat-box"><div class="num" id="qCount">0/6</div><div class="lbl">Fragen</div></div>
        <div class="stat-box"><div class="num" id="scoreCount">0</div><div class="lbl">Richtig</div></div>
        <div class="stat-box"><div class="num" id="streakCount">0</div><div class="lbl">Serie</div></div>
    </div>

    <div class="progress-bar"><div class="progress-fill" id="progressFill" style="width:0%"></div></div>

    <div id="quizContainer"></div>
    <div id="resultContainer" class="hidden"></div>
</div>

<script>
const QUIZ = {{ quiz_json|safe }};
let current = 0;
let correct = 0;
let streak = 0;
let answered = false;

function renderQuestion() {
    const q = QUIZ[current];
    answered = false;
    const idx = current + 1;
    const total = QUIZ.length;

    document.getElementById('qCount').textContent = idx + '/' + total;
    document.getElementById('progressFill').style.width = (idx / total * 100) + '%';

    const container = document.getElementById('quizContainer');
    let answersHTML = q.antworten.map((a, i) =>
        `<button class="answer-btn" data-idx="${i}" onclick="checkAnswer(this, ${i})">${a}</button>`
    ).join('');

    container.innerHTML = `
        <div class="card">
            <span class="counter">Frage ${idx} von ${total}</span>
            <h2>${q.frage}</h2>
            <div class="answers">${answersHTML}</div>
            <div class="explanation" id="explanation"><p>${q.erklaerung}</p></div>
            <div class="btn-row">
                <button class="btn btn-secondary" id="skipBtn" onclick="skipQuestion()">⏭ Überspringen</button>
                <button class="btn btn-primary hidden" id="nextBtn" onclick="nextQuestion()">Weiter →</button>
            </div>
        </div>
    `;
}

function checkAnswer(btn, idx) {
    if (answered) return;
    answered = true;

    const q = QUIZ[current];
    const allBtns = document.querySelectorAll('.answer-btn');
    allBtns.forEach(b => b.disabled = true);

    if (idx === q.richtig) {
        btn.classList.add('correct');
        correct++;
        streak++;
    } else {
        btn.classList.add('wrong');
        allBtns[q.richtig].classList.add('correct');
        streak = 0;
    }

    document.getElementById('scoreCount').textContent = correct;
    document.getElementById('streakCount').textContent = streak;
    document.getElementById('explanation').style.display = 'block';
    document.getElementById('skipBtn').classList.add('hidden');
    document.getElementById('nextBtn').classList.remove('hidden');
}

function skipQuestion() {
    if (answered) return;
    answered = true;
    streak = 0;
    document.getElementById('streakCount').textContent = streak;

    const q = QUIZ[current];
    const allBtns = document.querySelectorAll('.answer-btn');
    allBtns.forEach(b => b.disabled = true);
    allBtns[q.richtig].classList.add('correct');

    document.getElementById('explanation').style.display = 'block';
    document.getElementById('skipBtn').classList.add('hidden');
    document.getElementById('nextBtn').classList.remove('hidden');
}

function nextQuestion() {
    current++;
    if (current >= QUIZ.length) {
        showResult();
    } else {
        renderQuestion();
    }
}

function showResult() {
    document.getElementById('quizContainer').classList.add('hidden');
    document.getElementById('resultContainer').classList.remove('hidden');

    const pct = Math.round(correct / QUIZ.length * 100);
    let msg = '';
    if (pct === 100) msg = 'Perfekt! Du bist bereit für deinen eigenen Bot! 🚀';
    else if (pct >= 67) msg = 'Gut gemacht! Nur noch ein paar Details und du kannst starten! 📈';
    else if (pct >= 50) msg = 'Solide Basis! Wiederhol die Fragen die falsch waren und versuchs nochmal. 💪';
    else msg = 'Grundlagen sind da, aber schau dir die Erklärungen genau an. Wiederhol den Test! 📚';

    document.getElementById('resultContainer').innerHTML = `
        <div class="card result">
            <h2>🎉 Quiz abgeschlossen!</h2>
            <div class="score">${correct}/${QUIZ.length}</div>
            <div class="score-label">${pct}% richtig</div>
            <div class="details">${msg}</div>
            <div class="btn-row" style="justify-content:center">
                <button class="btn btn-primary" onclick="restart()">🔄 Nochmal</button>
                <a href="https://youtube.com/@argo.cashflow" class="btn btn-secondary" target="_blank">📺 YouTube Kanal</a>
            </div>
        </div>
    `;
}

function restart() {
    current = 0; correct = 0; streak = 0;
    document.getElementById('scoreCount').textContent = '0';
    document.getElementById('streakCount').textContent = '0';
    document.getElementById('quizContainer').classList.remove('hidden');
    document.getElementById('resultContainer').classList.add('hidden');
    renderQuestion();
}

renderQuestion();
</script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML, quiz_json=json.dumps(QUIZ))

@app.route("/api/quiz")
def api_quiz():
    return jsonify(QUIZ)

if __name__ == "__main__":
    print("🧠 Trading Bot Lern-App")
    print("   http://localhost:5001")
    app.run(host="0.0.0.0", port=5001, debug=True)
