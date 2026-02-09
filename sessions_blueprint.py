import uuid

from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from database import get_db, query, query_one, excute
from auth_middleware import get_current_user

router = APIRouter(prefix="/sessions", tags=["sessions"])

class SessionCreate(BaseModel):
    soundscape_id: str
    volume_used: = 0.75

class SessionUpdate(BaseModel):
    ended_at: datetime: = None
    duration_actual: int = 0
    completed: bool = False

@router.post("")
def create_session(data: SessionCreate, user=Depends(get_current_user), conn=Depends(get_db)):
    session_id = str(uuid.uuid4())
    sql = """
        INSERT INTO sessions(id, user_id, soundscape_id, volume_used)
        VALUES (%s, %s, %s, %s)
        RETURNING *
    """
    with conc.cursor() as cur:
        cur.execute(sql, (session_id, user["id"], data.soundscapes_id, date.volume_used))
        con.commit()
            return cur.fetchone()

@router.patch("/{session_id}")
def update_session(session_id: str, data: SessionUpdate, user=Depends(get_current_user), conn=Depends(get_db)):
    sql = """
        UPDATE sessions
        SET ended_at = %s, duration_actual = %s, completed = %s
        WHERE id = %s AND user_id = %s 
        RETURNING *
    """
    with conn.cursor() as cur:
        cur.execute(sql, (data.ended_at, data.duration_actual, data.completed, session_id, user["id"]))
        conn.commit()
        result = cur.fetchone()
        if not result:
            raise HTTPException(status_code=404, detail="session not found")
            return result

@router.get("")
def get_user_sessions(user=Depends(get_current_user), conn=Depends(get_db)):
    sql = """
        SELECT s.*,   sc.name AS soundscape_name, sc.category, sc.genre
        FROM sessions s
        JOIN soundscapes sc ON s.soundscape_id = sc.id
        WHERE s.user_id = %s
        ORDER BY s.started_at DESC
    """
    return query(conn,sql, (user["id"],))              
                                