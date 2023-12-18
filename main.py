from fastapi import FastAPI, Request
from app.routers import user, restaurant, cart_item, order
import uvicorn
from starlette.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.include_router(restaurant.router, prefix='/restaurant')
app.include_router(cart_item.router, prefix='/cart_item')
app.include_router(user.router, prefix='/user')
app.include_router(order.router, prefix='/order')

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def root():
    return RedirectResponse('Login.html')


@app.get("/Login.html")
def login_view(request: Request):
    return templates.TemplateResponse("Login.html", {"request": request})


@app.get("/Register.html")
def register_view(request: Request):
    return templates.TemplateResponse("Register.html", {"request": request})


if __name__ == '__main__':
    uvicorn.run(app='main:app', host='0.0.0.0', port=8000,
                reload=True, debug=True)
