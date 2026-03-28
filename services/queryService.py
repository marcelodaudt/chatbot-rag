from services.authenticationService import authentication_pinecone
from services.embeddingsService import embeddingsService

def query_simple(search: str):

    pc = authentication_pinecone()

    try:

        vectors = embeddingsService(search)

        # EXPERIMENTOS:
        # Experimento 1
        #index = pc.Index(host="https://experiment-1-knowledge-base-chunk-500-k6qbag2.svc.aped-4627-b74a.pinecone.io")
        # Experimento 2
        #index = pc.Index(host="https://experiment-2-knowledge-base-chunk-1000-k6qbag2.svc.aped-4627-b74a.pinecone.io")
        # Experimento 3
        #index = pc.Index(host="https://experiment-3-knowledge-base-chunk-2000-k6qbag2.svc.aped-4627-b74a.pinecone.io")
        # Experimento 4
        index = pc.Index(host="https://experiment-4-knowledge-base-chunk-1000-k6qbag2.svc.aped-4627-b74a.pinecone.io")
        # Experimento 5
        index = pc.Index(host="https://experiment-5-knowledge-base-chunk-by-call-k6qbag2.svc.aped-4627-b74a.pinecone.io")

        response = index.query(namespace="knowledge-base", vector=vectors, top_k=3, include_metadata=True)
        
        return response
    
    except Exception as e:

        return {"message": str(e)}
