import os
import json
from openai import OpenAI

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "your-openai-key-here")
openai_client = OpenAI(api_key=OPENAI_API_KEY)

def get_openai_response(question):
    """Get response from OpenAI for biblical questions"""
    try:
        # Check if API key is properly set
        if not OPENAI_API_KEY or OPENAI_API_KEY == "your-openai-key-here":
            return "⚠️ **API OpenAI non configurée**\n\nLa clé API OpenAI n'est pas configurée correctement. Veuillez contacter l'administrateur.\n\nEn attendant, vous pouvez utiliser nos **50 sujets bibliques prédéfinis** disponibles dans la liste déroulante."
        
        # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
        # do not change this unless explicitly requested by the user
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": """Tu es Kadosh.ia, un assistant biblique chrétien. Réponds aux questions bibliques et spirituelles avec:
                    
1. Des versets bibliques pertinents (au moins 3)
2. Des explications claires et édifiantes
3. Des applications pratiques pour la vie chrétienne
4. Un ton respectueux et encourageant

Format ta réponse en markdown avec des sections claires.
Si la question n'est pas liée à la Bible ou à la spiritualité chrétienne, redirige poliment vers des sujets bibliques."""
                },
                {
                    "role": "user",
                    "content": question
                }
            ],
            max_tokens=800,
            temperature=0.7
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        print(f"Erreur OpenAI: {e}")
        return "⚠️ **Erreur de connexion à OpenAI**\n\nIl semble y avoir un problème avec la clé API ou la connexion à OpenAI.\n\nVeuillez utiliser nos **50 sujets bibliques prédéfinis** disponibles dans la liste déroulante ci-dessus, ou réessayer plus tard."
