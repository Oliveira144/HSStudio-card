import streamlit as st

# =====================
# CONFIGURAÇÃO
# =====================
st.set_page_config(
    page_title="Football Studio - Padrões Reais",
    layout="wide"
)

# Evita quebra visual por erro de front
st.set_option("client.showErrorDetails", False)

# =====================
# ESTADO
# =====================
if "history" not in st.session_state:
    st.session_state.history = []

# =====================
# FUNÇÕES BÁSICAS
# =====================
def add_result(result):
    # Mais recente sempre à esquerda
    st.session_state.history.insert(0, result)

def reset():
    st.session_state.history = []

def chunk_history(hist, size=9):
    return [hist[i:i + size] for i in range(0, len(hist), size)]

# =====================
# MOTOR DE PADRÕES (OFICIAL)
# =====================
def analyze(history):
    if len(history) < 4:
        return "Dados insuficientes", "Aguardando formação", "AGUARDAR"

    recent = history[:6]
    last = recent[0]

    # 1️⃣ EXTENSÃO
    if last != "🟡" and recent.count(last) >= 4:
        lado = "BANQUEIRO 🔴" if last == "🔴" else "JOGADOR 🔵"
        return "Extensão", f"Sequência longa de {lado}", "RISCO ALTO"

    # 2️⃣ REPETIÇÃO CURTA
    if recent[0] == recent[1] and recent[0] != "🟡":
        lado = "BANQUEIRO 🔴" if recent[0] == "🔴" else "JOGADOR 🔵"
        return "Repetição curta", "Continuação provável", f"ENTRAR {lado} (stake baixa)"

    # 3️⃣ ALTERNÂNCIA
    alterna = True
    for i in range(len(recent) - 1):
        if recent[i] == recent[i + 1]:
            alterna = False
            break

    if alterna:
        if last == "🔴":
            return "Alternância", "Mesa equilibrada", "ENTRAR JOGADOR 🔵"
        if last == "🔵":
            return "Alternância", "Mesa equilibrada", "ENTRAR BANQUEIRO 🔴"

    # 4️⃣ EMPATE COMO ÂNCORA
    if last == "🟡" and len(history) > 1:
        prev = history[1]
        lado = "BANQUEIRO 🔴" if prev == "🔴" else "JOGADOR 🔵"
        return "Empate âncora", "Tendência de repetição do lado anterior", f"ENTRAR {lado}"

    # 5️⃣ QUEBRA DE EXTENSÃO
    if (
        len(history) >= 4
        and history[0] != history[1]
        and history[1] == history[2] == history[3]
    ):
        lado = "BANQUEIRO 🔴" if history[0] == "🔴" else "JOGADOR 🔵"
        return "Quebra de extensão", "Correção detectada", f"ENTRAR {lado}"

    # 6️⃣ COMPRESSÃO
    if "🟡" in recent and recent.count("🔴") == recent.count("🔵"):
        return "Compressão", "Mesa travada / sem dominância", "AGUARDAR"

    # 7️⃣ FALSO PADRÃO
    if recent[:5].count("🔴") == 3 and recent[:5].count("🔵") == 2:
        return "Falso padrão", "Possível armadilha", "AGUARDAR"

    # 8️⃣ ZONA NEUTRA
    return "Zona neutra", "Sem padrão confiável", "AGUARDAR"

# =====================
# INTERFACE
# =====================
st.title("⚽ Football Studio – Análise de Padrões Reais")
st.caption("🔵 Jogador | 🔴 Banqueiro | 🟡 Empate")

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("🔵 Jogador"):
        add_result("🔵")

with col2:
    if st.button("🔴 Banqueiro"):
        add_result("🔴")

with col3:
    if st.button("🟡 Empate"):
        add_result("🟡")

with col4:
    if st.button("♻️ Reset"):
        reset()

st.divider()

# =====================
# HISTÓRICO (ESTÁVEL)
# =====================
st.subheader("📊 Histórico (mais recente à esquerda)")

with st.container():
    chunks = chunk_history(st.session_state.history)
    for row in chunks:
        st.markdown(" ".join(row))

# =====================
# ANÁLISE
# =====================
padrao, estado, sugestao = analyze(st.session_state.history)

st.divider()
st.subheader("🧠 Leitura da Mesa")

st.write(f"**Padrão identificado:** {padrao}")
st.write(f"**Estado da mesa:** {estado}")
st.write(f"**Sugestão:** {sugestao}")

st.caption("⚠️ Leitura estatística. Não existe garantia de ganho. Use gestão.")
