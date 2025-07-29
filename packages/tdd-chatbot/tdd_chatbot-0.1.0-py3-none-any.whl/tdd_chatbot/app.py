import streamlit as st
import speech_recognition as sr
import pyttsx3
import requests
from langdetect import detect

# Streamlit UI setup
st.set_page_config(page_title="Ollama Voice Q&A Bot", layout="centered")
st.title("🎙️ Ask Your Question by Voice (Ollama + Streamlit)")

# Text-to-speech function
def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.say(text)
    engine.runAndWait()

# Voice-to-text (STT) using SpeechRecognition
def get_voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening for your question (max 5 seconds)...")
        audio = recognizer.listen(source, phrase_time_limit=5)

    try:
        question = recognizer.recognize_google(audio)
        return question
    except sr.UnknownValueError:
        return "Sorry, I couldn't understand the audio."
    except sr.RequestError:
        return "Speech recognition service is unavailable."

# Send question to Ollama (LLM)
def generate_answer_with_ollama(question):
    system_prompt = (
        "You are a helpful assistant that answers only questions related to data science. "
        "If the question is not related to data science, politely say you can only answer data science questions."
    )

    try:
        full_prompt = f"{system_prompt}\n\nQuestion: {question}"
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "mistral", "prompt": full_prompt, "stream": False}
        )
        result = response.json()
        return result["response"]
    except Exception as e:
        return f"Error communicating with Ollama: {e}"

# Main interaction
if st.button("🎤 Ask Your Question"):
    question = get_voice_input()
    st.subheader("🗣️ You asked:")
    st.write(question)

    try:
        language = detect(question)
        if language != "en":
            st.warning("Please ask your question in English.")
            speak("Please ask your question in English.")
        elif "Sorry" in question:
            st.warning("Could not understand your voice input.")
            speak("Sorry, I couldn't understand your question.")
        else:
            answer = generate_answer_with_ollama(question)
            st.subheader("🤖 Chatbot's Answer:")
            st.write(answer)
            speak(answer)
    except Exception as e:
        st.error("Something went wrong.")
        speak("Sorry, something went wrong.")



#=============================================================================================================================
# TDD Testing part

# # For test_llm.py
def generate_answer_with_ollama2(question):
    # return "Linear regresstion is a data science model used to predict continuous values."

    system_prompt = (
        "You are a helpful assistant that answers only questions related to data science. "
        "If the question is not related to data science, politely say you can only answer data science questions."
    )
    full_prompt = f"{system_prompt}\n\nQuestion: {question}"

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "mistral", "prompt": full_prompt, "stream": False}
        )
        result = response.json()
        return result["response"]
    except Exception as e:
        return f"Error communicating with Ollama: {e}"
    


# For test_voice.py
def get_voice_input2():
    # return "What is data science?"

    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for your question (max 5 seconds)...")
        audio = recognizer.listen(source, phrase_time_limit=5)

        try:
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            return "Sorry, I couldn't understand the audio."
        except sr.RequestError:
            return f"Could not request result; {e}"
        

# For test_language.py
def detect_language(text):
    # return "en"
    return detect(text)
