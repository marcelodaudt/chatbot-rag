from services.authenticationService import authentication_pinecone
from services.embeddingsService import embeddingsService

def query_simple(search: str):

    pc = authentication_pinecone()

    try:

        vectors = embeddingsService(search)

        index = pc.Index(host="https://itvalleyschool-k6qbag2.svc.aped-4627-b74a.pinecone.io")

        response = index.query(namespace="ti-suporte-desenvolvimento", vector=vectors, top_k=5, include_metadata=True)
        
        return response
    
    except Exception as e:

        return {"message": str(e)}
