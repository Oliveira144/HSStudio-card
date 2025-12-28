import streamlit as st
from collections import Counter

# ======================
# CONFIG
# ======================
st.set_page_config(page_title="Football Studio IA Pro", layout="centered")
st.title("🧠 Football Studio – IA Profissional (Mesa Real)")

# ======================
# ESTADO
# ======================
if "h" not in st.session_state:
    st.session_state.h = []  # MAIS RECENTE SEMPRE NA POSIÇÃO 0

# ======================
# FUNÇÕES BASE
# ======================
def limitar_historico(h, limite=90):
    return h[:limite]

def nivel_manipulacao(h):
    if len(h) < 5:
        return 1

    ult = h[:10]  # mais recentes
    cont = Counter(ult)

    nivel = 1
    if max(cont["R"], cont["B"]) >= 3:
        nivel += 1
    if max(cont["R"], cont["B"]) >= 5:
        nivel += 2
    if cont["E"] >= 1:
        nivel += 1
    if cont["E"] >= 2:
        nivel += 2
    if cont["R"] == cont["B"]:
        nivel += 1
    if len(set(ult[:4])) == 4:
        nivel += 1  # confusão proposital

    return min(nivel, 9)

def detectar_macro_padrao(h):
    if len(h) < 6:
        return "Histórico insuficiente"

    ult = h[:6]

    if ult[0] == "E" and ult[1] == "E":
        return "Empate Duplo (Limpeza)"

    if ult[0] == "E" and ult[1] == ult[2]:
        return "Empate de Corte"

    if ult[:4] in (["R","B","R","B"], ["B","R","B","R"]):
        return "Alternância Perfeita (Falsa)"

    if ult[0] == ult[1] == ult[2]:
        return "Tripla Repetição"

    if ult.count("R") >= 5:
        return "Sequência Forte Vermelho"

    if ult.count("B") >= 5:
        return "Sequência Forte Azul"

    return "Padrão Camuflado"

def falso_padrao(h):
    if len(h) < 5:
        return False
    ult = h[:5]
    return ult.count("R") == ult.count("B") and "E" not in ult

def leitura_quantica(h):
    pontos = {"R": 0, "B": 0}
    ult = h[:10]
    cont = Counter(ult)

    # Excesso
    if cont["R"] >= 5:
        pontos["B"] += 1
    if cont["B"] >= 5:
        pontos["R"] += 1

    # Empate como corte
    if ult[0] == "E":
        if ult[1] == "R":
            pontos["B"] += 1
        if ult[1] == "B":
            pontos["R"] += 1

    # Pressão psicológica
    if cont["R"] > cont["B"]:
        pontos["B"] += 1
    if cont["B"] > cont["R"]:
        pontos["R"] += 1

    return pontos

def decisao_final(h):
    macro = detectar_macro_padrao(h)
    nivel = nivel_manipulacao(h)
    quant = leitura_quantica(h)
    falso = falso_padrao(h)

    if macro == "Empate Duplo (Limpeza)":
        return "⛔ PAUSAR", "Limpeza total da mesa", 92

    if nivel >= 8:
        return "⏳ AGUARDAR", "Manipulação extrema", 88

    if falso:
        return "🔄 CONTRARIAR", "Falso padrão detectado", 82

    if quant["R"] >= 2:
        return "▶️ ENTRAR 🔴", "Convergência quântica", 79

    if quant["B"] >= 2:
        return "▶️ ENTRAR 🔵", "Convergência quântica", 79

    return "⏳ AGUARDAR", "Sem brecha clara", 65

# ======================
# INSERÇÃO DE RESULTADO
# ======================
st.subheader("Inserir Resultado (Mesa Real)")

c1, c2, c3 = st.columns(3)

with c1:
    if st.button("🔴 Vermelho"):
        st.session_state.h.insert(0, "R")

with c2:
    if st.button("🔵 Azul"):
        st.session_state.h.insert(0, "B")

with c3:
    if st.button("🟡 Empate"):
        st.session_state.h.insert(0, "E")

st.session_state.h = limitar_historico(st.session_state.h)

# ======================
# HISTÓRICO VISUAL
# ======================
st.subheader("Histórico (Mais recente à esquerda)")

def render(h):
    mapa = {"R": "🔴", "B": "🔵", "E": "🟡"}
    linhas = [h[i:i+9] for i in range(0, len(h), 9)]
    for l in linhas:
        st.write(" ".join(mapa[x] for x in l))

render(st.session_state.h)

# ======================
# PAINEL DE IA
# ======================
if len(st.session_state.h) >= 6:
    st.divider()
    st.subheader("🧠 Análise Inteligente")

    macro = detectar_macro_padrao(st.session_state.h)
    nivel = nivel_manipulacao(st.session_state.h)
    acao, motivo, conf = decisao_final(st.session_state.h)

    st.write(f"**Macro Padrão:** {macro}")
    st.write(f"**Nível de Manipulação:** {nivel}/9")
    st.write(f"**Decisão da IA:** {acao}")
    st.write(f"**Motivo:** {motivo}")
    st.write(f"**Confiança:** {conf}%")

# ======================
# RESET
# ======================
if st.button("♻️ Resetar Mesa"):
    st.session_state.h = []
