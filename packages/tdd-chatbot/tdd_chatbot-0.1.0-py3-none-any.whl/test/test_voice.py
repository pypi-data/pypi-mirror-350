from unittest.mock import patch, MagicMock
from tdd_chatbot.app import get_voice_input2

@patch("speech_recognition.Recognizer.listen")
@patch("speech_recognition.Microphone")
def test_get_voice_input_returns_expected_string(mock_microphone, mock_listen):
    # Create a mock audio data object
    mock_audio_data = MagicMock()
    mock_listen.return_value = mock_audio_data

    # Also patch the recognizer's recognize_google method
    with patch("speech_recognition.Recognizer.recognize_google", return_value="What is data science?"):
        result = get_voice_input2()
        assert result == "What is data science?"