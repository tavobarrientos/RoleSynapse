from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import AuditLog
from database import get_db
from datetime import datetime
from auth import get_current_role  # ya que depende de la simulación de roles

router = APIRouter()

# Endpoint para registrar una acción de auditoria
@router.post("/log")
def log_action(action: str, db: Session = Depends(get_db), user: str = Depends(get_current_role)):
    """
    Registra una acción en la tabla audit_logs.
    - `action`: Descripción de la acción realizada.
    - `user`: Usuario autenticado que realizó la acción.
    """
    log_entry = AuditLog(action=action, user=user, timestamp=datetime.now())
    db.add(log_entry)
    db.commit()
    db.refresh(log_entry)
    return {"message": "Action logged successfully", "log_id": log_entry.id}

# Endpoint para obtener los registros de auditoria
@router.get("/logs")
def get_logs(db: Session = Depends(get_db), role: str = Depends(get_current_role)):
    """
    Devuelve todos los registros de auditoría desde la tabla audit_logs.
    Solo accesible para usuarios con rol 'admin'.
    """
    if role != "admin":
        raise HTTPException(status_code=403, detail="Access denied")
    
    logs = db.query(AuditLog).all()
    return {
        "logs": [
            {"id": log.id, "action": log.action, "user": log.user, "timestamp": log.timestamp}
            for log in logs
        ]
    }
