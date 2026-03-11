import sys
import os
import numpy as np
import gradio as gr
from loguru import logger
import ollama
from fastrtc import get_stt_model, get_tts_model
from datetime import datetime, timezone, timedelta
from pathlib import Path

logger.remove(0)
logger.add(sys.stderr, level="INFO")

stt_model = get_stt_model()
tts_model = get_tts_model()

client = ollama.Client(host=os.getenv("OLLAMA_HOST", "http://localhost:11434"))

SYSTEM_PROMPT = (
    "You are a friendly English conversation partner. "
    "Keep responses brief, conversational, and natural. "
    "Never use bullet points or numbered lists."
)


def process_audio(audio, history):
    if audio is None:
        return history, None, gr.update()

    sample_rate, audio_data = audio

    # Ensure mono float32
    if audio_data.ndim > 1:
        audio_data = audio_data.mean(axis=1)
    if audio_data.dtype != np.float32:
        audio_data = audio_data.astype(np.float32) / np.iinfo(audio_data.dtype).max

    # STT
    transcript = stt_model.stt((sample_rate, audio_data))
    logger.info(f"You: {transcript}")

    if not transcript.strip():
        return history, None, gr.update()

    # Build message history for Ollama
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for msg in history:
        messages.append({"role": msg["role"], "content": msg["content"]})
    messages.append({"role": "user", "content": transcript})

    # LLM
    model = os.getenv("OLLAMA_MODEL", "mistral:7b-instruct")
    response = client.chat(
        model=model,
        messages=messages,
        options={"num_predict": 200},
    )
    response_text = response["message"]["content"]
    logger.info(f"AI: {response_text}")

    # TTS — chunks are (sample_rate, ndarray)
    audio_chunks = []
    tts_sample_rate = 24000
    for chunk_sr, chunk_data in tts_model.stream_tts_sync(response_text):
        tts_sample_rate = chunk_sr
        audio_chunks.append(chunk_data)

    output_audio = None
    if audio_chunks:
        combined = np.concatenate(audio_chunks)
        output_audio = (tts_sample_rate, combined)

    new_history = history + [
        {"role": "user", "content": transcript},
        {"role": "assistant", "content": response_text},
    ]
    # Clear audio input after processing
    return new_history, output_audio, gr.update(value=None)


with gr.Blocks(title="Fluency AI") as demo:
    gr.Markdown("# Fluency AI – English Conversation Partner")
    gr.Markdown("🎤 Record your message, then click **Send**. The AI will reply with voice.")

    chatbot = gr.Chatbot(label="Conversation", height=400, type="messages")

    audio_input = gr.Audio(
        sources=["microphone"],
        type="numpy",
        label="Your message",
    )

    with gr.Row():
        send_btn = gr.Button("Send 🎤", variant="primary", scale=3)
        clear_btn = gr.Button("Clear", scale=1)

    audio_output = gr.Audio(label="AI Response", autoplay=True)

    send_btn.click(
        fn=process_audio,
        inputs=[audio_input, chatbot],
        outputs=[chatbot, audio_output, audio_input],
    )

    # Also trigger automatically when recording stops
    audio_input.stop_recording(
        fn=process_audio,
        inputs=[audio_input, chatbot],
        outputs=[chatbot, audio_output, audio_input],
    )

    clear_btn.click(lambda: ([], None, None), outputs=[chatbot, audio_output, audio_input])


if __name__ == "__main__":
    cert_file = Path("cert.pem")
    key_file = Path("key.pem")

    if not cert_file.exists() or not key_file.exists():
        from cryptography import x509
        from cryptography.x509.oid import NameOID
        from cryptography.hazmat.primitives import hashes, serialization
        from cryptography.hazmat.primitives.asymmetric import rsa
        import ipaddress

        key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COMMON_NAME, u"fluency-ai-local"),
        ])
        cert = (
            x509.CertificateBuilder()
            .subject_name(subject)
            .issuer_name(issuer)
            .public_key(key.public_key())
            .serial_number(x509.random_serial_number())
            .not_valid_before(datetime.now(timezone.utc))
            .not_valid_after(datetime.now(timezone.utc) + timedelta(days=3650))
            .add_extension(
                x509.SubjectAlternativeName([
                    x509.DNSName(u"localhost"),
                    x509.IPAddress(ipaddress.IPv4Address("127.0.0.1")),
                    x509.IPAddress(ipaddress.IPv4Address("192.168.0.103")),
                ]),
                critical=False,
            )
            .sign(key, hashes.SHA256())
        )
        cert_file.write_bytes(cert.public_bytes(serialization.Encoding.PEM))
        key_file.write_bytes(key.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.TraditionalOpenSSL,
            serialization.NoEncryption(),
        ))
        logger.info("Generated self-signed certificate")

    logger.info("Access from local network: https://192.168.0.103:7860")
    logger.info("(Accept the browser security warning to proceed)")
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        ssl_certfile=str(cert_file),
        ssl_keyfile=str(key_file),
        ssl_verify=False,
    )
