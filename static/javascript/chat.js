console.log("chat.js carregado");

async function carregarMensagens() {
    try {
        const resposta = await fetch("/mensagens");
        const msgs = await resposta.json();

        const div = document.getElementById("chat-container");
        div.innerHTML = "";

        msgs.forEach(m => {
            const linha = document.createElement("p");
            linha.innerHTML = `<b>${m.usuario}</b>: ${m.conteudo} <span style="font-size:12px;color:#777;">(${m.criado_em})</span>`;
            div.appendChild(linha);
        });

        div.scrollTop = div.scrollHeight;

    } catch (error) {
        console.error("Erro ao carregar mensagens:", error);
    }
}

setInterval(carregarMensagens, 1500);
carregarMensagens();

document.getElementById("formMsg").addEventListener("submit", async (e) => {
    e.preventDefault();

    const input = document.getElementById("msgInput");
    const conteudo = input.value.trim();
    if (!conteudo) return;

    const fd = new FormData();
    fd.append("conteudo", conteudo);

    const resposta = await fetch("/enviar_mensagem", {
        method: "POST",
        body: fd
    });

    if (resposta.ok) {
        input.value = "";
        carregarMensagens();
    }
});