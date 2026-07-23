//LLAMADAS FETCH(). SOLO HABLA CON FASTAPI

const CANDLES_URL = "/api/candles";

export async function deleteCandle(id) {
    const response = await fetch(`${CANDLES_URL}/${id}`, {
        method: "DELETE",
    });

    if (!response.ok) {
        throw new Error(`No se pudo eliminar la vela (status ${response.status})`);
    }
}

export async function toggleCandleVisibility(id, isHidden) {
    const response = await fetch(`${CANDLES_URL}/${id}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ is_hidden: isHidden }),
    });

    if (!response.ok) {
        throw new Error(`No se pudo actualizar la visibilidad (status ${response.status})`);
    }

    return response.json();
}