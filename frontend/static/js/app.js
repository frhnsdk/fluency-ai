const recordButton = document.getElementById('record');
const chatDiv = document.getElementById('chat');
const audioElement = document.getElementById('audio');

let mediaRecorder;
let audioChunks = [];
let sessionId = 'session_' + Date.now();

recordButton.addEventListener('click', async () => {
    if (recordButton.textContent === 'Start Recording') {
        startRecording();
    } else {
        stopRecording();
    }
});

async function startRecording() {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);
    audioChunks = [];

    mediaRecorder.ondataavailable = event => {
        audioChunks.push(event.data);
    };

    mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
        await sendAudio(audioBlob);
    };

    mediaRecorder.start();
    recordButton.textContent = 'Stop Recording';
}

function stopRecording() {
    mediaRecorder.stop();
    recordButton.textContent = 'Start Recording';
}

async function sendAudio(blob) {
    const formData = new FormData();
    formData.append('file', blob, 'audio.webm');

    addMessage('System', 'Transcribing...');

    const response = await fetch('/stt', {
        method: 'POST',
        body: formData
    });

    const data = await response.json();
    const text = data.text;
    removeLastSystemMessage();
    addMessage('User', text);

    if (text.toLowerCase().includes('thank you bye')) {
        addMessage('AI', 'Goodbye! It was great practising with you.');
        return;
    }

    await sendText(text);
}

async function sendText(text) {
    addMessage('System', 'Thinking...');

    const response = await fetch('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text, session_id: sessionId })
    });

    removeLastSystemMessage();
    const replyText = response.headers.get('X-Reply-Text');
    addMessage('AI', replyText);

    const audioBlob = await response.blob();
    const audioUrl = URL.createObjectURL(audioBlob);
    audioElement.src = audioUrl;
    audioElement.style.display = 'block';
    audioElement.play();
}

function addMessage(sender, text) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender.toLowerCase()}`;
    const escaped = document.createElement('span');
    escaped.textContent = text;
    messageDiv.innerHTML = `<strong>${sender}:</strong> `;
    messageDiv.appendChild(escaped);
    chatDiv.appendChild(messageDiv);
    chatDiv.scrollTop = chatDiv.scrollHeight;
}

function removeLastSystemMessage() {
    const msgs = chatDiv.querySelectorAll('.message.system');
    if (msgs.length) msgs[msgs.length - 1].remove();
}