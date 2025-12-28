import streamlit as st
from collections import Counter

# =====================================================
# CONFIGURAÇÃO
# =====================================================
st.set_page_config(page_title="Football Studio IA Profissional", layout="centered")
st.title("🧠 Football Studio – Leitura Profissional Completa")

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
    mapa = {"R": "🔴", "B": "🔵", "E": "🟡"}
    for i in range(0, len(h), 9):
        st.write(" ".join(mapa[x] for x in h[i:i+9]))

render(st.session_state.h)

# =====================================================
# LEITURA DE EMPATE (ESSENCIAL)
# =====================================================
def leitura_empate(h):
    if h[0] != "E":
        return None

    if len(h) > 1 and h[1] == "E":
        return ("Empate duplo (limpeza)", "pausa", 30)

    if len(h) > 2 and h[1] == h[2] and h[1] != "E":
        return ("Empate de corte", "contrariar", 25)

    if h[:6].count("R") >= 4:
        return ("Empate pós-saturação Vermelho", "contrariar", 28)

    if h[:6].count("B") >= 4:
        return ("Empate pós-saturação Azul", "contrariar", 28)

    return ("Empate âncora", "contrariar", 18)

# =====================================================
# PADRÕES DE COR
# =====================================================
def detectar_padroes(h):
    p = []
    u = h[:8]

    if len(u) < 4:
        return p

    if u[:4] in (["R","B","R","B"], ["B","R","B","R"]):
        p.append(("Alternância longa", "neutro", 15))

    if u[0] != u[1] and u[1] != u[2]:
        p.append(("Alternância curta", "seguir", 12))

    if u[0] == u[1] and u[0] != "E":
        p.append(("Repetição dupla", "seguir", 10))

    if u[:3].count(u[0]) == 3 and u[0] != "E":
        p.append(("Repetição tripla", "neutro", 15))

    if u[:5].count("R") >= 4:
        p.append(("Saturação Vermelho", "contrariar", 22))

    if u[:5].count("B") >= 4:
        p.append(("Saturação Azul", "contrariar", 22))

    if u.count("R") == u.count("B") and "E" not in u:
        p.append(("Simetria forçada", "alerta", 20))

    return p

# =====================================================
# DECISÃO FINAL (EMPATE MANDA NA MESA)
# =====================================================
def decidir(h):
    score = {"R": 0, "B": 0}
    alertas = []
    padroes = detectar_padroes(h)

    for nome, tipo, peso in padroes:
        if tipo == "seguir":
            score[h[0]] += peso
        if tipo == "contrariar":
            score["B" if h[0] == "R" else "R"] += peso
        if tipo == "alerta":
            alertas.append(nome)

    # Empate redefine leitura
    if h[0] == "E":
        nome, tipo, peso = leitura_empate(h)
        alertas.append(nome)

        if tipo == "contrariar" and len(h) > 1:
            base = h[1]
            if base in ("R","B"):
                score["B" if base == "R" else "R"] += peso

    # Micro-tendência como fallback
    if abs(score["R"] - score["B"]) < 8:
        ult = [x for x in h[:10] if x != "E"]
        if ult:
            score[Counter(ult).most_common(1)[0][0]] += 6

    lado = "R" if score["R"] >= score["B"] else "B"
    confianca = min(abs(score["R"] - score["B"]) + 40, 100)

    return lado, score, confianca, alertas

# =====================================================
# PAINEL DE LEITURA
# =====================================================
if len(st.session_state.h) >= 4:
    st.divider()
    st.subheader("🧠 Leitura Profissional da Mesa")

    lado, score, confianca, alertas = decidir(st.session_state.h)

    st.write("### Pontuação")
    st.write(f"🔴 Vermelho: {score['R']}")
    st.write(f"🔵 Azul: {score['B']}")

    st.success(f"▶️ Sugestão: {'🔴 Vermelho' if lado=='R' else '🔵 Azul'}")
    st.write(f"**Confiança:** {confianca}%")

    if confianca < 50:
        st.warning("⚠️ Risco alto — mesa instável / empate recente")
    elif confianca < 70:
        st.info("ℹ️ Risco médio")
    else:
        st.success("🔥 Risco baixo")

    if alertas:
        st.error("🚨 Alertas de mesa:")
        for a in alertas:
            st.write(f"• {a}")

# =====================================================
# RESET
# =====================================================
if st.button("♻️ Resetar Mesa"):
    st.session_state.h = []
