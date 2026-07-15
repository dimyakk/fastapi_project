//COORDINADOR. "Sabe todo"
console.log("candles.js cargado");
import { showModal } from "./modal.js";

//Busca en el HTML el boton 'data-delete-button' y lo guarda
const deleteButton = document.querySelectorAll("[data-delete-button]");

//Recorremos cada boton y escuchamos el click
deleteButton.forEach((button) => {
    button.addEventListener("click", () => {
        const candleId = button.dataset.candleId;
        console.log(candleId);
        showModal("deleteModal");
    });
});

