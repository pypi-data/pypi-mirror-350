# 🎙️ Ollama Voice Q&A Bot

> 🎯 **A voice-activated chatbot that answers only data science-related questions using Ollama (Mistral LLM).**
>
> Powered by **Streamlit**, **Speech Recognition**, and **Test-Driven Development (TDD)**.

---

## ✨ Features

✅ Ask your question with your voice  
✅ Responses only for **data science-related** queries  
✅ Built-in **Text-to-Speech** replies  
✅ Detects non-English and politely declines  
✅ Locally hosted LLM via **Ollama + Mistral**  
✅ Unit tested with **TDD** practices

---

## 🛠️ Tech Stack

| Category           | Tools / Libraries Used                            |
|-------------------|---------------------------------------------------|
| UI                | Streamlit                                         |
| Speech-to-Text    | `speech_recognition`                              |
| Text-to-Speech    | `pyttsx3`                                         |
| LLM               | [Ollama](https://ollama.com) with `mistral` model |
| Language Detection| `langdetect`                                      |
| Testing           | Pytest + Mocking                                  |

---

## 🧪 Test-Driven Development (TDD)

This project follows TDD principles:
- Write failing tests first
- Build functionality to pass them
- Refactor and improve

📁 Tests included:
- `test_llm.py`: Ensures LLM answers are relevant
- `test_voice.py`: Mocks voice input and checks result
- `test_language.py`: Validates correct language detection

---
