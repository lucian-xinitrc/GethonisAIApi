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
from fastapi.responses import PlainTextResponse
from prometheus_client import Counter, generate_latest
import os
from pydantic import BaseModel
from fastapi import Query, Header, HTTPException
from cryptography.fernet import Fernet, InvalidToken
from dotenv import load_dotenv
# Router initialiser
router = APIRouter()
REQUEST_COUNT = Counter('api_requests_total', 'Total API requests')
# Initialising directory ( the dir were the html files will be)
templates = Jinja2Templates(directory="templates")

# Main Page displayer
@router.get("/")
def custom_docs(request: Request):
    return templates.TemplateResponse(request, "index.html")

@router.post("/dates")
def dates(info: ut.Verf):
    token = info.token
    if(token == "12021908"):
        load_dotenv()
        db = Authentication()
        cursor = db.conn.cursor()
        query = """
            SELECT friday, saturday, sunday, monday, extra, extrafri, extrasat, extrasan, extramon
            FROM bubusbirth
            WHERE id=%s
        """
        try:
            data = (1,)
            cursor.execute(query, data)
            result = cursor.fetchone()
            if result: 
                friday, saturday, sunday, monday, extra, extrafri, extrasat, extrasan, extramon = result
                db.conn.commit()
                return {"status": "Success", "friday": friday, "saturday": saturday, "sunday": sunday, "monday": monday, "extra": extra, "extrafri": extrafri, "extrasat": extrasat, "extrasan": extrasan, "extramon": extramon}
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
        UPDATE esp32sensorreceiver
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

@router.post("/arduinobubu")
def arduino(ardu: ut.ArduinoTemp):
    temp = ardu.temp
    humi = ardu.humi
    load_dotenv()
    db = Authentication()
    cursor = db.conn.cursor()
    insert_query = """
        UPDATE esp32sensorreceiver
        SET temp = %s,
            humi = %s
        WHERE id = 2
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
        FROM esp32sensorreceiver
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

@router.get("/tempbubu")
def temp():
    load_dotenv()
    db = Authentication()
    cursor = db.conn.cursor()
    insert_query = """
        SELECT temp, humi
        FROM esp32sensorreceiver
        WHERE id=%s
    """
    try:
        data = (2,)
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

@router.post("/api/gethonisDebate")
def response_gethonis_debate(action: ut.Message):
    if(action.messages != "" and action.headers != ""):
        token = action.headers
        message = action.messages
        if action.stream:
            return ut.streaming(token, message, "text/plain", 5)
        return ut.non_streaming(token, message, "text/plain", 5)
    else:
        return "The parameters cannot be empty!"

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

FLIPPER_API_TOKEN = os.getenv("FLIPPER_API_TOKEN")
FLIPPER_MESSAGE_KEY = os.getenv("FLIPPER_MESSAGE_KEY")

if not FLIPPER_API_TOKEN:
    raise RuntimeError("FLIPPER_API_TOKEN is not configured")

if not FLIPPER_MESSAGE_KEY:
    raise RuntimeError("FLIPPER_MESSAGE_KEY is not configured")

fernet = Fernet(FLIPPER_MESSAGE_KEY.encode())


class FlipperMessage(BaseModel):
    sender: str
    content: str


def check_flipper_token(token: str):
    if token != FLIPPER_API_TOKEN:
        raise HTTPException(
            status_code=401,
            detail="Invalid Flipper token"
        )


@router.post("/messages")
def send_flipper_message(
    message: FlipperMessage,
    x_flipper_token: str = Header(default="")
):
    check_flipper_token(x_flipper_token)

    content = message.content.strip()
    sender = message.sender.strip()

    if not content:
        raise HTTPException(
            status_code=400,
            detail="Message cannot be empty"
        )

    if len(content) > 200:
        raise HTTPException(
            status_code=400,
            detail="Message too long"
        )

    if len(sender) > 32:
        raise HTTPException(
            status_code=400,
            detail="Sender too long"
        )

    db = Authentication()
    cursor = db.conn.cursor()

    try:
        query = """
            INSERT INTO public.flipper_messages
            (sender, content)
            VALUES (%s, %s)
            RETURNING id, sender, content, created_at
        """

        cursor.execute(
            query,
            (sender, content)
        )

        result = cursor.fetchone()

        db.conn.commit()

        return {
            "status": "success",
            "id": result[0],
            "sender": result[1],
            "content": result[2],
            "created_at": result[3].isoformat()
        }

    except Exception as e:
        db.conn.rollback()

        return {
            "status": "error",
            "error": str(e)
        }

    finally:
        cursor.close()
        db.conn.close()


@router.get("/messages")
def get_flipper_messages(
    after_id: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=50),
    x_flipper_token: str = Header(default="")
):
    check_flipper_token(x_flipper_token)

    db = Authentication()
    cursor = db.conn.cursor()

    try:
        query = """
            SELECT id, sender, content, created_at
            FROM public.flipper_messages
            WHERE id > %s
            ORDER BY id ASC
            LIMIT %s
        """

        cursor.execute(
            query,
            (after_id, limit)
        )

        rows = cursor.fetchall()

        messages = []

        for row in rows:
            messages.append({
                "id": row[0],
                "sender": row[1],
                "content": row[2],
                "created_at": row[3].isoformat()
            })

        return {
            "status": "success",
            "messages": messages
        }

    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }

    finally:
        cursor.close()
        db.conn.close()

