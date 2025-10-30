# HS Studio Card V2 – Corrigido
import streamlit as st

st.set_page_config(page_title="HS Studio Card", page_icon="🎴", layout="centered")

# ==============================
# 🔹 Estilo visual cassino
st.markdown("""
<style>
body { background-color:#0b0c10; color:#f8f8f2; font-family:'Poppins', sans-serif;}
h1,h2,h3 { text-align:center; }
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
# 🔹 Exibir histórico da esquerda (mais recente) para direita (mais antigo)
hist_exibicao = " ".join(["🔴" if x=="R" else "🔵" if x=="B" else "🟡" 
                          for x in reversed(st.session_state.historico)])
st.markdown(f"<h3 style='color:#aaa;'>Histórico ({len(st.session_state.historico)}/27):</h3>", unsafe_allow_html=True)
st.markdown(f"<h2 style='color:white;'>{hist_exibicao}</h2>", unsafe_allow_html=True)

# ==============================
# 🔹 Funções auxiliares de inteligência
def espelhar(seq):
    return "".join(["B" if x=="R" else "R" if x=="B" else "D" for x in seq])

def similaridade(sub, target):
    max_sim = 0
    tipo = "Indefinido"
    for i in range(len(target)-len(sub)+1):
        seg = target[i:i+len(sub)]
        sim = sum([1 for a,b in zip(sub, seg) if a==b])/len(sub)*100
        if sim>max_sim:
            max_sim = sim
            tipo = "Direta"
        sim_esp = sum([1 for a,b in zip(espelhar(sub), seg) if a==b])/len(sub)*100
        if sim_esp>max_sim:
            max_sim = sim_esp
            tipo = "Espelhada"
    return max_sim, tipo

# ==============================
# 🔹 Motor inteligente de análise
def motor_inteligente(historico):
    if len(historico)<5:
        return None, 0, "-", "-", 1
    # ANÁLISE DA DIREITA PARA A ESQUERDA (mais antigo -> mais recente)
    seq = "".join(reversed(historico))
    similares = {}
    tipos = {}
    for tam in range(2, min(10,len(seq))):
        for start in range(len(seq)-tam+1):
            sub = seq[start:start+tam]
            sim, tipo = similaridade(sub, seq)
            similares[sub] = similares.get(sub,0)+sim
            tipos[sub] = tipo
    padrao_dom = max(similares, key=lambda k: similares[k])
    tipo_dom = tipos[padrao_dom]
    nivel_manip = int(min(9, max(1, 1 + (100 - similares[padrao_dom])//11)))
    prox = padrao_dom[-1]
    confianca = round(similares[padrao_dom]/len(seq),2)
    return prox, confianca, padrao_dom, tipo_dom, nivel_manip

# ==============================
# 🔹 Exibir previsão
prox, confianca, padrao, tipo, nivel = motor_inteligente(st.session_state.historico)
if prox:
    cor_emoji = "🔴" if prox=="R" else "🔵" if prox=="B" else "🟡"
    cor_nome = "Vermelho" if prox=="R" else "Azul" if prox=="B" else "Empate"
    st.markdown(f"""
        <div class="result-box">
            <h2 style='color:gold;'>🎯 Próxima cor provável:</h2>
            <h1 style='font-size:70px;'>{cor_emoji} {cor_nome}</h1>
            <h3 style='color:#ccc;'>Confiança: {confianca}%</h3>
            <h3 style='color:#ccc;'>Nível de manipulação: {nivel}</h3>
        </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("<p style='color:#888;'>Insira pelo menos 5 resultados para iniciar a leitura comportamental.</p>", unsafe_allow_html=True)
