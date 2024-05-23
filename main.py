from fastapi import FastAPI
from database import models
from database.db import engine
from routes import users, products, cart, auth


app = FastAPI()
models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(products.router)
app.include_router(cart.router)


@app.get('/')
async def root():
    return "Привет!"
