from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas import ContentRequest, ContentResponse
from models import FilterRule
from database import get_db

router = APIRouter()

# Endpoint para filtrar contenido basado en las reglas y roles
@router.post("/content", response_model=ContentResponse)
def filter_content(request: ContentRequest, db: Session = Depends(get_db)):
    """
    Filtra el contenido basado en las reglas asociadas al rol del usuario.
    """
    # Obtener todas las reglas aplicables al rol del usuario
    rules = db.query(FilterRule).filter(FilterRule.role == request.role).all()
    
    if not rules:
        # Si no hay reglas configuradas para este rol, devolver contenido redactado
        return {"filtered_content": "REDACTED"}

    # Aplicar cada regla al contenido
    filtered_content = request.content
    for rule in rules:
        if "replace:" in rule.rule:  # Ejemplo: "replace: confidential -> REDACTED"
            try:
                _, pattern, replacement = rule.rule.split(": ")
                filtered_content = filtered_content.replace(pattern.strip(), replacement.strip())
            except ValueError:
                raise HTTPException(status_code=400, detail=f"Invalid rule format: {rule.rule}")
        elif "redact" in rule.rule:  # Ejemplo: "redact"
            filtered_content = "REDACTED"
        elif "delete" in rule.rule:  # Ejemplo: "delete: [Confidential]"
            try:
                _, pattern = rule.rule.split(": ")
                filtered_content = filtered_content.replace(pattern.strip(), "")
            except ValueError:
                raise HTTPException(status_code=400, detail=f"Invalid rule format: {rule.rule}")

    return {"filtered_content": filtered_content}

# Endpoint para agregar una nueva regla de filtrado
@router.post("/rules")
def add_filter_rule(role: str, rule: str, db: Session = Depends(get_db)):
    """
    Agrega una nueva regla de filtrado asociada a un rol específico.
    """
    new_rule = FilterRule(role=role, rule=rule)
    db.add(new_rule)
    db.commit()
    return {"message": "Rule added successfully"}

# Endpoint para obtener todas las reglas de filtrado
@router.get("/rules")
def get_filter_rules(db: Session = Depends(get_db)):
    """
    Obtiene todas las reglas de filtrado configuradas en el sistema.
    """
    rules = db.query(FilterRule).all()
    return {"rules": [{"id": rule.id, "role": rule.role, "rule": rule.rule} for rule in rules]}

# Endpoint para eliminar una regla de filtrado especifica
@router.delete("/rules/{rule_id}")
def delete_filter_rule(rule_id: int, db: Session = Depends(get_db)):
    """
    Elimina una regla de filtrado basada en su ID.
    """
    rule = db.query(FilterRule).filter(FilterRule.id == rule_id).first()
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")
    db.delete(rule)
    db.commit()
    return {"message": "Rule deleted successfully"}
