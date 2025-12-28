import streamlit as st
from collections import Counter

st.set_page_config(page_title="Football Studio IA Pro", layout="centered")
st.title("🧠 Football Studio – IA Profissional de Manipulação")

# =========================
# ESTADO
# =========================
if "h" not in st.session_state:
    st.session_state.h = []

# =========================
# FUNÇÕES BASE
# =========================
def limite_hist(h, lim=90):
    return h[-lim:]

def nivel_manipulacao(h):
    score = 1
    if len(h) < 6:
        return score

    ult = h[-10:]
    rep_r = ult.count("R")
    rep_b = ult.count("B")
    emp = ult.count("E")

    if max(rep_r, rep_b) >= 3: score += 1
    if max(rep_r, rep_b) >= 5: score += 2
    if emp >= 1: score += 1
    if emp >= 2: score += 2
    if rep_r == rep_b: score += 1
    if len(set(ult[-4:])) == 4: score += 1  # confusão proposital

    return min(score, 9)

def detectar_macro_padrao(h):
    if len(h) < 6:
        return "Histórico insuficiente"

    ult = h[-6:]

    if ult[-2:] == ["E","E"]:
        return "Empate Duplo (Limpeza)"
    if ult[-1] == "E" and ult[-2] == ult[-3]:
        return "Empate de Corte"
    if ult[-4:] in (["R","B","R","B"],["B","R","B","R"]):
        return "Alternância Perfeita (Falsa)"
    if ult[-3] == ult[-2] == ult[-1]:
        return "Tripla Repetição"
    if ult.count("R") >= 5:
        return "Sequência Forte Vermelho"
    if ult.count("B") >= 5:
        return "Sequência Forte Azul"

    return "Padrão Camuflado"

def falso_padrao(h):
    if len(h) < 5:
        return False
    ult = h[-5:]
    return ult.count("R") == ult.count("B") and "E" not in ult

def leitura_quântica(h):
    """
    Convergência de 3 fatores:
    1. Excesso
    2. Empate
    3. Pressão
    """
    pontos = {"R":0,"B":0}

    ult = h[-10:]
    cont = Counter(ult)

    # Excesso
    if cont["R"] >= 5: pontos["B"] += 1
    if cont["B"] >= 5: pontos["R"] += 1

    # Empate como corte
    if ult[-1] == "E":
        if ult[-2] == "R": pontos["B"] += 1
        if ult[-2] == "B": pontos["R"] += 1

    # Pressão psicológica
    if cont["R"] > cont["B"]: pontos["B"] += 1
    if cont["B"] > cont["R"]: pontos["R"] += 1

    return pontos

def decisao_final(h):
    macro = detectar_macro_padrao(h)
    nivel = nivel_manipulacao(h)
    quântico = leitura_quântica(h)
    falso = falso_padrao(h)

    if macro == "Empate Duplo (Limpeza)":
        return "⛔ PAUSAR", "Limpeza total detectada", 92

    if nivel >= 8:
        return "⏳ AGUARDAR", "Manipulação extrema", 88

    if falso:
        return "🔄 CONTRARIAR", "Falso padrão identificado", 82

    if quântico["R"] >= 2:
        return "▶️ ENTRAR 🔴", "Convergência quântica", 79

    if quântico["B"] >= 2:
        return "▶️ ENTRAR 🔵", "Convergência quântica", 79

    return "⏳ AGUARDAR", "Sem convergência clara", 65

# =========================
# INSERÇÃO MANUAL
# =========================
st.subheader("Inserir Resultado (Mesa Real)")

c1,c2,c3 = st.columns(3)

with c1:
    if st.button("🔴 Vermelho"):
        st.session_state.h.append("R")
with c2:
    if st.button("🔵 Azul"):
        st.session_state.h.append("B")
with c3:
    if st.button("🟡 Empate"):
        st.session_state.h.append("E")

st.session_state.h = limite_hist(st.session_state.h)

# =========================
# HISTÓRICO VISUAL
# =========================
st.subheader("Histórico")
def render(h):
    mapa = {"R":"🔴","B":"🔵","E":"🟡"}
    linhas = [h[i:i+9] for i in range(0,len(h),9)]
    for l in linhas:
        st.write(" ".join(mapa[x] for x in l))

render(st.session_state.h)

# =========================
# PAINEL IA
# =========================
if len(st.session_state.h) >= 6:
    st.divider()
    st.subheader("🧠 Análise Profissional")

    macro = detectar_macro_padrao(st.session_state.h)
    nivel = nivel_manipulacao(st.session_state.h)
    acao, motivo, conf = decisao_final(st.session_state.h)

    st.write(f"**Macro Padrão:** {macro}")
    st.write(f"**Manipulação:** {nivel}/9")
    st.write(f"**Decisão IA:** {acao}")
    st.write(f"**Motivo:** {motivo}")
    st.write(f"**Confiança:** {conf}%")

# =========================
# RESET
# =========================
if st.button("♻️ Resetar Mesa"):
    st.session_state.h = []
