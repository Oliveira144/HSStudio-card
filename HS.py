import streamlit as st
from collections import Counter

# =====================================================
# CONFIGURAÇÃO
# =====================================================
st.set_page_config(page_title="Football Studio IA Profissional", layout="centered")
st.title("🧠 Football Studio – Leitura Profissional Evoluída")

# =====================================================
# ESTADO
# =====================================================
if "h" not in st.session_state:
    st.session_state.h = []

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
# HISTÓRICO
# =====================================================
st.subheader("Histórico (Mais recente → Mais antigo)")

def render(h):
    mapa = {"R":"🔴","B":"🔵","E":"🟡"}
    for i in range(0, len(h), 9):
        st.write(" ".join(mapa[x] for x in h[i:i+9]))

render(st.session_state.h)

# =====================================================
# MICRO-TENDÊNCIA (NOVO)
# =====================================================
def micro_tendencia(h):
    ult = h[:10]
    c = Counter([x for x in ult if x != "E"])
    if not c:
        return None
    return c.most_common(1)[0][0]

# =====================================================
# PADRÕES PRINCIPAIS
# =====================================================
def detectar_padroes(h):
    u = h[:8]
    p = []

    if len(u) < 4:
        return p

    if u[:4] in (["R","B","R","B"], ["B","R","B","R"]):
        p.append(("Alternância longa", "neutro", 15))

    if u[0] != u[1] and u[1] != u[2]:
        p.append(("Alternância curta", "seguir", 12))

    if u[0] == u[1]:
        p.append(("Repetição dupla", "seguir", 10))

    if u[:3].count(u[0]) == 3:
        p.append(("Repetição tripla", "neutro", 15))

    if u[:5].count("R") >= 4:
        p.append(("Saturação Vermelho", "contrariar", 20))

    if u[:5].count("B") >= 4:
        p.append(("Saturação Azul", "contrariar", 20))

    if u[0] == "E":
        p.append(("Empate âncora", "contrariar", 18))

    if u.count("R") == u.count("B") and "E" not in u:
        p.append(("Simetria forçada", "alerta", 25))

    return p

# =====================================================
# QUEBRA IMINENTE (NOVO)
# =====================================================
def quebra_iminente(h):
    ult = h[:6]
    if ult.count("R") >= 5:
        return "Vermelho saturado"
    if ult.count("B") >= 5:
        return "Azul saturado"
    if ult[:4] in (["R","B","R","B"], ["B","R","B","R"]):
        return "Alternância esticada"
    return None

# =====================================================
# DECISÃO FINAL
# =====================================================
def decidir(h, padroes):
    score = {"R": 0, "B": 0}
    alertas = []

    for nome, tipo, peso in padroes:
        if tipo == "seguir":
            score[h[0]] += peso
        if tipo == "contrariar":
            score["B" if h[0] == "R" else "R"] += peso
        if tipo == "alerta":
            alertas.append(nome)

    # Micro-tendência entra só se score estiver baixo
    if abs(score["R"] - score["B"]) < 10:
        mt = micro_tendencia(h)
        if mt:
            score[mt] += 8

    confianca = min(sum(p[2] for p in padroes) + 20, 100)

    lado = "R" if score["R"] >= score["B"] else "B"
    return lado, score, confianca, alertas

# =====================================================
# PAINEL IA
# =====================================================
if len(st.session_state.h) >= 4:
    st.divider()
    st.subheader("🧠 Leitura Profissional")

    padroes = detectar_padroes(st.session_state.h)
    lado, score, confianca, alertas = decidir(st.session_state.h, padroes)
    quebra = quebra_iminente(st.session_state.h)

    st.write("### Padrões Detectados")
    if padroes:
        for n, t, p in padroes:
            st.write(f"• **{n}** | {t} | peso {p}")
    else:
        st.write("• Leitura por micro-tendência")

    st.write("### Pontuação")
    st.write(f"🔴 Vermelho: {score['R']}")
    st.write(f"🔵 Azul: {score['B']}")

    st.success(f"▶️ Sugestão: {'🔴 Vermelho' if lado=='R' else '🔵 Azul'}")
    st.write(f"**Confiança:** {confianca}%")

    if confianca < 45:
        st.warning("⚠️ Risco alto (mesa instável)")
    elif confianca < 70:
        st.info("ℹ️ Risco médio")
    else:
        st.success("🔥 Risco baixo")

    if alertas:
        st.error(f"🚨 Alerta: {', '.join(alertas)}")

    if quebra:
        st.warning(f"💣 Quebra iminente detectada: {quebra}")

# =====================================================
# RESET
# =====================================================
if st.button("♻️ Resetar Mesa"):
    st.session_state.h = []
