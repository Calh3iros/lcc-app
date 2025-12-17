import streamlit as st
import requests
import json

# Configuração da Página
st.set_page_config(page_title="L.C.C.", page_icon="🏆", layout="centered")

st.title("🏆 L.C.C.")
st.subheader("Liste. Compare. Classifique.")
st.markdown("---")

# Pega a chave
api_key = st.secrets["GEMINI_API_KEY"]

# Prompt Mestre
PROMPT_MESTRE = """
Você é o L.C.C. (Liste, Compare, Classifique), uma IA especialista em curadoria.
Responda SEMPRE em Português do Brasil seguindo esta estrutura:
### 1. LISTE (Os Finalistas)
### 2. COMPARE (Tabela Markdown)
### 3. CLASSIFIQUE (O Pódio com Medalhas 🥇🥈🥉)
Seja direto e use formatação rica.
"""

# Input do usuário
usuario_input = st.chat_input("O que você precisa decidir hoje?")

if usuario_input:
    with st.chat_message("user"):
        st.write(usuario_input)

    with st.chat_message("assistant"):
        with st.spinner("O Robô está pensando (Via Conexão Direta)..."):
            try:
                # CONEXÃO DIRETA (SEM BIBLIOTECA BUGADA)
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
                
                headers = {"Content-Type": "application/json"}
                payload = {
                    "contents": [{
                        "parts": [{"text": f"{PROMPT_MESTRE}\n\nPERGUNTA: {usuario_input}"}]
                    }]
                }

                # Dispara a requisição
                response = requests.post(url, headers=headers, json=payload)

                if response.status_code == 200:
                    resultado = response.json()
                    texto_final = resultado['candidates'][0]['content']['parts'][0]['text']
                    st.markdown(texto_final)
                else:
                    st.error(f"Erro no Google: {response.text}")

            except Exception as e:
                st.error(f"Erro técnico: {e}")
