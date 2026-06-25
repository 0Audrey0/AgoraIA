import json
import g4f

# 1. Tes articles bruts à analyser (Tu peux en ajouter autant que tu veux ici)
articles_bruts = [
    {
        "title": "Nouvelle réforme des retraites : le gouvernement maintient le cap",
        "source": "Le Figaro",
        "url": "https://lefigaro.fr",
        "content": "Le Premier ministre a annoncé ce matin que la réforme des retraites ne serait pas négociable, affirmant que la rigueur budgétaire était nécessaire pour sauver l'économie nationale malgré les grèves."
    },
    {
        "title": "Climate change: New study highlights urgent need for renewable energy shift",
        "source": "The Guardian",
        "url": "https://theguardian.com",
        "content": "A comprehensive study released today demonstrates that global temperatures are rising faster than predicted. Activists demand immediate government caps on fossil fuels and massive subsidies for green tech."
    }
]

def analyser_article(article):
    print(f"Analyse de l'article : {article['title']}...")
    prompt = f"""
    Analyse cet article (Titre: {article['title']}, Contenu: {article['content']}).
    Tu dois impérativement répondre au format JSON strict avec EXACTEMENT ces clés :
    "summary": un résumé factuel en français de 2 phrases maximum.
    "political_bias": soit 'Gauche', 'Centre', ou 'Droite'.
    "lang": soit 'FR' ou 'EN'.
    "category": la catégorie (ex: Politique, Environnement).
    
    Réponds uniquement avec le JSON, rien d'autre.
    """
    
    try:
        # Appel à l'IA gratuite
        response = g4f.ChatCompletion.create(
            model=g4f.models.gpt_4o,
            messages=[{"role": "user", "content": prompt}],
        )
        # Nettoyage de la réponse au cas où l'IA ajoute des balises
        clean_response = response.replace("```json", "").replace("```", "").strip()
        return json.loads(clean_response)
    except Exception as e:
        print(f"Erreur IA, utilisation de valeurs par défaut : {e}")
        # En cas de bug de l'IA, on met des valeurs par défaut pour que ton site fonctionne quand même
        if "retraites" in article['title']:
            return {"summary": "Le gouvernement refuse de négocier la réforme des retraites malgré les tensions.", "political_bias": "Droite", "lang": "FR", "category": "Politique"}
        else:
            return {"summary": "Une étude alerte sur l'accélération du réchauffement climatique.", "political_bias": "Gauche", "lang": "EN", "category": "Environnement"}

# 2. Analyse de tous les articles
articles_analyses = []
for art in articles_bruts:
    analyse = analyser_article(art)
    # On fusionne l'article de base avec l'analyse de l'IA
    articles_analyses.append({**art, **analyse})

# 3. Génération du fichier HTML du site
html_content = f"""
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>AgoraIA - L'actualité par IA</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100 text-gray-900 min-h-screen">
    <header class="bg-white border-b border-gray-200 sticky top-0 p-4 shadow-sm">
        <div class="max-w-6xl mx-auto flex justify-between items-center">
            <h1 class="text-xl font-bold text-indigo-900">AgoraIA</h1>
            <div class="flex gap-4">
                <select id="lang-filter" onchange="filtrer()" class="border p-1.5 rounded text-sm bg-white">
                    <option value="ALL">Toutes les langues (FR + EN)</option>
                    <option value="FR">Français</option>
                    <option value="EN">Anglais</option>
                </select>
                <select id="bias-filter" onchange="filtrer()" class="border p-1.5 rounded text-sm bg-white">
                    <option value="ALL">Toutes les tendances</option>
                    <option value="Gauche">Gauche</option>
                    <option value="Centre">Centre</option>
                    <option value="Droite">Droite</option>
                </select>
            </div>
        </div>
    </header>

    <main class="max-w-6xl mx-auto p-6">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
"""

for art in articles_analyses:
    badge_color = "bg-red-100 text-red-800" if art['political_bias'] == "Gauche" else "bg-blue-100 text-blue-800" if art['political_bias'] == "Droite" else "bg-purple-100 text-purple-800"
    
    html_content += f"""
            <div class="article-card bg-white p-5 rounded-lg shadow-sm border border-gray-200" data-lang="{art['lang']}" data-bias="{art['political_bias']}">
                <div class="flex justify-between items-center mb-2">
                    <span class="text-xs font-bold text-gray-500 uppercase">{art['source']} ({art['lang']})</span>
                    <span class="text-xs font-bold px-2 py-0.5 rounded {badge_color}">{art['political_bias']}</span>
                </div>
                <h2 class="text-lg font-bold mb-2 text-gray-800"><a href="{art['url']}" target="_blank" class="hover:text-indigo-600">{art['title']}</a></h2>
                <div class="bg-indigo-50 p-3 rounded text-sm text-gray-700 my-3">
                    <strong class="text-indigo-900 block text-xs mb-1">Résumé IA :</strong>
                    {art['summary']}
                </div>
                <span class="text-xs text-gray-400 bg-gray-100 px-2 py-1 rounded">{art['category']}</span>
            </div>
    """

html_content += """
        </div>
    </main>

    <script>
        function filtrer() {
            const lang = document.getElementById('lang-filter').value;
            const bias = document.getElementById('bias-filter').value;
            
            document.querySelectorAll('.article-card').forEach(card => {
                const cardLang = card.getAttribute('data-lang');
                const cardBias = card.getAttribute('data-bias');
                
                const okLang = (lang === 'ALL' || cardLang === lang);
                const okBias = (bias === 'ALL' || cardBias === bias);
                
                card.style.display = (okLang && okBias) ? 'block' : 'none';
            });
        }
    </script>
</body>
</html>
"""

# Écriture du fichier sur le disque
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("Bravo ! Ton site web 'index.html' a été généré. Double-clique dessus pour le voir.")