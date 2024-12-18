from fastapi import FastAPI
from routes import filter, audit, access

app = FastAPI(title="Content Moderation API")

# Registrar las rutas
app.include_router(filter.router, prefix="/filter", tags=["Filtering"])
app.include_router(audit.router, prefix="/audit", tags=["Audit"])
