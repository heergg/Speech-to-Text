import streamlit as st
import azure.cognitiveservices.speech as speechsdk
import os
from dotenv import load_dotenv

# Load .env
load_dotenv()
SPEECH_KEY = os.getenv("AZURE_SPEECH_KEY")
SPEECH_REGION = os.getenv("AZURE_SPEECH_REGION")

# Streamlit UI
st.title("🎤 Azure Speech Service - STT & TTS (Mic Input)")
st.write("Speak into your microphone or convert text to speech!")

mode = st.radio("Choose Mode:", ("Speech-to-Text (Mic)", "Text-to-Speech"))

# Azure Speech Config
speech_config = speechsdk.SpeechConfig(subscription=SPEECH_KEY, region=SPEECH_REGION)

if mode == "Speech-to-Text (Mic)":
    st.write("Click 'Start Recording' and speak into your microphone.")
    
    if st.button("Start Recording"):
        audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
        recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
        
        st.info("Listening...")
        result = recognizer.recognize_once()
        
        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            st.success("You said:")
            st.write(result.text)
        elif result.reason == speechsdk.ResultReason.NoMatch:
            st.error("Speech could not be recognized.")
        else:
            st.error(f"Error: {result.reason}")

elif mode == "Text-to-Speech":
    text_input = st.text_area("Enter text to convert to speech:")
    voice = st.selectbox(
        "Choose voice:",
        ["en-US-JennyNeural", "en-US-GuyNeural", "en-GB-LibbyNeural", "en-GB-RyanNeural"]
    )
    
    if st.button("Convert to Speech"):
        if text_input.strip() == "":
            st.warning("Please enter some text.")
        else:
            audio_config = speechsdk.audio.AudioOutputConfig(filename="output.wav")
            synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
            synthesizer.speak_text(text_input)
            
            # Streamlit audio player
            audio_file = open("output.wav", "rb")
            audio_bytes = audio_file.read()
            st.audio(audio_bytes, format="audio/wav")
            st.success("Speech generated successfully!")

