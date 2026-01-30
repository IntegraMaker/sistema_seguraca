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
const btnCadastrar = document.getElementById('btnCadastrar');

let stream = null;
let photoDataUrl = null;

// Função auxiliar segura para exibir Toast ou Alert (caso o Toast falhe)
function notificar(mensagem, tipo) {
    if (typeof exibirToast === "function") {
        exibirToast(mensagem, tipo);
    } else {
        // Fallback para alert caso o script de toast não tenha carregado
        alert(mensagem);
    }
}

// Lógica de mostrar campos baseada no Cargo
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

// Lógica do Veículo
function verificar() {
  var selecionado = document.querySelector('input[id="radio_sim"]:checked');
  if (selecionado) {
    form_veiculo.style.display = "block";
  } else {
    form_veiculo.style.display = "none";
  }
}
    
// === LÓGICA DA CÂMERA (Mantida Intacta) ===
openBtn.addEventListener("click", async () => {
  modal.style.display = "flex";
  try {
    stream = await navigator.mediaDevices.getUserMedia({ video: true });
    video.srcObject = stream;
  } catch (err) {
    notificar("Erro ao acessar a câmera: " + err.message, "danger");
  }
});

captureBtn.addEventListener("click", () => {
  const context = canvas.getContext("2d");
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  context.drawImage(video, 0, 0, canvas.width, canvas.height);

  photoDataUrl = canvas.toDataURL("image/png", 0.8);
  fotoPreview.src = photoDataUrl;
  fotoPreview.style.display = "block";

  closeBtn.click();
  Btn_apagar.style.display = "block";
});

closeBtn.addEventListener("click", () => {
  modal.style.display = "none";
  if (stream) {
    stream.getTracks().forEach(track => track.stop());
  }
});

Btn_apagar.addEventListener("click", () => {
  photoDataUrl = null;
  fotoPreview.src = "";
  fotoPreview.style.display = "none";
  Btn_apagar.style.display = "none";  
});

// === LÓGICA DE CADASTRO (Atualizada com Toast) ===
btnCadastrar.addEventListener('click', async function() {
  const btnOriginal = this.innerHTML;
  
  try {
    const nome = document.getElementById("nome").value;
    const cpf = document.getElementById("floatingInput").value;

    // Validação básica
    if(!nome || !cpf) {
      notificar('Por favor, preencha todos os campos obrigatórios.', 'warning');
      return;
    }

    // Validação da foto
    if (!photoDataUrl) {
      notificar('Por favor, tire uma foto do visitante!', 'warning');
      return;
    }

    // Preparação visual do botão
    this.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Cadastrando...';
    this.disabled = true;

    const form = document.getElementById('cadastroForm');
    const formData = new FormData();
    
    // Coleta dados do formulário
    const formElements = form.elements;
    for (let element of formElements) {
      if (element.name && element.value) {
        if (element.type === 'radio') {
          if (element.checked) {
            formData.append(element.name, element.value);
          }
        } else {
          formData.append(element.name, element.value);
        }
      }
    }
    
    // Processa a foto
    const responseFoto = await fetch(photoDataUrl);
    const blob = await responseFoto.blob();
    formData.append('foto', blob, 'foto_visitante.png');
    
    console.log('Enviando formulário...');
    
    // Envio para o Backend
    const response = await fetch('/cadastro/pessoa', {
      method: 'POST',
      body: formData
    });
    
    const result = await response.json();
    console.log('Resposta do servidor:', result);
    
    if (response.ok) {
      // SUCESSO
      notificar('Visitante cadastrado com sucesso!', 'success');
      
      // Limpar formulário e resets visuais
      form.reset();
      photoDataUrl = null;
      fotoPreview.style.display = 'none';
      Btn_apagar.style.display = 'none';
      matricula_div.style.display = "none";
      curso_div.style.display = "none";
      form_veiculo.style.display = "none";
      
    } else {
      // ERRO DO BACKEND (ex: CPF duplicado)
      notificar('Erro: ' + result.erro, 'danger');
    }
        
  } catch (error) {
    console.error('Erro:', error);
    notificar('Erro de conexão: ' + error.message, 'danger');
  } finally {
    // Restaura o botão
    this.innerHTML = btnOriginal;
    this.disabled = false;
  }
});