# servidor.py (Versão Final com Health Check)

import re
from collections import Counter
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# --- Modelo de Dados para a API ---
class ToolRequest(BaseModel):
    arguments: dict

# --- Aplicação FastAPI ---
app = FastAPI()

# Configuração do CORS para permitir que o seu frontend se conecte
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Nossas Ferramentas ---
def contar_frequencia_palavras(texto: str) -> str:
    # (O código da sua ferramenta aqui)
    palavras = re.findall(r'\b\w+\b', texto.lower())
    if not palavras:
        return "Nenhuma palavra encontrada no texto."
    contagem = Counter(palavras)
    resultado_str = ", ".join([f"{palavra}: {freq}" for palavra, freq in contagem.most_common()])
    return f"Frequência de palavras: {resultado_str}"

def add(a: int, b: int) -> int:
    return a + b

ferramentas_disponiveis = {
    "contar_frequencia": contar_frequencia_palavras,
    "somar": add,
}

# --- Endpoints da API ---

# AQUI ESTÁ A ADIÇÃO IMPORTANTE:
@app.get("/")
def health_check():
    """Endpoint de saúde para o Easypanel saber que o serviço está no ar."""
    return {"status": "ok", "message": "Servidor está saudável!"}

@app.post("/tool/{tool_name}")
def execute_tool(tool_name: str, request: ToolRequest):
    """Endpoint principal que executa as ferramentas."""
    if tool_name not in ferramentas_disponiveis:
        raise HTTPException(status_code=404, detail="Ferramenta não encontrada")
    
    try:
        ferramenta = ferramentas_disponiveis[tool_name]
        resultado = ferramenta(**request.arguments)
        return {"result": resultado}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao executar a ferramenta: {e}")
