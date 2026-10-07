import os
import glob
# pyrefly: ignore [missing-import]
from fastapi import FastAPI, HTTPException
# pyrefly: ignore [missing-import]
from fastapi.responses import FileResponse
# pyrefly: ignore [missing-import]
from fastapi.middleware.cors import CORSMiddleware
from data.figurinhas import figurinhas

# Inicializa a aplicação FastAPI
app = FastAPI()

# Configuração do Middleware CORS para aceitar requisições de qualquer origem
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Definição dos caminhos absolutos para encontrar a pasta de imagens 'figurinhas'
PASTA_BASE = os.path.dirname(os.path.abspath(__file__))
PASTA_IMAGENS = os.path.join(PASTA_BASE, "figurinhas")

# Endpoint para listar todas as figurinhas ativas
@app.get("/figurinhas")
def listar_figurinhas():
    return figurinhas

# Endpoint para obter a imagem de uma figurinha específica pelo ID
@app.get("/figurinhas/{id}/imagem")
def obter_imagem(id: int):
    # Usa glob para encontrar o arquivo com o prefixo do ID correspondente na pasta figurinhas/
    padrao = os.path.join(PASTA_IMAGENS, f"{id:02d}[!0-9]*")
    arquivos = glob.glob(padrao)
    
    # Retorna erro 404 caso nenhuma imagem seja encontrada para o ID fornecido
    if not arquivos:
        raise HTTPException(status_code=404, detail="Imagem não encontrada")
    
    # Retorna a imagem encontrada como FileResponse
    return FileResponse(arquivos[0])