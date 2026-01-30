// Variável de controle para impedir leituras múltiplas enquanto valida
let isProcessing = false;
function onScanSuccess(decodedText, decodedResult) {
    // Se já estiver processando um código ou mostrando a msg de 5s, ignora novos QRs
    if (isProcessing) {
        return;
    }
    console.log(`Código lido: ${decodedText}`);
    isProcessing = true; // Trava novas leituras
    // Envia para o Backend Python
    fetch('/registro/qrcode', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ conteudo: decodedText })
    })
    .then(response => response.json())
    .then(data => {
        mostrarMensagem(data.mensagem, data.sucesso);
    })
    .catch(error => {
        console.error('Erro:', error);
        mostrarMensagem("Erro de comunicação com o servidor.", false);
    });
}
function mostrarMensagem(texto, sucesso) {
    var x = document.getElementById("status-msg");
    x.innerText = texto;
    
    // Define a cor baseada na resposta do backend
    if (sucesso) {
        x.className = "show msg-sucesso";
    } else {
        x.className = "show msg-erro";
    }
    // A câmera continua ligada, mas o 'isProcessing' impede novos envios
    // O requisito diz 5 segundos de mensagem
    setTimeout(function(){ 
        x.className = x.className.replace("show", ""); // Remove a mensagem visual
        isProcessing = false; // Destrava para ler o próximo QR Code
    }, 5000);
}
function onScanFailure(error) {
    // Não fazer nada aqui para não poluir o console, 
    // pois a biblioteca gera erros constantes enquanto não acha um QR code.
}
// Configuração do Leitor
let html5QrcodeScanner = new Html5QrcodeScanner(
    "reader", 
    { 
        fps: 10, // Frames por segundo de leitura
        qrbox: {width: 250, height: 250}, // Tamanho da caixa de foco
        aspectRatio: 1.0
    },
    /* verbose= */ false
);

html5QrcodeScanner.render(onScanSuccess, onScanFailure);