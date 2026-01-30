// Função para exibir Toasts (Notificações Flutuantes)
// Tipo pode ser: 'success' (Verde), 'danger' (Vermelho), 'warning' (Amarelo), 'info' (Azul)
function exibirToast(mensagem, tipo = 'success') {
    const toastContainer = document.getElementById('toast-container');
    
    // Define cores e ícones baseados no tipo
    let bgClass = 'text-bg-success';
    let icon = 'bi-check-circle-fill';

    if (tipo === 'danger') {
        bgClass = 'text-bg-danger';
        icon = 'bi-exclamation-triangle-fill';
    } else if (tipo === 'warning') {
        bgClass = 'text-bg-warning';
        icon = 'bi-exclamation-circle-fill';
    } else if (tipo === 'info') {
        bgClass = 'text-bg-primary';
        icon = 'bi-info-circle-fill';
    }

    // Cria o HTML do Toast
    const toastHtml = `
        <div class="toast align-items-center ${bgClass} border-0" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="d-flex">
                <div class="toast-body fs-6">
                    <i class="bi ${icon} me-2"></i> ${mensagem}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
        </div>
    `;

    // Converte a string em elemento DOM
    const template = document.createElement('div');
    template.innerHTML = toastHtml.trim();
    const toastElement = template.firstChild;

    // Adiciona ao container
    toastContainer.appendChild(toastElement);

    // Inicializa e mostra usando o Bootstrap
    const toast = new bootstrap.Toast(toastElement, { delay: 5000 }); // some em 5 segundos
    toast.show();

    // Remove do HTML quando terminar de esconder para não acumular lixo
    toastElement.addEventListener('hidden.bs.toast', () => {
        toastElement.remove();
    });
}