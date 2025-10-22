const openBtn = document.getElementById("openCameraBtn");
const modal = document.getElementById("cameraModal");
const video = document.getElementById("camera");
const canvas = document.getElementById("canvas");
const captureBtn = document.getElementById("captureBtn");
const closeBtn = document.getElementById("closeCameraBtn");
const fotoPreview = document.getElementById("fotoPreview");
const Btn_apagar = document.getElementById("btn_apagar");
const form_veiculo = document.getElementById("form_veiculo");
const matricula_div = document.getElementById("matricula");
const curso_div = document.getElementById("curso");
const tipo = document.getElementById("tipo");
const btnCadastrar = document.getElementById('btnCadastrar')

let stream = null;
let photoDataUrl = null;
  

  tipo.addEventListener("change", function(){
    
    if(this.value === "Visitante"){

      matricula_div.style.display = "none";
      curso_div.style.display = "none";

    } else if (this.value === "Aluno") {

      matricula_div.style.display = "block";
      curso_div.style.display = "block";

    } else if (this.value === "Servidor") {

      matricula_div.style.display = "block";
      curso_div.style.display = "none";

    }
  });


  function verificar() {
  var selecionado = document.querySelector('input[id="radio_sim"]:checked');

  if (selecionado) {

    form_veiculo.style.display = "block";

  } else {

    form_veiculo.style.display = "none";

  }
}
    

// 👉 Abrir câmera
openBtn.addEventListener("click", async () => {
  modal.style.display = "flex";

  try {
    stream = await navigator.mediaDevices.getUserMedia({ video: true });
    video.srcObject = stream;
  } catch (err) {
    alert("Erro ao acessar a câmera: " + err.message);
  }
});

// 👉 Tirar foto
captureBtn.addEventListener("click", () => {
  const context = canvas.getContext("2d");
  

  // Ajusta canvas ao tamanho do vídeo
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;

  // Copia frame do vídeo para o canvas
  context.drawImage(video, 0, 0, canvas.width, canvas.height);

  // Se quiser, converte em imagem base64
    photoDataUrl = canvas.toDataURL("image/png", 0.8);
    fotoPreview.src = photoDataUrl;
    fotoPreview.style.display = "block";

    closeBtn.click();
    Btn_apagar.style.display = "block"


});

// 👉 Fechar câmera
closeBtn.addEventListener("click", () => {
  modal.style.display = "none";

  // Parar a câmera
  if (stream) {
    stream.getTracks().forEach(track => track.stop());
  }
});

btnCadastrar.addEventListener('click', async function() {
  try {
        // Coletar todos os dados do formulário
        const form = document.getElementById('cadastroForm');
        const formData = new FormData();
        
        // Adicionar todos os campos do formulário
        const formElements = form.elements;
        for (let element of formElements) {
            if (element.name && element.value) {
                // Para radio buttons, pegar o valor selecionado
                if (element.type === 'radio') {
                    if (element.checked) {
                        formData.append(element.name, element.value);
                    }
                } else {
                    formData.append(element.name, element.value);
                }
            }
        }
        
        // Adicionar a foto se existir
        if (photoDataUrl) {
            const response = await fetch(photoDataUrl);
            const blob = await response.blob();
            formData.append('foto', blob, 'foto_visitante.png');
        } else {
            alert('Por favor, tire uma foto do visitante!');
            return;
        }
        
        // Mostrar loading
        const btnOriginal = this.innerHTML;
        this.innerHTML = 'Cadastrando...';
        this.disabled = true;
        
        console.log('Enviando formulário...');
        
        // Enviar para o servidor
        const response = await fetch('/cadastro/pessoa', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        console.log('Resposta do servidor:', result);
        
        if (response.ok) {
            alert('✅ Visitante cadastrado com sucesso!');
            // Limpar formulário
            form.reset();
            photoDataUrl = null;
            fotoPreview.style.display = 'none';
            btnApagar.style.display = 'none';
        } else {
            alert('❌ Erro: ' + result.erro);
        }
        
    } catch (error) {
        console.error('Erro:', error);
        alert('❌ Erro de conexão: ' + error.message);
    } finally {
        // Restaurar botão
        this.innerHTML = btnOriginal;
        this.disabled = false;
    }
});