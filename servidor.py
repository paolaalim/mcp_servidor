# servidor.py (VERSÃO COM CORS CORRIGIDO)

import re
from collections import Counter
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# --- Modelo de Dados para a nossa API ---
class ToolRequest(BaseModel):
    arguments: dict

# --- Aplicação FastAPI ---
app = FastAPI()

# --- Configuração do CORS CORRIGIDA ---
# Trocamos o "*" por uma lista específica de origens permitidas
origins = [
    "null",  # Necessário para permitir abrir o index.html como arquivo local (file://)
    "http://127.0.0.1:5500"  # Para o caso de você usar a extensão "Live Server"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Nossas Ferramentas ---
def contar_frequencia_palavras(texto: str) -> str:
    """Conta a frequência de cada palavra em um texto fornecido."""
    palavras = re.findall(r'\b\w+\b', texto.lower())
    if not palavras:
        return "Nenhuma palavra encontrada no texto."
    contagem = Counter(palavras)
    resultado_str = ", ".join([f"{palavra}: {freq}" for palavra, freq in contagem.most_common()])
    return f"Frequência de palavras: {resultado_str}"

def add(a: int, b: int) -> int:
    """Soma dois números inteiros."""
    return a + b

ferramentas_disponiveis = {
    "contar_frequencia": contar_frequencia_palavras,
    "somar": add,
}

# --- Endpoints da API ---
@app.get("/")
def health_check():
    """Endpoint de saúde para o Easypanel saber que o serviço está no ar."""
    return {"status": "ok"}

@app.post("/tool/{tool_name}")
def execute_tool(tool_name: str, request: ToolRequest):
    """Endpoint principal que recebe o nome da ferramenta e os seus argumentos."""
    if tool_name not in ferramentas_disponiveis:
        raise HTTPException(status_code=404, detail="Ferramenta não encontrada")
    
    try:
        ferramenta = ferramentas_disponiveis[tool_name]
        resultado = ferramenta(**request.arguments)
        return {"result": resultado}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao executar a ferramenta: {e}")