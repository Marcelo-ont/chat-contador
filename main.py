import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="Chat Contador de Palabras", page_icon="🐼")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
system_message = (
    "Eres un contador de palabras. Analiza solo el último mensaje del usuario. "
    "Responde únicamente con las palabras que se repiten más de una vez en formato "
    "'palabra: conteo' separadas por comas. "
    "Si ninguna se repite responde exactamente 'Ninguna palabra se repite.' "
    "No añadas más texto ni explicaciones."
)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Escribe un texto y te diré qué palabras se repiten y cuántas veces.",
        }
    ]
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

prompt = st.chat_input("Escribe un texto para contar repeticiones")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        response = client.chat.completions.create(
            model="chatgpt-4o-latest",
            temperature=0,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt},
            ],
        )
        reply_text = response.choices[0].message.content.strip()
    except Exception:
        reply_text = "Error al llamar a ChatGPT."

    st.session_state.messages.append({"role": "assistant", "content": reply_text})
    with st.chat_message("assistant"):
        st.markdown(reply_text)
