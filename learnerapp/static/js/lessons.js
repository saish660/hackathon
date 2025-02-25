let speech = new SpeechSynthesisUtterance();

const speakBtn = document.querySelector('#speak')

speakBtn.addEventListener('click', () => {
    let text = speakBtn.dataset.content
    text = text.replace(/[\/\\#~*]/g,'')

    speech.text = text;
    let voices = window.speechSynthesis.getVoices();
    window.speechSynthesis.speak(speech);
})



