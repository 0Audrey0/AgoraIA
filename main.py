import sqlite3
from ai_analyzer import analyze_article_with_ia

def insert_article(article_data):
    conn = sqlite3.connect('journal.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT OR IGNORE INTO articles 
            (title, source, url, content, lang, category, summary, political_bias, confidence_score)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            article_data['title'],
            article_data['source'],
            article_data['url'],
            article_data['content'],
            article_data['lang'],
            article_data['category'],
            article_data['summary'],
            article_data['political_bias'],
            article_data['confidence_score']
        ))
        conn.commit()
        print(f"Article inséré : {article_data['title']} -> Classé à {article_data['political_bias']}")
    except Exception as e:
        print(f"Erreur insertion : {e}")
    finally:
        conn.close()

# SIMULATION : Un faux article pour tester le pipeline
faux_article = {
    "title": "Nouvelle réforme des retraites : le gouvernement maintient le cap",
    "source": "Le Figaro",
    "url": "https://lefigaro.fr/exemple1",
    "content": "Le Premier ministre a annoncé ce matin que la réforme des retraites ne serait pas négociable, affirmant que la rigueur budgétaire était nécessaire pour sauver l'économie nationale malgré les grèves."
}

print("Analyse de l'article par l'IA en cours...")
ai_result = analyze_article_with_ia(faux_article['title'], faux_article['content'])

if ai_result:
    # On fusionne les données de base et l'analyse de l'IA
    complete_article = {**faux_article, **ai_result}
    insert_article(complete_article)