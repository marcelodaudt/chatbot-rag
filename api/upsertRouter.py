from fastapi import APIRouter, File, UploadFile, Form
from services.miscellaneousService import extract_text_from_pdf
from api.miscellaneousRouter import split_in_chunks_embeddings, split_in_chunks_simple
from services.upsertService import upsertService, upsertService_metadata
import json

router = APIRouter()

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
