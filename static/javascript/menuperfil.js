// Função para mostrar o menu
function mostrarMenu() {
    const menu = document.querySelector(".menu-opcoes");
    menu.style.display = "block";
}

// Função para ocultar o menu
function ocultarMenu() {
    const menu = document.querySelector(".menu-opcoes");
    menu.style.display = "none";
}

// Alterna o menu ao clicar na imagem
document.addEventListener("DOMContentLoaded", function () {
    const botaoPerfil = document.querySelector(".menu-titulo");
    const menu = document.querySelector(".menu-opcoes");

    if (botaoPerfil && menu) {
        botaoPerfil.addEventListener("click", function (e) {
            e.stopPropagation();
            if (menu.style.display === "block") {
                ocultarMenu();
            } else {
                mostrarMenu();
            }
        });

        // Fecha o menu ao clicar fora
        document.addEventListener("click", function () {
            ocultarMenu();
        });

        // Impede o fechamento ao clicar dentro do menu
        menu.addEventListener("click", function (e) {
            e.stopPropagation();
        });
    }
});
