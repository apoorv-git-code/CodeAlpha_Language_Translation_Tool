import gradio as ui
from gtts import gTTS
from deep_translator import GoogleTranslator
import os

# Mapping user-friendly names to ISO 639-1 language codes
LANGUAGE_MAP = {
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Italian": "it",
    "Japanese": "ja",
    "Chinese (Simplified)": "zh-CN",
    "Arabic": "ar",
    "Portuguese": "pt",
    "Russian": "ru",
    "Hindi": "hi",
    "Korean": "ko",
}

# gTTS uses slightly different codes for a couple of languages
GTTS_CODE_MAP = {
    "zh-CN": "zh",  # gTTS uses 'zh' for Chinese
}

def translation_engine(text, source_lang, target_lang):
    """Translates text using deep-translator (no API key required)."""
    if not text.strip():
        return "Please enter some text to translate.", None

    src_code = LANGUAGE_MAP[source_lang]
    tgt_code = LANGUAGE_MAP[target_lang]

    if src_code == tgt_code:
        return "Source and target languages are the same!", None

    try:
        # Translate using deep-translator — free, no credentials needed
        translated_text = GoogleTranslator(source=src_code, target=tgt_code).translate(text)

        # Generate Text-to-Speech audio for the translated text
        gtts_lang = GTTS_CODE_MAP.get(tgt_code, tgt_code)
        tts = gTTS(text=translated_text, lang=gtts_lang)
        audio_path = "translation_speech.mp3"
        tts.save(audio_path)

        return translated_text, audio_path

    except Exception as e:
        return f"Translation error: {str(e)}", None


# --- Gradio UI ---
with ui.Blocks(title="🌐 Language Translator") as demo:
    ui.Markdown("# 🌐 Real-Time Language Translator")
    ui.Markdown(
        "Enter your text, choose your languages, and get instant translations with audio playback. "
    )

    with ui.Row():
        with ui.Column():
            input_text = ui.Textbox(
                label="Source Text",
                placeholder="Type what you want to translate here...",
                lines=5,
            )
            source_dropdown = ui.Dropdown(
                choices=list(LANGUAGE_MAP.keys()),
                value="English",
                label="Source Language",
            )
            target_dropdown = ui.Dropdown(
                choices=list(LANGUAGE_MAP.keys()),
                value="Spanish",
                label="Target Language",
            )
            submit_btn = ui.Button("Translate Text", variant="primary")

        with ui.Column():
            output_text = ui.Textbox(
                label="Translated Text", lines=5, interactive=False
            )
            output_audio = ui.Audio(
                label="Audio Pronunciation", type="filepath"
            )

    submit_btn.click(
        fn=translation_engine,
        inputs=[input_text, source_dropdown, target_dropdown],
        outputs=[output_text, output_audio],
    )

if __name__ == "__main__":
    demo.launch(share=True, theme=ui.themes.Soft())
