var tela = document.getElementById('display');
tela.textContent = '0';
var recomecar = false; // true após resultado/erro: próximo dígito começa do zero

function clean() {
    tela.textContent = '0';
    recomecar = false;
}

function insert(valor) {
    var ehOperador = ['+', '-', 'x', '/'].indexOf(valor) !== -1;
    if (recomecar && !ehOperador) {
        tela.textContent = '0';
    }
    recomecar = false;
    if (tela.textContent === '0' && !ehOperador && valor !== '.') {
        tela.textContent = valor;
    } else {
        tela.textContent += valor;
    }
}

function back() {
    var texto = tela.textContent.slice(0, -1);
    tela.textContent = texto === '' ? '0' : texto;
}

function calcular() {
    var expressao = tela.textContent.replace(/x/g, '*');
    // aceita só números e operadores (evita executar código arbitrário no eval)
    if (!/^[0-9+\-*/.\s]+$/.test(expressao)) {
        tela.textContent = 'Erro';
        recomecar = true;
        return;
    }
    try {
        var resultado = eval(expressao);
        if (!isFinite(resultado)) {
            tela.textContent = 'Erro';
        } else {
            tela.textContent = String(parseFloat(resultado.toFixed(10)));
        }
    } catch (error) {
        tela.textContent = 'Erro';
    }
    recomecar = true;
}
