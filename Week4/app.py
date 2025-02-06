from typing import Annotated
from fastapi import FastAPI, Request, Form, status, Response, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()
# middleware
app.add_middleware(SessionMiddleware, secret_key="session_key")
# print("Middlewares:", app.user_middleware)

app.mount("/static", StaticFiles(directory="static"), name="static666")
templates = Jinja2Templates(directory="templates")


# 處理HTTPException
@app.exception_handler(HTTPException)
async def httpException_handler(request: Request, exc: HTTPException):
    if exc.status_code == 404:
        return RedirectResponse(url=f"/error?message={exc.detail}", status_code=status.HTTP_302_FOUND)


@app.get("/")
async def form_data(request: Request):
    return templates.TemplateResponse(request, name="home.html")


@app.post("/signin", status_code=status.HTTP_302_FOUND)
async def sign_in(username: Annotated[str, Form()], password: Annotated[str, Form()], request: Request):
    if username == "test" and password == "test":
        session = request.session
        session["SIGNED-IN"] = True
        session["username"] = username
        return RedirectResponse(url="/member", status_code=status.HTTP_302_FOUND)
    elif username == "" or password == "":
        message = "Please enter username and password."
        return RedirectResponse(url=f"/error?message={message}", status_code=status.HTTP_302_FOUND,)
    else:
        message = "Username or password is not correct."
        return RedirectResponse(url=f"/error?message={message}", status_code=status.HTTP_302_FOUND, )


@app.get("/member")
async def success_page(request: Request):
    if request.session.get("SIGNED-IN"):
        username = request.session.get("username")
        return templates.TemplateResponse(request, name="success.html", context={"username": username})
    return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)


@app.get("/error")
async def error_page(message: str, request: Request,):
    return templates.TemplateResponse(request, name="error.html", context={"error_message": message})


@app.get("/signout")
async def sign_out(request: Request):
    session = request.session
    session["SIGNED-IN"] = False
    return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)


@app.get("/square/{number}")
async def calculate(request: Request, number: str):
    try:
        num = int(number)
        if num >= 0:
            res = num**2
            return templates.TemplateResponse(request, name="calculate_result.html", context={"result": res})
        else:
            raise ValueError
    except ValueError:
        message = "請輸入正整數"
        return RedirectResponse(url=f"/error?message={message}", status_code=status.HTTP_302_FOUND, )


# 處理任何找不到的頁面
@app.get("/{full_path:path}")
async def not_exist_path(request: Request, full_path: str):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Page was not found.")
