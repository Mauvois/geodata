from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
import psycopg2
from psycopg2.extras import RealDictCursor
import os

app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "ok", "env": os.getenv("ENV", "staging")}

@app.get("/data")
def get_data():
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST", "localhost"),
            database=os.getenv("DB_NAME", "geodata"),
            user=os.getenv("DB_USER", "roger"),
            password=os.getenv("DB_PASSWORD", "motdepassefort")
        )
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        # cursor.execute("""
        #     SELECT
        #         t.nom AS territoire,
        #         i.nom AS indicateur,
        #         vi.date,
        #         vi.valeur,
        #         s.nom AS source,
        #         cg.nom AS couche_geographique
        #     FROM valeur_indicateur vi
        #     JOIN territoire t ON vi.territoire_id = t.id
        #     JOIN indicateur i ON vi.indicateur_id = i.id
        #     LEFT JOIN source s ON i.source_id = s.id
        #     LEFT JOIN couche_geographique cg ON cg.territoire_id = t.id;
        # """)

        cursor.execute("""
            SELECT
                tc.table_schema,
                tc.table_name,
                kcu.column_name,
                ccu.table_schema AS foreign_table_schema,
                ccu.table_name AS foreign_table_name,
                ccu.column_name AS foreign_column_name
            FROM
                information_schema.table_constraints AS tc
            JOIN
                information_schema.key_column_usage AS kcu
                ON tc.constraint_name = kcu.constraint_name
            JOIN
                information_schema.constraint_column_usage AS ccu
                ON ccu.constraint_name = tc.constraint_name
            WHERE
                tc.constraint_type = 'FOREIGN KEY'
            ORDER BY
                tc.table_schema, tc.table_name;
        """)
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"error": str(e)})
