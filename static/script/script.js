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
const tipo = document.getElementById("tipo");

let stream;
  

  tipo.addEventListener("change", function(){
    
    if(this.value === "Visitante"){

      matricula_div.style.display = "none";

    }else{

      matricula_div.style.display = "block";

    }
  })


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
    const fotoData = canvas.toDataURL("image/png");
    fotoPreview.src = fotoData;
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