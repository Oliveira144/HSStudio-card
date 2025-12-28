import streamlit as st
from collections import Counter

st.set_page_config("Football Studio IA Avançada", layout="centered")
st.title("🧠 Football Studio – IA Profissional de Padrões")

# ======================================================
# ESTADO
# ======================================================
if "h" not in st.session_state:
    st.session_state.h = []  # índice 0 = MAIS RECENTE

# ======================================================
# INSERÇÃO
# ======================================================
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

# ======================================================
# HISTÓRICO (MESA REAL)
# ======================================================
st.subheader("Histórico (Mais recente → Mais antigo)")

def render(h):
    mapa = {"R": "🔴", "B": "🔵", "E": "🟡"}
    for i in range(0, len(h), 9):
        st.write(" ".join(mapa[x] for x in h[i:i+9]))

render(st.session_state.h)

# ======================================================
# IDENTIFICAÇÃO DE SURF
# ======================================================
def detectar_surf(h):
    cor = h[0]
    if cor == "E":
        return None

    count = 0
    for x in h:
        if x == cor:
            count += 1
        else:
            break

    if count >= 4:
        return ("Surf longo", "seguir", 30)
    if count == 3:
        return ("Surf médio", "seguir", 22)
    if count == 2:
        return ("Surf curto", "seguir", 14)

    return None

# ======================================================
# PADRÕES DE EMPATE
# ======================================================
def detectar_empate(h):
    if h[0] != "E":
        return None

    if len(h) > 2 and h[1] == "E" and h[2] == "E":
        return ("Empate triplo – mesa morta", "pausa", 0)

    if len(h) > 1 and h[1] == "E":
        return ("Empate duplo", "pausa", 0)

    ult = h[1:6]
    if ult.count("R") >= 4 or ult.count("B") >= 4:
        return ("Empate pós-surf", "contrariar", 28)

    return ("Empate âncora", "contrariar", 20)

# ======================================================
# PADRÕES GERAIS
# ======================================================
def detectar_padroes(h):
    padroes = []

    surf = detectar_surf(h)
    if surf:
        padroes.append(surf)

    if h[0] == "E":
        padroes.append(detectar_empate(h))
        return padroes

    u = h[:6]

    if u[:4] in (["R","B","R","B"], ["B","R","B","R"]):
        padroes.append(("Alternância longa", "neutro", 12))

    if u.count("R") == u.count("B"):
        padroes.append(("Simetria forçada", "alerta", 18))

    if len(set(u)) == 3:
        padroes.append(("Mesa em transição", "cautela", 10))

    return padroes

# ======================================================
# DECISÃO FINAL
# ======================================================
def decidir(h):
    score = {"R": 0, "B": 0}
    leitura = []
    acao = "Aguardar"

    padroes = detectar_padroes(h)

    for nome, tipo, peso in padroes:
        leitura.append(nome)

        if tipo == "seguir" and h[0] in ("R","B"):
            score[h[0]] += peso

        if tipo == "contrariar":
            base = h[1] if h[0] == "E" else h[0]
            if base in ("R","B"):
                score["B" if base == "R" else "R"] += peso

        if tipo in ("pausa", "cautela"):
            acao = "PAUSAR"

    if acao == "PAUSAR":
        return None, score, leitura, "PAUSAR"

    lado = "R" if score["R"] >= score["B"] else "B"
    return lado, score, leitura, "ENTRAR"

# ======================================================
# PAINEL
# ======================================================
if len(st.session_state.h) >= 4:
    st.divider()
    st.subheader("🧠 Leitura da Mesa")

    lado, score, leitura, acao = decidir(st.session_state.h)

    st.write("### Padrões Detectados:")
    for l in leitura:
        st.write(f"• {l}")

    st.write("### Pontuação")
    st.write(f"🔴 Vermelho: {score['R']}")
    st.write(f"🔵 Azul: {score['B']}")

    if acao == "PAUSAR":
        st.error("⛔ PAUSAR – Mesa travada ou empate dominante")
    else:
        st.success(f"▶️ Sugestão: {'🔴 Vermelho' if lado=='R' else '🔵 Azul'}")

# ======================================================
# RESET
# ======================================================
if st.button("♻️ Resetar Mesa"):
    st.session_state.h = []
