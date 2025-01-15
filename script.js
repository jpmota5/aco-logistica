document.getElementById("rotaForm").addEventListener("submit", async function (e) {
    e.preventDefault();

    const origem = document.getElementById("origem").value;
    const destino = document.getElementById("destino").value;

    try {
        const response = await fetch("http://127.0.0.1:5000/rotas", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ origem, destino }),
        });

        const data = await response.json();

        const rotaContainer = document.getElementById("rotaContainer");
        rotaContainer.innerHTML = ""; // Limpar resultados anteriores

        if (data.rotas && data.rotas.length > 0) {
            data.rotas.forEach((rota, index) => {
                const rotaElement = document.createElement("div");
                rotaElement.className = "rota";
                rotaElement.innerHTML = `
                    <h3>Rota ${index + 1}</h3>
                    <p><strong>Caminho:</strong> ${rota.caminho.join(" → ")}</p>
                    <p><strong>Distância:</strong> ${rota.distancia} km</p>
                    <p><strong>Custo:</strong> R$${rota.custo}</p>
                    <p><strong>Tempo:</strong> ${rota.tempo} horas</p>
                `;
                rotaContainer.appendChild(rotaElement);
            });
        } else {
            rotaContainer.innerHTML = "<p>Nenhuma rota encontrada.</p>";
        }
    } catch (error) {
        console.error("Erro ao buscar rotas:", error);
        alert("Erro ao buscar rotas. Tente novamente mais tarde.");
    }
});
