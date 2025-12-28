import streamlit as st
from collections import Counter

st.set_page_config(page_title="Football Studio IA Avançada", layout="centered")
st.title("🧠 Football Studio – IA Nível Avançado")

# =====================================================
# ESTADO
# =====================================================
if "h" not in st.session_state:
    st.session_state.h = []  # índice 0 = MAIS RECENTE

# =====================================================
# INSERÇÃO MANUAL
# =====================================================
st.subheader("Inserir Resultado")

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

st.session_state.h = st.session_state.h[:120]

# =====================================================
# HISTÓRICO VISUAL (MESA REAL)
# =====================================================
st.subheader("Histórico (Mais recente → Mais antigo)")

def render(h):
    mapa = {"R":"🔴","B":"🔵","E":"🟡"}
    for i in range(0, len(h), 9):
        st.write(" ".join(mapa[x] for x in h[i:i+9]))

render(st.session_state.h)

# =====================================================
# MOTOR 1 — LEITURA DE PADRÕES
# =====================================================
def detectar_padroes(h):
    p = []
    u = h[:8]

    if len(u) < 6:
        return p

    # Alternância
    if u[:4] in (["R","B","R","B"], ["B","R","B","R"]):
        p.append(("Alternância longa", "neutro", 20))

    if u[0] != u[1] and u[1] != u[2]:
        p.append(("Alternância curta", "seguir", 15))

    # Repetição
    if u[0] == u[1]:
        p.append(("Repetição dupla", "seguir", 10))

    if u[:3].count(u[0]) == 3:
        p.append(("Repetição tripla", "neutro", 18))

    # Saturação
    if u[:5].count("R") >= 4:
        p.append(("Saturação Vermelho", "contrariar", 30))

    if u[:5].count("B") >= 4:
        p.append(("Saturação Azul", "contrariar", 30))

    # Empate
    if u[0] == "E":
        p.append(("Empate âncora", "contrariar", 25))

    if u[0] == "E" and u[1] == "E":
        p.append(("Empate duplo (limpeza)", "bloqueio", 50))

    # Manipulação
    if u.count("R") == u.count("B") and "E" not in u:
        p.append(("Simetria forçada", "armadilha", 40))

    return p

# =====================================================
# MOTOR 2 — FORÇA DO PADRÃO
# =====================================================
def calcular_forca(padroes):
    forca = sum(p[2] for p in padroes)
    return min(forca, 100)

# =====================================================
# MOTOR 3 — DETECTOR DE ARMADILHA
# =====================================================
def armadilha_ativa(padroes):
    for p in padroes:
        if "armadilha" in p[1] or "bloqueio" in p[1]:
            return True
    return False

# =====================================================
# MOTOR 4 — DECISÃO FINAL
# =====================================================
def decidir(h, padroes):
    score = {"R":0, "B":0}

    for nome, tipo, peso in padroes:
        if tipo == "seguir":
            score[h[0]] += peso

        if tipo == "contrariar":
            score["B" if h[0]=="R" else "R"] += peso

    forca = calcular_forca(padroes)
    trap = armadilha_ativa(padroes)

    return score, forca, trap

# =====================================================
# PAINEL AVANÇADO
# =====================================================
if len(st.session_state.h) >= 6:
    st.divider()
    st.subheader("🧠 Painel Avançado de Leitura")

    padroes = detectar_padroes(st.session_state.h)
    score, forca, trap = decidir(st.session_state.h, padroes)

    st.write("### Padrões Detectados")
    for nome, tipo, peso in padroes:
        st.write(f"• **{nome}** | ação: `{tipo}` | peso: {peso}")

    st.write("### Métricas")
    st.write(f"🔥 Força do Padrão: **{forca}/100**")
    st.write(f"⚠️ Armadilha ativa: **{trap}**")

    st.write("### Pontuação")
    st.write(f"🔴 Vermelho: {score['R']}")
    st.write(f"🔵 Azul: {score['B']}")

    if trap or forca < 65:
        st.error("⛔ ENTRADA BLOQUEADA (Manipulação ou força insuficiente)")
    else:
        lado = "🔴 Vermelho" if score["R"] > score["B"] else "🔵 Azul"
        st.success(f"▶️ ENTRAR EM {lado} | Confiança: {forca}%")

# =====================================================
# RESET
# =====================================================
if st.button("♻️ Resetar Mesa"):
    st.session_state.h = []
