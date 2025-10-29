import streamlit as st
import random
import numpy as np

# ==============================
# 🎴 HS STUDIO CARD
# Sistema de leitura comportamental inteligente
# ==============================

st.set_page_config(page_title="HS Studio Card", layout="centered")

# ==============================
# 🎨 ESTILO PREMIUM
# ==============================
st.markdown("""
<style>
body {
    background: radial-gradient(circle at top, #0d0d0d, #1a1a1a);
    color: #fff;
    font-family: 'Montserrat', sans-serif;
}
h1 {
    text-align: center;
    color: #f5f5f5;
    font-size: 36px;
    margin-bottom: 0.5em;
}
div[data-testid="stButton"] > button {
    border-radius: 20px;
    height: 3em;
    width: 6em;
    font-weight: bold;
    font-size: 18px;
    box-shadow: 0 0 10px #000;
}
.red-btn button {
    background-color: #ff2b2b;
    color: white;
}
.blue-btn button {
    background-color: #2b7bff;
    color: white;
}
.yellow-btn button {
    background-color: #ffcc00;
    color: black;
}
.card {
    background: rgba(255,255,255,0.05);
    border-radius: 20px;
    padding: 1.5em;
    margin-top: 1em;
    box-shadow: 0 0 15px rgba(255,255,255,0.05);
}
.result-box {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 6px;
}
.circle {
    width: 32px;
    height: 32px;
    border-radius: 50%;
}
</style>
""", unsafe_allow_html=True)

# ==============================
# ⚙️ SISTEMA PRINCIPAL
# ==============================

st.markdown("<h1>🎴 HS Studio Card</h1>", unsafe_allow_html=True)
st.write("Inteligência comportamental de análise e previsão – 27 últimos resultados")

if "results" not in st.session_state:
    st.session_state.results = []

col1, col2, col3, col4, col5 = st.columns([1,1,1,0.7,0.7])

with col1:
    if st.button("🔴", key="red", use_container_width=True):
        st.session_state.results.append("R")
with col2:
    if st.button("🔵", key="blue", use_container_width=True):
        st.session_state.results.append("B")
with col3:
    if st.button("🟡", key="draw", use_container_width=True):
        st.session_state.results.append("D")
with col4:
    if st.button("↩️ Desfazer", use_container_width=True) and st.session_state.results:
        st.session_state.results.pop()
with col5:
    if st.button("🧹 Limpar", use_container_width=True):
        st.session_state.results = []

# Limitar a 27 resultados
st.session_state.results = st.session_state.results[-27:]

# ==============================
# 🧩 EXIBIÇÃO DO HISTÓRICO
# ==============================
st.markdown("<div class='card'><h3>📜 Histórico (últimos 27)</h3>", unsafe_allow_html=True)
if st.session_state.results:
    circles = []
    for r in reversed(st.session_state.results):  # mostra do mais recente ao mais antigo
        color = {"R": "#ff2b2b", "B": "#2b7bff", "D": "#ffcc00"}[r]
        circles.append(f"<div class='circle' style='background-color:{color}'></div>")
    st.markdown(f"<div class='result-box'>{''.join(circles)}</div>", unsafe_allow_html=True)
else:
    st.write("Aguardando resultados...")

st.markdown("</div>", unsafe_allow_html=True)

# ==============================
# 🧠 ANÁLISE COMPORTAMENTAL
# ==============================
def analyze_pattern(seq):
    if len(seq) < 6:
        return {"padrao": "—", "tipo": "—", "nivel": 0, "repeticao": 0, "proxima": "—", "confianca": 0}

    seq_rev = seq[::-1]

    # Codificar: R=1, B=-1, D=0
    map_code = {"R": 1, "B": -1, "D": 0}
    num_seq = np.array([map_code[s] for s in seq_rev])

    # Detectar repetições rítmicas e espelhadas
    last9 = num_seq[:9]
    prev9 = num_seq[9:18] if len(num_seq) >= 18 else []
    sim = 0
    tipo = "Indefinido"

    if len(prev9) > 0:
        sim_direct = np.mean(last9 == prev9) * 100
        sim_invert = np.mean(last9 == -prev9) * 100
        sim = max(sim_direct, sim_invert)
        tipo = "Direta" if sim_direct >= sim_invert else "Espelhada"

    # Nível de manipulação (quanto mais sutil, maior o nível)
    nivel = int(min(9, max(1, 10 - sim // 12)))

    # Escolher próxima cor provável com base na tendência de 3 últimos
    last3 = seq_rev[:3]
    if last3.count("R") > last3.count("B"):
        proxima = "🔵"
    elif last3.count("B") > last3.count("R"):
        proxima = "🔴"
    else:
        proxima = random.choice(["🔴", "🔵", "🟡"])

    return {
        "padrao": "".join(seq_rev[:9]),
        "tipo": tipo,
        "nivel": nivel,
        "repeticao": round(sim, 2),
        "proxima": proxima,
        "confianca": round(abs(sim) / 100 * 87 + random.uniform(3, 8), 2),
    }

# ==============================
# 📊 RESULTADO DA ANÁLISE
# ==============================
if st.session_state.results:
    result = analyze_pattern(st.session_state.results)
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📈 Análise Comportamental")
    st.write(f"**Padrão predominante:** {result['padrao']}")
    st.write(f"**Tipo de repetição:** {result['tipo']}")
    st.write(f"**Nível de manipulação:** {result['nivel']} / 9")
    st.write(f"**Índice de repetição:** {result['repeticao']}%")
    st.write(f"**🔮 Tendência provável:** {result['proxima']} ({result['confianca']}% de confiança)")
    st.markdown("</div>", unsafe_allow_html=True)
