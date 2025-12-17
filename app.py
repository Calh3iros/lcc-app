import streamlit as st
import google.generativeai as genai

# Configuração da Página (Design Minimalista e Escuro)
st.set_page_config(
    page_title="L.C.C. - Decisor Inteligente",
    page_icon="🏆",
    layout="centered"
)

# Título e Subtítulo
st.title("🏆 L.C.C.")
st.subheader("Liste. Compare. Classifique.")
st.markdown("---")

# Captura a Chave da API (Segredo)
api_key = st.secrets["GEMINI_API_KEY"]

if not api_key:
    st.error("Chave da API não encontrada. Configure os 'Secrets' no Streamlit.")
    st.stop()

# Configura o Modelo Gemini
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-pro')

# O Prompt Mestre (A Alma do Negócio)
PROMPT_MESTRE = """
Você é o L.C.C. (Liste, Compare, Classifique), uma IA especialista em curadoria de produtos e serviços.
Sua missão é eliminar a paralisia da escolha do usuário.
Você deve responder SEMPRE em Português do Brasil, seguindo RIGOROSAMENTE a estrutura abaixo:

ESTRUTURA DA RESPOSTA:

### 1. LISTE (Os Finalistas)
- Liste de 3 a 5 opções relevantes.
- Breve descrição de cada uma.

### 2. COMPARE (Tabela)
- Crie uma tabela Markdown comparando: Nome, Preço Estimado (R$), Ponto Forte, Ponto Fraco.

### 3. CLASSIFIQUE (O Pódio)
- Use Emojis de medalhas.
- 🥇 **MEDALHA DE OURO:** [Nome] - O Veredito: [Por que vence].
- 🥈 **MEDALHA DE PRATA:** [Nome] - O Veredito: [Por que é a segunda opção].
- 🥉 **MEDALHA DE BRONZE:** [Nome] - O Veredito: [Para quem serve].

REGRAS:
- Seja direto, autoritário e imparcial.
- Se for produto, inclua um link de busca genérico (ex: Busca Amazon).
- Use formatação Markdown (negrito, tabelas) para facilitar a leitura.
"""

# Campo de Busca do Usuário
usuario_input = st.chat_input("O que você precisa decidir hoje? (Ex: Melhor notebook até 3k)")

# Processamento
if usuario_input:
    # Mostra a pergunta do usuário
    with st.chat_message("user"):
        st.write(usuario_input)

    # Mostra a resposta da IA
    with st.chat_message("assistant"):
        with st.spinner("Analisando o mercado... Consultando especialistas..."):
            try:
                # Monta a requisição completa
                full_prompt = f"{PROMPT_MESTRE}\n\nPERGUNTA DO USUÁRIO: {usuario_input}"
                
                # Chama a API
                response = model.generate_content(full_prompt)
                
                # Exibe o resultado
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Erro ao processar: {e}")
