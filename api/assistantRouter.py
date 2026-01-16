from fastapi import APIRouter
from services.queryService import query_simple
from services.assistantService import assistant_question

router = APIRouter()

@router.post('/api/assistant/query', summary="Query the database vector simple and return a intelligent response")
async def assistant_query(search: str):

    response_dbvectorextract = query_simple(search=search)

    response = assistant_question(question=search, shortextract=response_dbvectorextract)

    return response


###
# 1) Rota
# 2) Função
# 3) Retorno