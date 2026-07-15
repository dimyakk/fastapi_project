//CONOCE MODALES

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