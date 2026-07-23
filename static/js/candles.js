//COORDINADOR. "Sabe todo"
//Detectar clics en los botones de las velas.
//Saber qué vela se seleccionó.
//Abrir el modal correspondiente.
//Más adelante hacer el fetch para eliminar.
//Actualizar la interfaz.

import { showModal, hideModal} from "./modal.js";
import { deleteCandle, toggleCandleVisibility } from "./api.js";


//Busca en el HTML el boton 'data-delete-button' y lo guarda
//Recorremos cada boton y escuchamos el click
export function initializeCandles() {

    // Estado compartido: qué vela está seleccionada para eliminar
    let selectedCandleId = null;

    const deleteButtons = document.querySelectorAll("[data-delete-button]");

    deleteButtons.forEach((button) => {
        button.addEventListener("click", () => {
            selectedCandleId = button.dataset.candleId;
            showModal("deleteModal");
        });
    });

    const confirmDeleteButton = document.querySelector("[data-confirm-delete]");

    confirmDeleteButton.addEventListener("click", async () => {
        if (!selectedCandleId) return;

        try {
            await deleteCandle(selectedCandleId);
            
            hideModal("deleteModal");
            window.location.reload();
        } catch (error) {
            console.error("Error al eliminar la vela:", error);
        }   
    });

    // ---- Ocultar / mostrar vela ----
    const toggleButtons = document.querySelectorAll("[data-toggle-visibility]");

    toggleButtons.forEach((button) => {
        button.addEventListener("click", async () => {
            const candleId = button.dataset.candleId;
            const currentlyHidden = button.dataset.isHidden === "true";
            const newIsHidden = !currentlyHidden;

            try {
                const updatedCandle = await toggleCandleVisibility(candleId, newIsHidden);
                updateVisibilityUI(button, updatedCandle.is_hidden);
            } catch (error) {
                console.error("Error al cambiar la visibilidad:", error);
            }
        });
    });
}

function updateVisibilityUI(button, isHidden) {
    button.dataset.isHidden = isHidden;

    const strikeLine = button.querySelector("[data-strike-line]");
    const row = button.closest("tr");
    const badge = row.querySelector("[data-visibility-badge]");

    if (isHidden) {
        button.classList.remove("border-gray-200", "bg-white", "text-gray-500", "hover:bg-gray-100", "hover:text-gray-900");
        button.classList.add("border-red-200", "bg-red-50", "text-red-600", "hover:bg-red-100");

        strikeLine.classList.remove("hidden");
        strikeLine.classList.add("flex");

        badge.textContent = "Não visível";
        badge.classList.remove("bg-green-100", "text-green-700");
        badge.classList.add("bg-red-100", "text-red-700");
    } else {
        button.classList.remove("border-red-200", "bg-red-50", "text-red-600", "hover:bg-red-100");
        button.classList.add("border-gray-200", "bg-white", "text-gray-500", "hover:bg-gray-100", "hover:text-gray-900");

        strikeLine.classList.remove("flex");
        strikeLine.classList.add("hidden");

        badge.textContent = "Visível";
        badge.classList.remove("bg-red-100", "text-red-700");
        badge.classList.add("bg-green-100", "text-green-700");
    }
}
