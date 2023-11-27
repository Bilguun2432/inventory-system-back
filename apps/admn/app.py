from fastapi import FastAPI
from .router import auth, auth_user, auth_role
from .router import product_category, product
from .router import transfer
from .router import employee
from .router import action_status, action


app = FastAPI()


app.include_router(auth.router)
app.include_router(auth_user.router)
app.include_router(auth_role.router)
app.include_router(product_category.router)
app.include_router(product.router)
app.include_router(transfer.router)
app.include_router(employee.router)
app.include_router(action_status.router)
app.include_router(action.router)