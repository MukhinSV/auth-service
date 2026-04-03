import uvicorn
import sys
from fastapi import FastAPI
from pathlib import Path

from starlette.responses import JSONResponse

from src.exceptions import UserUnauthorisedHTTPException

sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.api.auth import router as auth_router
from src.api.user import router as user_router
from src.api.admin import router as admin_router

app = FastAPI()
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(admin_router)

@app.exception_handler(UserUnauthorisedHTTPException)
async def auth_exception_handler(request, exc):
    response = JSONResponse({"detail": "Unauthorized"}, status_code=401)
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return response

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True)
