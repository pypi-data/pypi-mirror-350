from tdd_chatbot.app import generate_answer_with_ollama2

def test_generate_answer_should_mention_data_science():
    response = generate_answer_with_ollama2("What is linear regression?")
    assert "data" in response.lower() or "model" in response.lower()