from fastapi import APIRouter, Depends, HTTPException
from database import get_db, query, query_one

router = APIRouter(prefix="/soundscapes", tags=["soundscapes"])

@router. get("")
def get_all_soundscapes(category: str = None, conn=Depends(get_db)):
    if category:
        sql = "SELECT * FROM soundscapes WHERE category = %s ORDER BY name"
        return query(conn, sql, (category,))
    else:
        sql = "SELECT *FROM soundscapes ORDER BY name"
        return query(conn, sql)

@router.get("/{soundscape_id}")
def get_soundscape(soundscape_id: str, conn=Depends(get_db)):
    sql = "SELECT* FROM soundscapes WHERE id  = %s"
    soundscape = query_one(conn, sql, (soundscape_id))
    if not soundscape:
        raise HTTPExcepetion(status_code 404, detail="Soundscape not found")
        return soundscape            