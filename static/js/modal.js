//CONOCE MODALES
//Saber abrir un <dialog>.
//Saber cerrarlo.
//Configurar los botones que lo cierran (data-modal-close).

export function showModal(modalId) {
    const modal = document.getElementById(modalId);

    if (!modal) {
        console.error(`Modal "${modalId}" no encontrado.`);
        return;
    }

    modal.showModal();
}

export function hideModal(modalId) {
    const modal = document.getElementById(modalId);

    if (!modal) {
        console.error(`Modal "${modalId}" no encontrado.`);
        return;
    }

    modal.close();
}

//Busca botones data-close-button, los recorre y escucha. Cuando lo escucha, JS sube por el arbol del HTML y devuelve ese elemento (dialog)
//entonces el boton no necesita saber en que modal esta, simplemente cerrarlo. Hace que funcione para cualquier modal y no para uno especifico
export function initializeModals() {

    const closeButtons = document.querySelectorAll("[data-modal-close]");

    closeButtons.forEach((button) => {
        button.addEventListener("click", () => {
            const modal = button.closest("dialog");

            modal.close();
        });
    });
}