from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference
from api.routes.auth import auth_routes
from api.routes.user import user_routes

app = FastAPI(title="Autenticação com JWT")

@app.get("/scalar", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(
        # Your OpenAPI document
        openapi_url=app.openapi_url,
        # Avoid CORS issues (optional)
        scalar_proxy_url="https://proxy.scalar.com",
    )

app.include_router(auth_routes.router)
app.include_router(user_routes.router)