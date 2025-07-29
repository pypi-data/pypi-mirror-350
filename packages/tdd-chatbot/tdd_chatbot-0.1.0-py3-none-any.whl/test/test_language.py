from tdd_chatbot.app import detect_language

def test_detect_language_returns_en_for_english_text():
    result = detect_language("What is linear regression?")
    assert result == "en"