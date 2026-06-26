import re
import gradio as ui
from deep_translator import GoogleTranslator
from gtts import gTTS

LANGUAGE_MAP = {
    "English": "en", "Spanish": "es", "French": "fr", "German": "de",
    "Italian": "it", "Japanese": "ja", "Chinese (Simplified)": "zh-CN",
    "Arabic": "ar", "Portuguese": "pt", "Russian": "ru", "Hindi": "hi",
    "Korean": "ko",
}
LANGS = list(LANGUAGE_MAP.keys())
MAX_CHUNK_SIZE = 4500

def split_text_into_chunks(text, max_size=MAX_CHUNK_SIZE):
    """Splits text into chunks <= max_size, preserving sentence boundaries."""
    if len(text) <= max_size:
        return [text]

    chunks, current_chunk = [], ""
    # Splitting on common punctuation, including the Hindi danda (।)
    sentences = re.split(r'(?<=[।.?!])\s*', text)

    for sentence in sentences:
        # If a single sentence is massive, break it down by words
        if len(sentence) > max_size:
            for word in sentence.split():
                if len(current_chunk) + len(word) + 1 > max_size:
                    if current_chunk: chunks.append(current_chunk)
                    current_chunk = word
                else:
                    current_chunk = f"{current_chunk} {word}".strip()
        elif len(current_chunk) + len(sentence) + 1 > max_size:
            if current_chunk: chunks.append(current_chunk)
            current_chunk = sentence
        else:
            current_chunk = f"{current_chunk} {sentence}".strip()

    if current_chunk:
        chunks.append(current_chunk)
    return chunks

def translation_engine(text, source_lang, target_lang):
    if not text.strip():
        return "Please enter some text to translate.", None

    src, tgt = LANGUAGE_MAP[source_lang], LANGUAGE_MAP[target_lang]
    if src == tgt:
        return "Source and target languages are the same!", None

    try:
        translator = GoogleTranslator(source=src, target=tgt)
        chunks = split_text_into_chunks(text)
        
        # Fast, clean list comprehension to translate non-empty chunks
        translated_chunks = [translator.translate(c) for c in chunks if c.strip()]
        translated = " ".join(filter(None, translated_chunks))

        if not translated:
            return "Translation returned an empty result. Please try again.", None

        # Generate audio
        audio_path = "translation_speech.mp3"
        tts = gTTS(text=translated, lang="zh" if tgt == "zh-CN" else tgt)
        tts.save(audio_path)
        
        return translated, audio_path

    except Exception as e:
        return f"Translation error: {e}", None

# UI Layout
with ui.Blocks(title="🌐 Language Translator", theme=ui.themes.Soft()) as demo:
    ui.Markdown("# 📝 Real-Time Language Translator 😲")
    ui.Markdown("Enter your text, choose your languages, and get instant translations with audio playback.")

    with ui.Row():
        with ui.Column():
            input_text = ui.Textbox(label="Source Text", placeholder="Type what you want to translate here...", lines=5)
            source_dd = ui.Dropdown(choices=LANGS, value="English", label="Source Language")
            target_dd = ui.Dropdown(choices=LANGS, value="Spanish", label="Target Language")
            submit_btn = ui.Button("Translate Text", variant="primary")
            
        with ui.Column():
            output_text = ui.Textbox(label="Translated Text", lines=5, interactive=False)
            output_audio = ui.Audio(label="Audio Pronunciation", type="filepath")

    # Wire up the button logic properly
    submit_btn.click(
        fn=translation_engine,
        inputs=[input_text, source_dd, target_dd],
        outputs=[output_text, output_audio],
    )

if __name__ == "__main__":
    demo.launch(share=True)
