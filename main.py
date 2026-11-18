from __future__ import annotations

import random
from typing import Annotated

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, ConfigDict


class Frase(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: int
    texto: str
    autores: list[str]
    fuente: str | None = None


FRASES: tuple[Frase, ...] = (
    Frase(id=1, texto="Pienso, luego existo.", autores=["René Descartes"], fuente="Discurso del método"),
    Frase(id=2, texto="La vida es sueño, y los sueños, sueños son.", autores=["Pedro Calderón de la Barca"], fuente="La vida es sueño"),
    Frase(id=3, texto="Caminante, no hay camino, se hace camino al andar.", autores=["Antonio Machado"], fuente="Proverbios y cantares (Campos de Castilla)"),
    Frase(id=4, texto="En un lugar de la Mancha, de cuyo nombre no quiero acordarme...", autores=["Miguel de Cervantes"], fuente="Don Quijote de la Mancha"),
    Frase(id=5, texto="La imaginación es más importante que el conocimiento.", autores=["Albert Einstein"], fuente="Entrevista publicada en The Saturday Evening Post (1929)"),
    Frase(id=6, texto="La medida del amor es amar sin medida.", autores=["San Agustín"], fuente="Atribuida a San Agustín"),
    Frase(id=7, texto="No hay nada más poderoso que una idea a la que le ha llegado su tiempo.", autores=["Víctor Hugo"], fuente="Atribuida a Víctor Hugo"),
    Frase(id=8, texto="El respeto al derecho ajeno es la paz.", autores=["Benito Juárez"], fuente="Manifiesto a la nación (1867)"),
    Frase(id=9, texto="La educación es el arma más poderosa que puedes usar para cambiar el mundo.", autores=["Nelson Mandela"], fuente="Discurso en la entrega del Premio Ambassadors for Humanity (2003)"),
    Frase(id=10, texto="Solo sé que no sé nada.", autores=["Sócrates"], fuente="Paráfrasis de la Apología de Sócrates de Platón"),
)

app = FastAPI(
    title="API de frases populares",
    description="Consulta frases populares y las personas a quienes se atribuyen.",
    version="1.0.0",
)


@app.get("/api/v1/frases", response_model=list[Frase], tags=["Frases"])
def listar_frases(
    q: Annotated[str | None, Query(description="Busca en el texto y los autores.")] = None,
    autor: Annotated[str | None, Query(description="Filtra por nombre de autor.")] = None,
    limite: Annotated[int, Query(ge=1, le=100)] = 20,
    desde: Annotated[int, Query(ge=0)] = 0,
) -> list[Frase]:
    resultados = list(FRASES)
    if q:
        termino = q.casefold()
        resultados = [
            frase for frase in resultados
            if termino in frase.texto.casefold()
            or any(termino in nombre.casefold() for nombre in frase.autores)
        ]
    if autor:
        termino_autor = autor.casefold()
        resultados = [
            frase for frase in resultados
            if any(termino_autor in nombre.casefold() for nombre in frase.autores)
        ]
    return resultados[desde : desde + limite]


@app.get("/api/v1/frases/aleatoria", response_model=Frase, tags=["Frases"])
def frase_aleatoria() -> Frase:
    return random.choice(FRASES)


@app.get("/api/v1/frases/{frase_id}", response_model=Frase, tags=["Frases"])
def obtener_frase(frase_id: int) -> Frase:
    for frase in FRASES:
        if frase.id == frase_id:
            return frase
    raise HTTPException(status_code=404, detail="No se encontró una frase con ese ID.")


@app.get("/", include_in_schema=False)
def inicio() -> dict[str, str]:
    return {"mensaje": "API de frases populares", "documentacion": "/docs"}
