# API de frases populares

API REST de solo lectura para consultar frases conocidas y sus autores. Cada frase incluye un identificador, el texto, una lista de autores y una fuente o nota de atribución cuando está disponible.

## Requisitos

- Python 3.10 o posterior

## Ejecutar localmente

```bash
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

La API queda disponible en `http://127.0.0.1:8000`. La documentación interactiva de OpenAPI está en `/docs` y el esquema en `/openapi.json`.

## Endpoints

| Método | Ruta | Descripción |
| --- | --- | --- |
| GET | `/api/v1/frases` | Lista frases. Admite `q`, `autor`, `limite` (1–100) y `desde` (offset). |
| GET | `/api/v1/frases/aleatoria` | Devuelve una frase aleatoria. |
| GET | `/api/v1/frases/{id}` | Devuelve una frase por ID; responde 404 si no existe. |

Ejemplos:

```text
GET /api/v1/frases?autor=Machado
GET /api/v1/frases?q=camino&limite=5
GET /api/v1/frases/3
GET /api/v1/frases/aleatoria
```

Los datos incluidos son un catálogo inicial mantenido en memoria; reiniciar el servidor no altera el catálogo. Algunas frases populares circulan con atribuciones discutidas; el campo `fuente` indica la obra, referencia o nota de atribución disponible.
