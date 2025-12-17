import streamlit as st
import requests
import json

# Configuração da Página
st.set_page_config(page_title="L.C.C.", page_icon="🏆", layout="centered")

st.title("🏆 L.C.C.")
st.subheader("Liste. Compare. Classifique.")
st.markdown("---")

# Pega a chave dos segredos
api_key = st.secrets["GEMINI_API_KEY"]

# Prompt Mestre
PROMPT_MESTRE = """
Você é o L.C.C. (Liste, Compare, Classifique), uma IA especialista em curadoria.
Responda SEMPRE em Português do Brasil seguindo esta estrutura:

### 1. LISTE (Os Finalistas)
- Liste 3 opções.

### 2. COMPARE (Tabela Markdown)
- Tabela com Nome, Preço Estimado e Ponto Forte.

### 3. CLASSIFIQUE (O Pódio)
- 🥇 **MEDALHA DE OURO:** [Nome] - [Motivo]
- 🥈 **MEDALHA DE PRATA:** [Nome] - [Motivo]
- 🥉 **MEDALHA DE BRONZE:** [Nome] - [Motivo]

Seja direto.
"""

usuario_input = st.chat_input("O que você precisa decidir hoje?")

if usuario_input:
    with st.chat_message("user"):
        st.write(usuario_input)

    with st.chat_message("assistant"):
        with st.spinner("Consultando o Oráculo..."):
            try:
                # URL DA VERSÃO ESTÁVEL (V1) - ESSA NÃO FALHA
                url = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={api_key}"
                
                headers = {"Content-Type": "application/json"}
                payload = {
                    "contents": [{
                        "parts": [{"text": f"{PROMPT_MESTRE}\n\nPERGUNTA: {usuario_input}"}]
                    }]
                }

                response = requests.post(url, headers=headers, json=payload)

                if response.status_code == 200:
                    resultado = response.json()
                    # Tratamento de erro caso o modelo bloqueie a resposta
                    if 'candidates' in resultado and resultado['candidates']:
                        texto = resultado['candidates'][0]['content']['parts'][0]['text']
                        st.markdown(texto)
                    else:
                        st.error("O modelo não retornou resposta (Bloqueio de segurança ou erro interno). Tente outra pergunta.")
                else:
                    st.error(f"Erro no Google: {response.status_code} - {response.text}")

            except Exception as e:
                st.error(f"Erro técnico: {e}")
