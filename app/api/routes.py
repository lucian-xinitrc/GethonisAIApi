import core, psycopg2, markdown, os, secrets, requests, json
from core import utils as ut
from typing import List, Dict
from dotenv import load_dotenv
from pydantic import BaseModel
from datetime import datetime, timedelta
from .authentication import Authentication
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, APIRouter, Request
from fastapi.responses import StreamingResponse, HTMLResponse

# Router initialiser
router = APIRouter()

# Initialising directory ( the dir were the html files will be)
templates = Jinja2Templates(directory="templates")

# Main Page displayer
@router.get("/")
def custom_docs(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.post("/dates")
def dates(info: ut.Verf):
    token = info.token
    if(token == "12021908"):
        load_dotenv()
        db = Authentication()
        cursor = db.conn.cursor()
        query = """
            SELECT friday, saturday, sunday, monday, extra
            FROM bubusbirth
            WHERE id=%s
        """
        try:
            data = (1,)
            cursor.execute(query, data)
            result = cursor.fetchone()
            if result: 
                friday, saturday, sunday, monday, extra = result
                db.conn.commit()
                return {"status": "Success", "friday": friday, "saturday": saturday, "sunday": sunday, "monday": monday, "extra": extra}
            else :
                return {"status": "error"}
        except Exception as e:
            return {"status": str(e)}
    else:
        return {"status": str(e)}


@router.post("/arduino")
def arduino(ardu: ut.ArduinoTemp):
    temp = ardu.temp
    humi = ardu.humi
    load_dotenv()
    db = Authentication()
    cursor = db.conn.cursor()
    insert_query = """
        UPDATE temphumi
        SET temp = %s,
            humi = %s
        WHERE id = 1
    """
    try:
        data = (temp, humi)
        cursor.execute(insert_query, data)
        db.conn.commit()
        return {"status": "Succesfully sent!"}
    except Exception as e:
        return {"status": str(e)}

@router.get("/temp")
def temp():
    load_dotenv()
    db = Authentication()
    cursor = db.conn.cursor()
    insert_query = """
        SELECT temp, humi
        FROM temphumi
        WHERE id=%s
    """
    try:
        data = (1,)
        cursor.execute(insert_query, data)
        result = cursor.fetchone()
        if result: 
            temp, humi = result
            db.conn.commit()
            return {"status": "Success", "temp": temp, "humi": humi}
        else :
            return {"status": "error"}
    except Exception as e:
        return {"status": str(e)}

# The route get route that generates the API Key
@router.get("/genToken")
def generatetoken():
    load_dotenv()
    db = Authentication()
    cursor = db.conn.cursor()
    insert_query = """
        INSERT INTO tokens (token, tries)
        VALUES (%s, %s);
        """
    token = "geth-" + secrets.token_urlsafe(16)
    try:
        data = (token, 0)
        cursor.execute(insert_query, data)
        db.conn.commit()
        return {"token": token}
    except Exception as e:
        print("Eroare la inserare în DB:", e)
        return {"error": str(e)}

# The token authorisation path
@router.post("/api/authorisation")
def check(tryIt: ut.Try):
	try:
		conn = Authentication()
		conn.check_auth(tryIt.token)
		if conn.auth == True:
			return {"Status": "Positive"}
	except:
		return {"Status": "Negative"}

@router.post("/api/gethonis")
def response_gethonis(action: ut.Message):
	token = action.headers
	message = action.messages
	if action.stream:
		return ut.streaming(token, message, "text/plain", 1)
	return ut.non_streaming(token, message, "text/plain", 1)

@router.post("/api/post")
def get_post(postc: ut.PostContent):
    token = postc.headers
    type = postc.type
    message = postc.prompt
    return ut.post_returning(token, type, message, 1)

@router.post("/api/checkpost")
def check_post(check: ut.PostVerify):
    token = check.headers
    idy = check.id

    db = Authentication()
    db.check_auth(token)
    checkPostData = db.conn.cursor()

    checkPostData.execute(
        "SELECT content FROM public.posts WHERE bot_id = %s",
        (idy,)
    )
    result = checkPostData.fetchone()
    if result:
        checkPostData.execute(
            "DELETE FROM public.posts WHERE bot_id = %s",
            (idy,)
        )
        db.conn.commit()
        checkPostData.close()
        return result
    else:
        return {'Status': "No posts yet."}

@router.post("/api/addpost")
async def add_post(add: ut.PostAdd):
    token = add.headers
    idy = add.id
    prompty = add.prompt
    date_gen = ut.post_returning(token, "", prompty, 1)

    db = Authentication()
    db.check_auth(token)
    addPostData = db.conn.cursor()

    date = next(date_gen)

    addPostData.execute(
        "SELECT * FROM public.posts WHERE bot_id = %s",
        (idy,)
    )
    result = addPostData.fetchone()
    if(result):
        addPostData.execute(
            "UPDATE public.posts SET content = %s WHERE bot_id = %s;",
            (date, idy)
        )
    else:
        addPostData.execute(
            "INSERT INTO public.posts (bot_id, content) VALUES (%s, %s)",
            (idy, date)
        )

    db.conn.commit()
    addPostData.close()
    return {"status": "ok"}

@router.post("/api/openai")
def response_openai(action: ut.Message):
	token = action.headers
	message = action.messages
	if action.stream:
		return ut.streaming(token, message, "text/plain", 2)
	return ut.non_streaming(token, message, "text/plain", 2)

@router.post("/api/grok")
def response_grok(action: ut.Message):
	token = action.headers
	message = action.messages
	if action.stream:
		return ut.streaming(token, message, "text/plain", 3)
	return ut.non_streaming(token, message, "text/plain", 3)

@router.post("/api/deepseek")
def response_deepseek(action: ut.Message):
    token = action.headers
    message = action.messages
    if action.stream:
        return ut.streaming(token, message, "text/plain", 4)
    return ut.non_streaming(token, message, "text/plain", 4)

