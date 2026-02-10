from services.authenticationService import authentication_pinecone
from services.embeddingsService import embeddingsService
import uuid

pc = authentication_pinecone()

def upsertService(embeddings: list):

    # Obs.: RECOMENDAÇÃO: usar o HOST do Índice no Pinecone, não o NAME do Índice - recomendado pelo próprio Pinecone
    #index = pc.Index(host="https://itvalleyschool-k6qbag2.svc.aped-4627-b74a.pinecone.io")
    #index = pc.Index(host="https://base-de-conhecimentos-chamados-1-k6qbag2.svc.aped-4627-b74a.pinecone.io")
    #index = pc.Index(host="https://base-de-conhecimentos-chamados-2-k6qbag2.svc.aped-4627-b74a.pinecone.io")
    index = pc.Index(host="https://base-de-conhecimento-chamados-3-k6qbag2.svc.aped-4627-b74a.pinecone.io")

    try:

        vectors = []

        for chunk_unit in embeddings:
            vectors.append({"id": f"{uuid.uuid4()}", "values": chunk_unit})

        response = index.upsert(vectors=vectors, namespace="ti-suporte-desenvolvimento")

        return {"message": "Document upserted successfully"}
    
    except Exception as e:
        
        return {"error": str(e)}
    
def upsertService_metadata(metadata: dict, chunkslistText: list):

    #index = pc.Index(host="https://itvalleyschool-k6qbag2.svc.aped-4627-b74a.pinecone.io") # banco inicial para testes
    #index = pc.Index(host="https://base-de-conhecimentos-chamados-1-k6qbag2.svc.aped-4627-b74a.pinecone.io")    # banco: base-de-conhecimento-chamados-1 -> chamados por filas -> chunk_size=1000, overlap=200
    #index = pc.Index(host="https://base-de-conhecimentos-chamados-2-k6qbag2.svc.aped-4627-b74a.pinecone.io")    # banco: base-de-conhecimento-chamados-2 -> chamados por filas -> chunk_size=1500, overlap=300
    index = pc.Index(host="https://base-de-conhecimento-chamados-3-k6qbag2.svc.aped-4627-b74a.pinecone.io")    # banco: base-de-conhecimento-chamados-3 -> chamados por filas -> chunk_size=2000, overlap=400

    try:

        vectors = []

        for chunkstext in chunkslistText:
            embeddingchunk = embeddingsService(chunkstext)
            metadatacomplete = {**metadata, "chunk": chunkstext}
            '''
            variável metadata
            {"aula": "aula 1", "professor": "nicksson", "chunk": "texto do chunk 1"}
            {"aula": "aula 1", "professor": "nicksson", "chunk": "texto do chunk 2"}
            {"aula": "aula 1", "professor": "nicksson", "chunk": "texto do chunk 3"}
            '''
            vectors.append({"id": f"{uuid.uuid4()}", "values": embeddingchunk, "metadata": metadatacomplete})
        
        response = index.upsert(vectors=vectors, namespace="ti-suporte-desenvolvimento")

        #return {"message": f"Successfully upserted documents with metadata"}
        return response.upserted_count
    
    except Exception as e:

        return {"error": str(e)}

def upsertService_registro_metadata(metadata: dict, chunk: str):

    index = pc.Index(host="https://base-de-conhecimento-chamados-4-k6qbag2.svc.aped-4627-b74a.pinecone.io")    # banco: base-de-conhecimento-chamados-4 -> chamados por registros e por filas -> chunk_size=tamanho_do_registro, overlap=0

    try:

        vectors = []

        embeddingchunk = embeddingsService(chunk)
        metadatacomplete = {**metadata, "chunk": chunk}
        vectors.append({"id": f"{uuid.uuid4()}", "values": embeddingchunk, "metadata": metadatacomplete})
        
        response = index.upsert(vectors=vectors, namespace="ti-suporte-desenvolvimento")

        return response.upserted_count
    
    except Exception as e:

        return {"error": str(e)}