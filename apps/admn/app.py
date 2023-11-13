from fastapi import FastAPI
from .router import auth, auth_user, auth_role, auth_permission
from .router import product_category, product


app = FastAPI()


app.include_router(auth.router)
app.include_router(auth_user.router)
app.include_router(auth_permission.router)
app.include_router(auth_role.router)
app.include_router(product_category.router)
app.include_router(product.router)
