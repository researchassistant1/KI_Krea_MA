import streamlit as st
import openai
import os
import requests  # Zum Senden der Daten an Google Sheets

# 🔹 Hole den API-Key aus den Umgebungsvariablen (GitHub Secrets oder Streamlit Secrets)
openai.api_key = os.getenv("OPENAI_API_KEY")

# 🔹 Google Apps Script API-URL & Sheet-ID für die Datenspeicherung
google_script_url = "https://script.google.com/macros/s/AKfycbwmixSK9TMI2RyAWTutomNZ5DofoefLKBpicVSx-TxAOhPZ8FlHXJE1oRiwp2p67-oRtA/exec
"  # ⬅️ Ersetze mit deiner Google Apps Script URL
google_sheet_id = "1cm8m01Rqe0FVEBZVkFjQbq_kEdrIuYQK1XplqZnkkWk"  # ⬅️ Ersetze mit deiner Google Sheets ID

st.title("Du kannst nur einen Prompt verwenden, also wähle deine Worte weise.")

if "used_prompt" not in st.session_state:
    st.session_state.used_prompt = False

# Eingabefeld für den Prompt
prompt = st.text_input("Gib deinen Prompt ein:", disabled=st.session_state.used_prompt)

if st.button("Senden") and prompt and not st.session_state.used_prompt:
    response = openai.ChatCompletion.create(
        model="gpt-4",  # Falls du GPT-3.5-Turbo statt GPT-4 nutzen willst, hier ändern
        messages=[{"role": "user", "content": prompt}]
    )
    ki_text = response["choices"][0]["message"]["content"]

    # Zeige die KI-Antwort an
    st.write("**KI-Generierter Text:**")
    st.write(ki_text)
    st.session_state.used_prompt = True  # Verhindert weiteres Prompten

    # 🔹 Senden der Daten an Google Sheets
    data = {"prompt": prompt, "ki_text": ki_text, "sheetID": google_sheet_id}
    response = requests.post(google_script_url, json=data)

    if response.status_code == 200:
        st.success("Deine Daten wurden gespeichert! ✅")
    else:
        st.error("Fehler beim Speichern der Daten. ❌")

# 🔹 Link zur SoSci Survey Umfrage anpassen
if st.session_state.used_prompt:
    st.markdown("[Zurück zur Umfrage](https://deine-umfrage.com)")  # ⬅️ Ersetze mit deiner SoSci Survey URL
