from fastapi import APIRouter, Depends, HTTPException
from auth import get_current_role

router = APIRouter()

# Politicas en memoria para simplificar
policies = [
    {"role": "user", "access_level": "restricted"},
    {"role": "admin", "access_level": "full"}
]

@router.get("/policies")
def get_policies(role: str = Depends(get_current_role)):
    """
    Devuelve las políticas de acceso.
    Solo los administradores pueden ver
    """
    if role != "admin":
        raise HTTPException(status_code=403, detail="Access denied")
    return policies
