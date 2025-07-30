from fastapi import FastAPI
from type_less.inject import fastapi_app_inject_types
from .matching import validate_openapi_has_return_schema

def test_fastapi_basic():
    app = FastAPI()

    @app.get("/root/before")
    async def root_before():
        return {"message": "Hello World"}

    injected_app = fastapi_app_inject_types(app)

    @app.get("/root/after")
    async def root_after():
        return {"message": "Hello World"}

    assert type(app) == type(injected_app)

    # Validate generated OpenAPI
    openapi_spec = app.openapi()

    assert openapi_spec is not None
    assert not validate_openapi_has_return_schema(openapi_spec, "/root/before", "get")
    assert validate_openapi_has_return_schema(openapi_spec, "/root/after", "get")
