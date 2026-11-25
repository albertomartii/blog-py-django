/* Envía el "me gusta" por POST y actualiza el contador sin recargar la página. */
document.addEventListener("DOMContentLoaded", function () {
    const botonLike = document.getElementById("boton-like");
    if (!botonLike) {
        return;
    }

    botonLike.addEventListener("click", async function (evento) {
        evento.preventDefault();

        const respuesta = await fetch(botonLike.dataset.url, {
            method: "POST",
            headers: { "X-CSRFToken": botonLike.dataset.csrf },
        });
        if (!respuesta.ok) {
            return;
        }

        const datos = await respuesta.json();
        document.getElementById("contador-likes").textContent = datos.likes;
    });
});
