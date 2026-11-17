var form = document.getElementById("form");
var campo = document.getElementById("nova");
var lista = document.getElementById("lista");
var aviso = document.getElementById("aviso");
var contador = document.getElementById("contador");

function atualizarContador() {
    var total = lista.children.length;
    var feitas = lista.querySelectorAll("li.feita").length;
    contador.textContent = total === 0 ? "Nenhuma tarefa ainda." : feitas + " de " + total + " concluída(s)";
}

function criarTarefa(texto) {
    var li = document.createElement("li");

    var check = document.createElement("input");
    check.type = "checkbox";
    check.setAttribute("aria-label", "Concluir: " + texto);
    check.addEventListener("change", function () {
        li.classList.toggle("feita", check.checked);
        atualizarContador();
    });

    var span = document.createElement("span");
    span.textContent = texto;

    var remover = document.createElement("button");
    remover.type = "button";
    remover.className = "remover";
    remover.textContent = "×";
    remover.setAttribute("aria-label", "Remover: " + texto);
    remover.addEventListener("click", function () {
        li.remove();
        atualizarContador();
    });

    li.append(check, span, remover);
    lista.appendChild(li);
}

form.addEventListener("submit", function (e) {
    e.preventDefault();
    var texto = campo.value.trim();
    if (!texto) {
        aviso.textContent = "Digite uma tarefa antes de adicionar.";
        campo.focus();
        return;
    }
    aviso.textContent = "";
    criarTarefa(texto);
    campo.value = "";
    campo.focus();
    atualizarContador();
});

atualizarContador();
