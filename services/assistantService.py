from services.authenticationService import authentication_openai
import json

clientOpenAI = authentication_openai()

def assistant_question(question: str, shortextract: str):
    
    try:
        # 1. Definimos a lista de mensagens em uma variável própria primeiro
        prompt_messages = [
            {"role": "system", "content": "You are a helpful support information technology assistant, which will respond only based on the excerpt (context) sent to you. If the context do not have the answer, say that you don't know."},
            {"role": "user", "content": f"The question is {question} and the excerpt (context) is {shortextract}"},
        ]

        # 2. Agora imprimimos a variável que criamos
        print("--- PROMPT ENVIADO ---")
        print(json.dumps(prompt_messages, indent=4, ensure_ascii=False))
        print("----------------------")

        # 3. Passamos a variável para a API
        response = clientOpenAI.chat.completions.create(
            model="gpt-4o-mini",
            messages=prompt_messages
        )
        
        return response.choices[0].message.content
    
    except Exception as e:
        return {"message": str(e)}
