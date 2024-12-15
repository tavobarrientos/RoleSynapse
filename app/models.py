from sqlalchemy import Column, Integer, String, DateTime
from database import Base

#"""
# Define las tablas de la base de datos utilizando SQLAlchemy
# Cada clase corresponde a una tabla con sus respectivas columnas y tipos de datos

#"""

#registros de auditoría
class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True, index=True)
    action = Column(String, index=True)
    user = Column(String, index=True)
    timestamp = Column(DateTime)

# reglas de filtrado 
class FilterRule(Base):
    __tablename__ = "filter_rules"
    id = Column(Integer, primary_key=True, index=True)
    role = Column(String, index=True)
    rule = Column(String)
