import sqlite3

def init_db():
    conn = sqlite3.connect('journal.db')
    cursor = conn.cursor()
    
    # Création de la table pour stocker les articles
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            source TEXT,
            url TEXT UNIQUE,
            content TEXT,
            lang TEXT,         -- 'FR' ou 'EN'
            category TEXT,     -- 'Politique', 'Tech', 'Éco', etc.
            summary TEXT,      -- Généré par l'IA
            political_bias TEXT, -- 'Gauche', 'Centre', 'Droite', etc.
            confidence_score INTEGER,
            published_at TEXT
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Base de données initialisée avec succès !")

if __name__ == '__main__':
    init_db()
    import sqlite3

def init_db():
    conn = sqlite3.connect('journal.db')
    cursor = conn.cursor()
    
    # Création de la table pour stocker les articles
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            source TEXT,
            url TEXT UNIQUE,
            content TEXT,
            lang TEXT,         -- 'FR' ou 'EN'
            category TEXT,     -- 'Politique', 'Tech', 'Éco', etc.
            summary TEXT,      -- Généré par l'IA
            political_bias TEXT, -- 'Gauche', 'Centre', 'Droite', etc.
            confidence_score INTEGER,
            published_at TEXT
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Base de données initialisée avec succès !")

if __name__ == '__main__':
    init_db()