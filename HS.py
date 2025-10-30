# HS Studio Card Pro Máximo – Ultimate Edition
import streamlit as st
from collections import defaultdict

st.set_page_config(page_title="HS Studio Card Pro Ultimate", page_icon="🎴", layout="centered")

# ==============================
# 🔹 Estilo visual cassino premium
st.markdown("""
<style>
body { background-color:#0b0c10; color:#f8f8f2; font-family:'Poppins', sans-serif;}
h1,h2,h3 { text-align:center; }
.stButton>button {
    width:100px; height:100px; font-size:35px; border-radius:20px;
    border:none; color:white; margin:10px; transition:0.3s;
}
.stButton>button:hover { transform:scale(1.08); box-shadow:0 0 30px gold; }
.result-box {
    background:linear-gradient(145deg,#1a1b20,#101113);
    border-radius:25px; padding:25px; margin-top:30px;
    box-shadow:0 0 30px rgba(255,215,0,0.3);
}
.pattern-box {
    background:#222; border-radius:15px; padding:15px; margin:10px 0;
    color:#fff; font-size:16px;
}
.prob-box {
    background:#111; border-radius:15px; padding:15px; margin:10px 0;
    color:#fff; font-size:16px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='color:gold;'>🎴 HS Studio Card Pro Ultimate</h1>", unsafe_allow_html=True)
st.markdown("### Inserir resultado:")

# ==============================
# 🔹 Estado da aplicação
if "historico" not in st.session_state:
    st.session_state.historico = []
if "padroes_aprendidos" not in st.session_state:
    st.session_state.padroes_aprendidos = {}

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
        st.session_state.padroes_aprendidos = {}

# Limitar a 27 últimos resultados
st.session_state.historico = st.session_state.historico[-27:]

# ==============================
# 🔹 Exibir histórico (mais recente à esquerda)
hist_exibicao = " ".join(["🔴" if x=="R" else "🔵" if x=="B" else "🟡" 
                          for x in reversed(st.session_state.historico)])
st.markdown(f"<h3 style='color:#aaa;'>Histórico ({len(st.session_state.historico)}/27):</h3>", unsafe_allow_html=True)
st.markdown(f"<h2 style='color:white;'>{hist_exibicao}</h2>", unsafe_allow_html=True)

# ==============================
# 🔹 Funções auxiliares
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
# 🔹 Motor máximo com sugestão de aposta
def motor_ultimate(historico, padroes_aprendidos):
    if len(historico)<5:
        return None, 0, "-", "-", 1, {}, {}
    seq = "".join(reversed(historico))  # análise mais antigo -> mais recente
    similares = {}
    tipos = {}
    contagem_prox = defaultdict(int)
    
    # análise de todas subsequências possíveis
    for tam in range(2, min(10,len(seq))):
        for start in range(len(seq)-tam+1):
            sub = seq[start:start+tam]
            sim, tipo = similaridade(sub, seq)
            similares[sub] = similares.get(sub,0)+sim
            tipos[sub] = tipo
            # aprendizado dinâmico de padrões
            if sub not in padroes_aprendidos:
                padroes_aprendidos[sub] = sim
            if espelhar(sub) not in padroes_aprendidos:
                padroes_aprendidos[espelhar(sub)] = sim
            # contar frequência da próxima cor
            if start+tam < len(seq):
                contagem_prox[seq[start+tam]] += sim
            else:
                contagem_prox[sub[-1]] += sim

    padrao_dom = max(similares, key=lambda k: similares[k])
    tipo_dom = tipos[padrao_dom]
    nivel_manip = int(min(9, max(1, 1 + (100 - similares[padrao_dom])//11)))
    prox = padrao_dom[-1]
    confianca = round(similares[padrao_dom]/len(seq),2)
    
    # calcular probabilidade da próxima cor
    total = sum(contagem_prox.values())
    prob = {k: round(v/total*100,2) for k,v in contagem_prox.items()} if total>0 else {}
    
    return prox, confianca, padrao_dom, tipo_dom, nivel_manip, padroes_aprendidos, prob

# ==============================
# 🔹 Exibir previsão
prox, confianca, padrao, tipo, nivel, st.session_state.padroes_aprendidos, prob = motor_ultimate(
    st.session_state.historico, st.session_state.padroes_aprendidos
)

if prox:
    cor_emoji = "🔴" if prox=="R" else "🔵" if prox=="B" else "🟡"
    cor_nome = "Vermelho" if prox=="R" else "Azul" if prox=="B" else "Empate"
    st.markdown(f"""
        <div class="result-box">
            <h2 style='color:gold;'>🎯 Próxima cor provável:</h2>
            <h1 style='font-size:70px;'>{cor_emoji} {cor_nome}</h1>
            <h3 style='color:#ccc;'>Confiança: {confianca}%</h3>
            <h3 style='color:#ccc;'>Nível de manipulação: {nivel}</h3>
            <h3 style='color:#ccc;'>Padrão dominante: {padrao} ({tipo})</h3>
        </div>
    """, unsafe_allow_html=True)
    
    # Exibir padrões detectados
    st.markdown("<h3 style='color:gold;'>📊 Padrões detectados:</h3>", unsafe_allow_html=True)
    for p, v in sorted(st.session_state.padroes_aprendidos.items(), key=lambda x:-x[1]):
        st.markdown(f"<div class='pattern-box'>{p} → Similaridade: {round(v,2)}%</div>", unsafe_allow_html=True)
    
    # Exibir sugestão de aposta (probabilidade próxima cor)
    st.markdown("<h3 style='color:gold;'>💹 Probabilidade da próxima cor:</h3>", unsafe_allow_html=True)
    for k, v in sorted(prob.items(), key=lambda x:-x[1]):
        emoji = "🔴" if k=="R" else "🔵" if k=="B" else "🟡"
        nome = "Vermelho" if k=="R" else "Azul" if k=="B" else "Empate"
        st.markdown(f"<div class='prob-box'>{emoji} {nome} → {v}%</div>", unsafe_allow_html=True)
    
    # Alerta manipulação avançada
    if nivel>=7:
        st.markdown(f"<h3 style='color:red;'>⚠️ Manipulação alta detectada! Nível: {nivel}</h3>", unsafe_allow_html=True)
else:
    st.markdown("<p style='color:#888;'>Insira pelo menos 5 resultados para iniciar a leitura comportamental.</p>", unsafe_allow_html=True)
