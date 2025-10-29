# HS Studio Card V2 - Motor de Padrões Profissional
import streamlit as st
import numpy as np

st.set_page_config(page_title="HS Studio Card", page_icon="🎴", layout="centered")

# ==============================
# 🔹 Estilo visual cassino
st.markdown("""
<style>
body { background-color:#0b0c10; color:#f8f8f2; font-family:'Poppins', sans-serif;}
h1, h2, h3 { text-align:center;}
.stButton>button {
    width:100px; height:100px; font-size:35px; border-radius:20px;
    border:none; color:white; margin:10px; transition:0.3s;
}
.stButton>button:hover { transform:scale(1.08); box-shadow:0 0 20px gold; }
.result-box {
    background:linear-gradient(145deg,#1a1b20,#101113);
    border-radius:20px; padding:25px; margin-top:30px;
    box-shadow:0 0 25px rgba(255,215,0,0.2);
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='color:gold;'>🎴 HS Studio Card V2</h1>", unsafe_allow_html=True)
st.markdown("### Inserir resultado:")

# ==============================
# 🔹 Estado da aplicação
if "historico" not in st.session_state:
    st.session_state.historico = []

# ==============================
# 🔹 Botões de inserção
col1, col2, col3, col4, col5 = st.columns([1,1,1,0.5,1])
with col1:
    if st.button("🔴"): st.session_state.historico.append("R")
with col2:
    if st.button("🔵"): st.session_state.historico.append("B")
with col3:
    if st.button("🟡"): st.session_state.historico.append("D")
with col4:
    if st.button("↩️ Desfazer") and st.session_state.historico:
        st.session_state.historico.pop()
with col5:
    if st.button("🧹 Limpar"):
        st.session_state.historico = []

# Limitar a 27 últimos resultados
st.session_state.historico = st.session_state.historico[-27:]

# ==============================
# 🔹 Exibir histórico
hist_exibicao = " ".join(["🔴" if x=="R" else "🔵" if x=="B" else "🟡" for x in st.session_state.historico])
st.markdown(f"<h3 style='color:#aaa;'>Histórico ({len(st.session_state.historico)}/27):</h3>", unsafe_allow_html=True)
st.markdown(f"<h2 style='color:white;'>{hist_exibicao}</h2>", unsafe_allow_html=True)

# ==============================
# 🔹 Funções auxiliares de análise
def espelhar(seq):
    return "".join(["B" if x=="R" else "R" if x=="B" else "D" for x in seq])

def calcular_similaridade(sub, target):
    # compara exata, espelhada e deslocada
    max_sim = 0
    tipo = "Indefinido"
    for i in range(len(target)-len(sub)+1):
        segmento = target[i:i+len(sub)]
        sim = sum([1 for a,b in zip(sub, segmento) if a==b])/len(sub)*100
        if sim>max_sim:
            max_sim = sim
            tipo = "Direta"
        # espelhamento
        sim_esp = sum([1 for a,b in zip(espelhar(sub), segmento) if a==b])/len(sub)*100
        if sim_esp>max_sim:
            max_sim = sim_esp
            tipo = "Espelhada"
    return max_sim, tipo

# ==============================
# 🔹 Motor profissional de análise
def analisar_padroes(historico):
    if len(historico)<5:
        return None, 0
    seq = "".join(historico)
    similar_total = {}
    tipos_total = {}
    # gera todas sub-sequências 2-9
    for tam in range(2, min(10,len(seq))):
        for start in range(len(seq)-tam+1):
            sub = seq[start:start+tam]
            sim, tipo = calcular_similaridade(sub, seq)
            similar_total[sub] = similar_total.get(sub,0)+sim
            tipos_total[sub] = tipo
    # padrão dominante
    padrao_dom = max(similar_total, key=lambda k: similar_total[k])
    tipo_dom = tipos_total[padrao_dom]
    nivel_manip = int(min(9, max(1, 1 + (100 - similar_total[padrao_dom])//11)))
    # escolha próxima cor baseada no último padrão
    prox = padrao_dom[-1]
    # confiança ponderada
    confianca = round(similar_total[padrao_dom]/len(seq),2)
    return prox, confianca, padrao_dom, tipo_dom, nivel_manip

# ==============================
# 🔹 Exibir resultado da análise
if st.session_state.historico:
    prox, confianca, padrao, tipo, nivel = analisar_padroes(st.session_state.historico)
    cor_emoji = "🔴" if prox=="R" else "🔵" if prox=="B" else "🟡"
    cor_nome = "Vermelho" if prox=="R" else "Azul" if prox=="B" else "Empate"
    st.markdown(f"""
        <div class="result-box">
            <h2 style='color:gold;'>🎯 Próxima cor provável:</h2>
            <h1 style='font-size:70px;'>{cor_emoji} {cor_nome}</h1>
            <h3 style='color:#ccc;'>Confiança: {confianca}%</h3>
        </div>
    """, unsafe_allow_html=True)
