from services.authenticationService import authentication_openai

clientOpenAI = authentication_openai()

def assistant_question(question: str, shortextract: str):
    
    try:
        # Criando o PROMPT
        response = clientOpenAI.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful support information technology assistant, which will respond only based on the excerpt (context) sent to you. If the context do not have the answer, say that you don't know."},
                {"role": "user", "content": f"The question is {question} and the excerpt (context) is {shortextract}"},
            ]
        )

        return response.choices[0].message.content
    
    except Exception as e:

        return {"message": str(e)}
