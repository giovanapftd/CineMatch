// Rola suavemente até o catálogo quando a pessoa clica em Explorar.
const botaoExplorar = document.querySelector(".botao-banner");
const catalogo = document.querySelector("#catalogo");

if (botaoExplorar && catalogo) {
    botaoExplorar.addEventListener("click", function (evento) {
        evento.preventDefault();

        if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
            catalogo.scrollIntoView();
            return;
        }

        const inicio = window.scrollY;
        const destino = catalogo.getBoundingClientRect().top + inicio;
        const distancia = destino - inicio;
        const duracao = 1400;
        let tempoInicial = null;

        function animarRolagem(tempoAtual) {
            if (tempoInicial === null) tempoInicial = tempoAtual;

            const progresso = Math.min((tempoAtual - tempoInicial) / duracao, 1);
            const suavizacao = progresso < 0.5
                ? 4 * progresso * progresso * progresso
                : 1 - Math.pow(-2 * progresso + 2, 3) / 2;

            window.scrollTo(0, inicio + distancia * suavizacao);

            if (progresso < 1) {
                window.requestAnimationFrame(animarRolagem);
            }
        }

        window.requestAnimationFrame(animarRolagem);
    });
}
