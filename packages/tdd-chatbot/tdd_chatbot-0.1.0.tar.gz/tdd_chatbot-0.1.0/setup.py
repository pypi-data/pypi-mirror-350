from setuptools import setup, find_packages

setup(
    name="tdd_chatbot",
    version="0.1.0",
    author="Kavisha Nilmani",
    author_email="kavishanilmani@outlook.com",
    description="Voice-based chatbot using Ollama LLM with TDD",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "streamlit",
        "speechrecognition",
        "pyttsx3",
        "requests",
        "langdetect"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires="==3.11.0",
)
