function mostrarMenu() {
    const menu = document.querySelector(".menu-opcoes");
    menu.style.display = "block";
}

function ocultarMenu() {
    const menu = document.querySelector(".menu-opcoes");
    menu.style.display = "none";
}

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

        document.addEventListener("click", function () {
            ocultarMenu();
        });

        menu.addEventListener("click", function (e) {
            e.stopPropagation();
        });
    }
});

document.addEventListener("DOMContentLoaded", function () {
    const favIcons = document.querySelectorAll(".fav-icon");

    favIcons.forEach(icon => {
        icon.addEventListener("click", async function () {

            const url = icon.dataset.url;

            const resp = await fetch(url, {
                method: "POST"
            });

            if (resp.status === 401) {
                window.location.href = "/login";
                return;
            }

            const data = await resp.json();

            if (data.favorito === true) {
                icon.textContent = "❤️";
                icon.classList.add("favorited");
            } else {
                icon.textContent = "♡";
                icon.classList.remove("favorited");
            }
        });
    });
});




function validacaoCadastro(cadastro) {
  const form = document.getElementById(cadastro);

  form.addEventListener("submit", function (event) {
    let valido = true;

    // Pegar campos
    const nome = document.getElementById("nome");
    const sobrenome = document.getElementById("sobrenome");
    const username = document.getElementById("username");
    const email = document.getElementById("email");
    const senha = document.getElementById("password");
    
    
    // Resetar mensagens
    document.getElementById("erro_nome").style.display = "none";
    document.getElementById("erro_sobrenome").style.display = "none";
    document.getElementById("erro_username").style.display = "none";
    document.getElementById("erro_email").style.display = "none";
    document.getElementById("erro_senha").style.display = "none";
    
    
    // Validar nome
    if (nome.value.trim() === "") {
      document.getElementById("erro_nome").style.display = "inline";
      valido = false;
    }

    if (sobrenome.value.trim() === "") {
      document.getElementById("erro_sobrenome").style.display = "inline";
      valido = false;
    }

    if (username.value.trim() === "") {
      document.getElementById("erro_username").style.display = "inline";
      valido = false;
    }

    // Validar email
    if (email.value.trim() === "" || 
        !email.value.includes("@") || 
        !email.value.includes(".com")
      ) {
    document.getElementById("erro_email").style.display = "inline";
    valido = false;
    }
    
    if (senha.value.trim().length < 8) {
      document.getElementById("erro_senha").style.display = "inline";
      valido = false;
  }
  
  
  // Se não for válido, impedir envio
  if (!valido) {
      event.preventDefault();
    }
  });
}