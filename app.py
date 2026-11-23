'''CASO EU ESQUECER DE ALGO, VER NO MATERIAL DO PROFESSOR'''

from pathlib import Path
import random

from flask import Flask, render_template, request, send_from_directory
from pyswip import Prolog


pasta_projeto = Path(__file__).resolve().parent
arquivo_catalogo = pasta_projeto / "catálogo-regras.pl"

app = Flask(__name__)

prolog = Prolog()
prolog.consult(str(arquivo_catalogo))





generos = {
    "acao": "Ação",
    "aventura": "Aventura",
    "animacao": "Animação",
    "comedia": "Comédia",
    "crime": "Crime",
    "documentario": "Documentário",
    "drama": "Drama",
    "ficcao_cientifica": "Ficção científica",
    "guerra": "Guerra",
    "misterio": "Mistério",
    "musical": "Musical",
    "romance": "Romance",
    "suspense": "Suspense",
    "terror": "Terror",
    "esporte": "Esporte",
    "policial": "Policial",
    "familia": "Família",
    "reality_show": "Reality show",
    "thriller_psicologico": "Thriller psicológico",
}



''' Poster dos Filmes e Séries em Destaque '''
destaque_filmes = (
    ("duro_de_matar", "https://image.tmdb.org/t/p/w500/1NnCbaFaWgHczKjH5Eii46VmpPp.jpg"),
    ("matrix", "https://image.tmdb.org/t/p/w500/f89U3ADr1oiB1s9GkdPOEpXUk5H.jpg"),
    ("toy_story", "https://image.tmdb.org/t/p/w500/uXDfjJbdP4ijW5hWSBrPrlKpxab.jpg"),
)

destaque_series = (
    ("reacher", "https://image.tmdb.org/t/p/w500/f1VCQIG2iCyOookdgOzwtUpwWC0.jpg"),
    ("the_boys", "https://image.tmdb.org/t/p/w500/2zmTngn1tYC1AvfnrFLhxeD82hz.jpg"),
    ("the_mandalorian", "https://image.tmdb.org/t/p/w500/eU1i6eHXlzMOlEq0ku1Rzq7Y4wA.jpg"),
)

poster = {
    "duro_de_matar": "https://image.tmdb.org/t/p/w500/1NnCbaFaWgHczKjH5Eii46VmpPp.jpg",
    "matrix": "https://image.tmdb.org/t/p/w500/f89U3ADr1oiB1s9GkdPOEpXUk5H.jpg",
    "toy_story": "https://image.tmdb.org/t/p/w500/uXDfjJbdP4ijW5hWSBrPrlKpxab.jpg",
}


def texto_prolog(valor):
    if isinstance(valor, bytes):
        return valor.decode("utf-8")
    return str(valor)


def carregar_filme(i, poster):
    consulta = (
        f"catalogo_filme({i}, Titulo, Genero, Duracao, Resumo)"
    )
    resultado = next(prolog.query(consulta, maxresult=1), None)

    if resultado is None:
        return None

    genero = texto_prolog(resultado["Genero"])
    return {
        "titulo": texto_prolog(resultado["Titulo"]),
        "genero": generos.get(genero, genero),
        "duracao": int(resultado["Duracao"]),
        "resumo": texto_prolog(resultado["Resumo"]),
        "poster": poster,
    }


def preparar_filme(resposta):
    i = texto_prolog(resposta["Id"])
    genero = texto_prolog(resposta["Genero"])

    return {
        "titulo": texto_prolog(resposta["Titulo"]),
        "genero": generos.get(genero, genero),
        "duracao": int(resposta["Duracao"]),
        "resumo": texto_prolog(resposta["Resumo"]),
        "poster": poster.get(i),
    }


def buscar_filmes(genero=None, limite=20):
    '''Consulta os Fatos (SEPARADOS COM VIRGULA)'''
    consulta_base = "catalogo_filme(Id, Titulo, Genero, Duracao, Resumo)"
    
    if genero:
        ''' LISTA FECHADA (Gêneros) '''
        consulta = f"{consulta_base}, Genero = {genero}"
        respostas = prolog.query(consulta, maxresult=limite)
        return [preparar_filme(resposta) for resposta in respostas]

    filmes = []
    generos_disponiveis = list(generos)
    random.shuffle(generos_disponiveis)

    for genero_codigo in generos_disponiveis:
        consulta = f"{consulta_base}, Genero = {genero_codigo}"
        resposta = next(prolog.query(consulta, maxresult=1), None)
        if resposta is not None:
            filmes.append(preparar_filme(resposta))
        if len(filmes) == 10:
            break
    return filmes


def carregar_serie(i, poster):
    consulta = (
        f"catalogo_serie({i}, Titulo, Genero, Episodios, Resumo)"
    )
    resultado = next(prolog.query(consulta, maxresult=1), None)

    if resultado is None:
        return None

    genero = texto_prolog(resultado["Genero"])
    return {
        "titulo": texto_prolog(resultado["Titulo"]),
        "genero": generos.get(genero, genero),
        "episodios": int(resultado["Episodios"]),
        "resumo": texto_prolog(resultado["Resumo"]),
        "poster": poster,
    }





''' Carregar os Filmes e Séries '''
@app.get("/")
@app.get("/inicio.html")
def inicio():
    filmes = [
        carregar_filme(i, poster)
        for i, poster in destaque_filmes
    ]
    series = [
        carregar_serie(i, poster)
        for i, poster in destaque_series
    ]

    return render_template(
        "inicio.html",
        filmes_destaque=[filme for filme in filmes if filme is not None],
        series_destaque=[serie for serie in series if serie is not None],
    )


@app.get("/filmes.html")
def filmes():
    genero = request.args.get("genero", "").strip().lower()
    if genero not in generos:
        genero = ""

    return render_template(
        "filmes.html",
        filmes=buscar_filmes(genero=genero or None),
        generos=generos,
        genero_selecionado=genero,
        nome_genero=generos.get(genero, ""),
    )





'''LOCALIZA AS PASTAS DO PROJETO'''
@app.get("/series.html")
def series():
    return render_template("series.html")


@app.get("/documentarios.html")
def documentarios():
    return render_template("documentarios.html")


@app.get("/style/<path:nome_arquivo>")
def estilos(nome_arquivo):
    return send_from_directory(pasta_projeto / "style", nome_arquivo)


@app.get("/js/<path:nome_arquivo>")
def arquivos_javascript(nome_arquivo):
    return send_from_directory(pasta_projeto / "js", nome_arquivo)


@app.get("/img/<path:nome_arquivo>")
def imagens_locais(nome_arquivo):
    return send_from_directory(pasta_projeto / "img", nome_arquivo)





if __name__ == "__main__":
    app.run(debug=True)
