from app.routers import products, categories, carts, users, auth, accounts
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from fastapi import Request

# Get the base directory
BASE_DIR = Path(__file__).resolve().parent

# Setup templates
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Mount static files
app = FastAPI()
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

description = """
Welcome to the E-commerce API! 🚀

This API provides a comprehensive set of functionalities for managing your e-commerce platform.

Key features include:

- **Crud**
	- Create, Read, Update, and Delete endpoints.
- **Search**
	- Find specific information with parameters and pagination.
- **Auth**
	- Verify user/system identity.
	- Secure with Access and Refresh tokens.
- **Permission**
	- Assign roles with specific permissions.
	- Different access levels for User/Admin.
- **Validation**
	- Ensure accurate and secure input data.


For any inquiries, please contact:

* Github: https://github.com/aliseyedi01
"""


app = FastAPI(
    description=description,
    title="E-commerce API",
    version="1.0.0",
    contact={
        "name": "Ali Seyedi",
        "url": "https://github.com/aliseyedi01",
    },
    swagger_ui_parameters={
        "syntaxHighlight.theme": "monokai",
        "layout": "BaseLayout",
        "filter": True,
        "tryItOutEnabled": True,
        "onComplete": "Ok"
    },
)


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


app.include_router(products.router)
app.include_router(categories.router)
app.include_router(carts.router)
app.include_router(users.router)
app.include_router(accounts.router)
app.include_router(auth.router)

# Handler for Vercel
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
handler = app
