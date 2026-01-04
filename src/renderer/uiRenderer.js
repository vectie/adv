class UIRenderer {
  constructor(domController) {
    this.domController = domController;
  }

  renderTranscription(transcription) {
    const container = this.domController.transcriptionResult;
    container.innerHTML = '';

    transcription.forEach(item => {
      const itemDiv = document.createElement('div');
      itemDiv.className = 'transcription-item';
      
      const speakerClass = item.speaker === '主持人' ? 'host' : 'guest';
      
      itemDiv.innerHTML = `
        <div class="speaker ${speakerClass}">${item.speaker}</div>
        <div class="transcription-text">${item.text}</div>
      `;
      
      container.appendChild(itemDiv);
    });
  }

  showAlert(message) {
    alert(message);
  }

  showError(message) {
    this.showAlert(`处理失败: ${message}`);
  }
}

module.exports = UIRenderer;