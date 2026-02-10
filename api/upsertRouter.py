from fastapi import APIRouter, File, UploadFile, Form
from services.miscellaneousService import extract_text_from_pdf, extract_text_from_txt
from api.miscellaneousRouter import split_in_chunks_embeddings, split_in_chunks_simple
from services.upsertService import upsertService, upsertService_metadata, upsertService_registro_metadata
import json

import uuid
import asyncio
from typing import List
from services.embeddingsService import embeddingsService

router = APIRouter()

### ARQUIVOS PDF
################

@router.post('/api/upsert/pdf', summary="SERVIÇO: Inserindo (upsert) um documento PDF no Banco de Dados (upsert a document PDF into the database).")
async def upsert(filepdf: UploadFile = File(...)):

    textfromPDF = extract_text_from_pdf(filepdf)
    chunkslistEmbeddings = await split_in_chunks_embeddings(text=textfromPDF)
    response = upsertService(embeddings=chunkslistEmbeddings)
    
    return response

@router.post('/api/upsert/pdf_metadata', summary="SERVIÇO: Inserindo (upsert) um documento no Banco de Dados com Metadados (upsert a document into the database with metadata).")
async def upsert_metadata(filepdf: UploadFile = File(...), metadata: str = Form(...)):      # Form(...) = Formulário

    try:
        metadataJson = json.loads(metadata)
        textfromPDF = extract_text_from_pdf(filepdf)
        chunkslistText = await split_in_chunks_simple(text=textfromPDF)
        response = upsertService_metadata(metadata=metadataJson, chunkslistText=chunkslistText)
        
        #return response
        return {"message": f"Successfully upserted {response} documents"}

    except Exception as e:

        return {"error": str(e)}

### ARQUIVOS TXT
################

@router.post('/api/upsert/txt', summary="SERVIÇO: Inserindo (upsert) um documento TXT no Banco de Dados (upsert a document TXT into the database).")
async def upsert(filetxt: UploadFile = File(...)):

    textfromTXT = extract_text_from_txt(filetxt)
    chunkslistEmbeddings = await split_in_chunks_embeddings(text=textfromTXT)
    response = upsertService(embeddings=chunkslistEmbeddings)
    
    return response

# FUNÇÃO PARA INSERIR UM DOCUMENTO TXT + METADADOS - é feito o upload do arquivo, depois esse arquivo é quebrado em pedaços (chunks); depois, cada chunk é vetorizado (embedding) e inserido no banco (upsert).
@router.post('/api/upsert/txt_metadata', summary="SERVIÇO: Inserindo (upsert) um documento TXT no Banco de Dados com Metadados (upsert a document TXT into the database with metadata).")
async def upsert_metadata(filetxt: UploadFile = File(...), metadata: str = Form(...)):      # Form(...) = Formulário

    try:
        metadataJson = json.loads(metadata)
        textfromTXT = extract_text_from_txt(filetxt)
        chunkslistText = await split_in_chunks_simple(text=textfromTXT)
        response = upsertService_metadata(metadata=metadataJson, chunkslistText=chunkslistText)
        
        #return response
        return {"message": f"Successfully upserted {response} documents"}

    except Exception as e:

        return {"error": str(e)}

# FUNÇÃO PARA INSERIR UM REGISTRO DE CHAMADO (arquivo TXT) - upload do arquivo, que será um chunk; depois esse chunck é vetorizado (embedding) e inserido no banco (upsert).
@router.post('/api/upsert/txt_registro_metadata', summary="SERVIÇO: Inserindo (upsert) um registro de chamado de arquivo TXT no Banco de Dados com Metadados (upsert a register from TXT into the database with metadata).")
async def upsert_registro_metadata(filetxt: UploadFile = File(...), metadata: str = Form(...)):

    try:
        metadataJson = json.loads(metadata)
        textfromTXT = extract_text_from_txt(filetxt)
        response = upsertService_registro_metadata(metadata=metadataJson, chunk=textfromTXT)
        
        return {"message": f"Successfully upserted {response} documents"}

    except Exception as e:

        return {"error": str(e)}

# FUNÇÃO PARA INSERIR VÁRIOS REGISTROS DE CHAMADO (vários arquivos TXT)
@router.post('/api/upsert/multiple_txt_files', summary="SERVIÇO: Inserir múltiplos arquivos TXT no Banco de Dados Vetorial com Metadados")
async def upsert_multiple_files(files: List[UploadFile] = File(...), metadata: str = Form(...)):
    """
    Insere múltiplos arquivos TXT no banco de dados vetorial Pinecone.
    
    Args:
        files: Lista de arquivos TXT para processar
        metadata_list: JSON string contendo lista de objetos de metadados
                      (um para cada arquivo, na mesma ordem)
    
    Returns:
        Resultado do upsert para cada arquivo
    """
    try:
        metadataJson = json.loads(metadata)
        
        results = []
        
        # Processar cada arquivo sequencialmente
        for i, filetxt in enumerate(files):
            try:
                # Extrair texto do arquivo
                textfromTXT = await extract_text_from_txt_async(filetxt)
                
                # Inserir no banco de dados
                result = upsertService_registro_metadata(metadata=metadataJson, chunk=textfromTXT)
                
                results.append({
                    "filename": filetxt.filename,
                    "status": "success",
                    "upserted_count": result if isinstance(result, int) else 0,
                    "message": f"Arquivo {i+1}/{len(files)} processado com sucesso"
                })
                
                # Pequena pausa para não sobrecarregar a API
                await asyncio.sleep(0.1)
                
            except Exception as file_error:
                results.append({
                    "filename": filetxt.filename,
                    "status": "error",
                    "error": str(file_error),
                    "message": f"Erro ao processar arquivo {i+1}/{len(files)}"
                })
        
        return {
            "message": f"Processamento de {len(files)} arquivos concluído",
            "results": results,
            "summary": {
                "total_files": len(files),
                "successful": sum(1 for r in results if r["status"] == "success"),
                "failed": sum(1 for r in results if r["status"] == "error")
            }
        }

    except Exception as e:
        return {"error": str(e)}

# Versão assíncrona da extração de texto
async def extract_text_from_txt_async(filetxt: UploadFile):
    """
    Versão assíncrona para extrair texto de arquivo TXT
    """
    content = await filetxt.read()
    return content.decode('utf-8')