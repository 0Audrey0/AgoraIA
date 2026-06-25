import os
from openai import OpenAI

# Remplace par ta clé d'API ou utilise les variables d'environnement
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "TA_CLE_ICI"))

def analyze_article_with_ia(title, content):
    """
    Envoie l'article à l'IA pour obtenir le résumé et le bord politique au format JSON.
    """
    prompt = f"""
    Analyse l'article suivant (Titre: {title}, Contenu: {content}).
    Tu dois impérativement répondre au format JSON strict avec les clés suivantes :
    - "summary": Un résumé factuel et objectif en 3 puces maximum (en français).
    - "political_bias": Le bord politique parmi ces options uniquement : 'Gauche', 'Centre-Gauche', 'Centre', 'Centre-Droite', 'Droite'.
    - "confidence_score": Un score de confiance de ton choix entre 0 et 100.
    - "lang": La langue d'origine de l'article ('FR' ou 'EN').
    - "category": La catégorie de l'article ('Politique', 'Économie', 'Tech', 'Société', 'International').

    Réponds uniquement avec le JSON, aucun autre texte.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini", # Modèle très économique et rapide
            messages=[
                {"role": "system", "content": "Tu es un analyste politique et média expert et neutre."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"} # Force le retour en JSON
        )
        
        # On récupère et retourne le dictionnaire JSON
        import json
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        print(f"Erreur lors de l'analyse IA : {e}")
        return None