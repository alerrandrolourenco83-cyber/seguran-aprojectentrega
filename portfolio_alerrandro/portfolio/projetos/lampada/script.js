var lampada = document.getElementById("lamp");
var acesa = false;

lampada.addEventListener("click", lig_des);

function lig_des() {
    acesa = !acesa;
    if (acesa) {
        lampada.src = "assets/lamp_on.png";
        lampada.alt = "Lâmpada acesa";
        document.body.style.background = "radial-gradient(circle, white 8%, yellow 100%)";
    } else {
        lampada.src = "assets/lamp_off.png";
        lampada.alt = "Lâmpada apagada";
        document.body.style.background = "radial-gradient(circle, white 8%, black 100%)";
    }
}
