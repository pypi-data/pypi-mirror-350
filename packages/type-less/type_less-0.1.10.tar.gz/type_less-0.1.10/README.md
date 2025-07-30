![Type-Less PyPI](https://img.shields.io/pypi/v/type-less)

# Type Less

Find yourself typing less with automatic type inference for Python!  Inject function return types at runtime for code generation 🤙.

## FastAPI Example

```python
class User:
    id: int
    first: str
    last: str

@app.get("/user/me")
def user_me(user: User):
    return {
        "id": user.id,
        "balance": 13.37,
        "name": {
            "first": user.first,
            "last": user.last,
        },
    }
```

🚀 Generates Return Types:

```python
class UserMeReturnName(TypedDict):
    first: str
    last: str

class UserMeReturn(TypedDict):
    id: int
    balance: Literal[13.37]
    name: UserMeReturnName
```

📋 OpenAPI Spec:

<img src="docs/example.png" alt="OpenAPI Example" height="170">

## Using in FastAPI Project

Inject types before by hooking before setting up routes.  Types will be automatically generated when new routes are added.

```python
from type_less.inject import inject_fastapi_route_types
from fastapi import FastAPI

app = FastAPI()
app = inject_fastapi_route_types(app)

@app.get("/test")
def test(request):
    ...
```

## TODO:
### Add Support:
 * Nested class inference
 * Deep function call / return inference
### Better Way?:
 * Possibly use pyright, pyre, mypy, or anything else to infer the type?
   * Tracking [pyright request](https://github.com/microsoft/pyright/issues/10394) - DENIED
### Cleanup:
 * Possibly refactor - a large portion of the initial work was codegen from claude and has patterns that need rethinking of proper documentation