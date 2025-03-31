from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
import os

app = FastAPI()

@app.get("/data")
def get_data():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        database=os.getenv("DB_NAME", "geodata"),
        user=os.getenv("DB_USER", "roger"),
        password=os.getenv("DB_PASSWORD", "motdepassefort")
    )
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("""
        SELECT
            t.nom AS territoire,
            i.nom AS indicateur,
            vi.date,
            vi.valeur,
            s.nom AS source,
            cg.nom AS couche_geographique
        FROM valeur_indicateur vi
        JOIN territoire t ON vi.territoire_id = t.id
        JOIN indicateur i ON vi.indicateur_id = i.id
        LEFT JOIN source s ON i.source_id = s.id
        LEFT JOIN couche_geographique cg ON cg.territoire_id = t.id;
    """)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result
