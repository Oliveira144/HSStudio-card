import streamlit as st

st.set_page_config(page_title="Football Studio - Padrões Reais", layout="wide")

# =====================
# ESTADO
# =====================
if "history" not in st.session_state:
    st.session_state.history = []

# =====================
# FUNÇÕES BÁSICAS
# =====================
def add_result(result):
    st.session_state.history.insert(0, result)

def reset():
    st.session_state.history = []

def chunk_history(hist, size=9):
    return [hist[i:i + size] for i in range(0, len(hist), size)]

# =====================
# MOTOR DE PADRÕES
# =====================
def analyze(history):
    if len(history) < 4:
        return "Dados insuficientes", "Aguardando formação", "AGUARDAR"

    recent = history[:6]
    last = recent[0]

    # 1️⃣ Extensão
    if last != "🟡" and recent.count(last) >= 4:
        return "Extensão", "Sequência longa perigosa", "RISCO ALTO"

    # 2️⃣ Repetição curta
    if recent[0] == recent[1] and recent[0] != "🟡":
        return "Repetição curta", "Continuação provável", f"ENTRAR {recent[0]} (stake baixa)"

    # 3️⃣ Alternância
    alterna = True
    for i in range(len(recent) - 1):
        if recent[i] == recent[i + 1]:
            alterna = False
            break
    if alterna:
        lado = "🔴" if last == "🔵" else "🔵"
        return "Alternância", "Mesa equilibrada", f"ENTRAR {lado}"

    # 4️⃣ Empate como âncora
    if last == "🟡":
        prev = history[1]
        return "Empate âncora", "Tendência de repetição", f"ENTRAR {prev}"

    # 5️⃣ Quebra de extensão
    if history[0] != history[1] and history[1] == history[2] == history[3]:
        return "Quebra de extensão", "Correção detectada", f"ENTRAR {history[0]}"

    # 6️⃣ Compressão
    if "🟡" in recent and recent.count("🔴") == recent.count("🔵"):
        return "Compressão", "Mesa travada", "AGUARDAR"

    # 7️⃣ Falso padrão
    if recent[:5].count("🔴") == 3 and recent[:5].count("🔵") == 2:
        return "Falso padrão", "Quebra iminente", "AGUARDAR"

    # 8️⃣ Zona neutra
    return "Zona neutra", "Sem padrão confiável", "AGUARDAR"

# =====================
# INTERFACE
# =====================
st.title("⚽ Football Studio – Análise de Padrões Reais (Cartas Físicas)")

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("🔴 Player"):
        add_result("🔴")

with col2:
    if st.button("🔵 Banker"):
        add_result("🔵")

with col3:
    if st.button("🟡 Empate"):
        add_result("🟡")

with col4:
    if st.button("♻️ Reset"):
        reset()

st.divider()

# =====================
# HISTÓRICO
# =====================
st.subheader("📊 Histórico (mais recente à esquerda)")
chunks = chunk_history(st.session_state.history)

for row in chunks:
    st.write(" ".join(row))

# =====================
# ANÁLISE
# =====================
padrao, estado, sugestao = analyze(st.session_state.history)

st.divider()
st.subheader("🧠 Leitura da Mesa")

st.write(f"**Padrão identificado:** {padrao}")
st.write(f"**Estado da mesa:** {estado}")
st.write(f"**Sugestão:** {sugestao}")

st.caption("⚠️ App de leitura estatística. Não garante ganhos. Use gestão.")
