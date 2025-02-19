from typing import Annotated, Optional
from fastapi import FastAPI, Request, Form, status, Response, HTTPException, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import mysql.connector.cursor
from starlette.middleware.sessions import SessionMiddleware
import mysql.connector
from pydantic import BaseModel

import os
from dotenv import load_dotenv

load_dotenv()
PASSWORD = os.getenv("PASSWORD")

app = FastAPI()
# middleware
app.add_middleware(SessionMiddleware, secret_key="session_key")
# print("Middlewares:", app.user_middleware)

app.mount("/static", StaticFiles(directory="static"), name="static666")
templates = Jinja2Templates(directory="templates")
MEMBER = 'member'
MESSAGE = "message"


class UserForm(BaseModel):
    name: Optional[str] = None
    username: str
    password: str

    @classmethod
    def form(cls,
             name: Optional[str] = Form(None),
             username: str = Form(...),
             password: str = Form(...)
             ):
        return cls(name=name,  username=username, password=password)


# database connection
def get_db():
    conn = mysql.connector.connect(user="root", password=PASSWORD,
                                   host='127.0.0.1', database='website')
    cursor = conn.cursor(dictionary=True)
    print("SQL connected successfully.")
    try:
        yield cursor
        conn.commit()
    finally:
        cursor.close()
        conn.close()


# 處理HTTPException
@app.exception_handler(HTTPException)
def http_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == 400:
        return RedirectResponse(url=f"/error?message={exc.detail}", status_code=status.HTTP_302_FOUND)
    if exc.status_code == 401:
        return RedirectResponse(url=f"/error?message={exc.detail}", status_code=status.HTTP_302_FOUND,)
    if exc.status_code == 404:
        return RedirectResponse(url=f"/error?message={exc.detail}", status_code=status.HTTP_302_FOUND)


@app.get("/")
def form_data(request: Request):
    return templates.TemplateResponse(request, name="home.html")


@app.post('/signup')
def create_user(userForm: Annotated[UserForm, Depends(UserForm.form)], db=Depends(get_db)):
    db.execute(
        f"SELECT * FROM {MEMBER} WHERE username= %s", (userForm.username,))
    user = db.fetchone()
    # print(user)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Repeated username")

    sql_stat = f"INSERT INTO {MEMBER} (name, username, password) VALUES (%s, %s, %s)"
    values = (userForm.name, userForm.username, userForm.password)
    db.execute(sql_stat, values)
    print("User create successfully.")
    return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)


@app.post("/signin", status_code=status.HTTP_302_FOUND)
def sign_in(request: Request, userForm: Annotated[UserForm, Depends(UserForm.form)], db=Depends(get_db)):
    db.execute(f"SELECT * FROM {MEMBER} WHERE username=%s AND password=%s",
               (userForm.username, userForm.password))
    user = db.fetchone()
    if user:
        session = request.session
        session["id"] = user.get("id")
        session["name"] = user.get("name")
        session["username"] = user.get("username")
        return RedirectResponse(url="/member", status_code=status.HTTP_302_FOUND)

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Username or password is not correct")


@app.get("/member")
def success_page(request: Request, db=Depends(get_db)):
    username = request.session.get("username")
    if username:
        id = request.session.get("id")
        db.execute(
            f"SELECT {MEMBER}.id, {MEMBER}.name, {MESSAGE}.content, {MESSAGE}.id AS message_id FROM {MESSAGE} INNER JOIN {MEMBER} ON {MESSAGE}.member_id={MEMBER}.id ")
        msg = db.fetchall()
        print(msg)
        return templates.TemplateResponse(request, name="success.html", context={"username": username, "msg": msg, "user_id": id})
    return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)


@app.get("/signout")
def sign_out(request: Request):
    request.session.clear()
    return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)


@app.post('/createMessage')
def create_message(request: Request, db=Depends(get_db), msg: str = Form()):
    id = request.session.get("id")
    stat = f"INSERT INTO {MESSAGE} (member_id, content) VALUES (%s, %s)"
    values = (id, msg)
    db.execute(stat, values)
    return RedirectResponse(url="/member", status_code=status.HTTP_302_FOUND)


@app.post('/deleteMessage/{id}')
def delete_message(request: Request, id: int, db=Depends(get_db)):

    db.execute(f'DELETE FROM {MESSAGE} WHERE id={id}')
    print("Delete msg succefully.")
    return RedirectResponse(url="/member", status_code=status.HTTP_302_FOUND)


@app.get("/error")
def error_page(message: str, request: Request,):
    return templates.TemplateResponse(request, name="error.html", context={"error_message": message})


# 處理任何找不到的頁面
@app.get("/{full_path:path}")
def not_exist_path(request: Request, full_path: str):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Page was not found.")
