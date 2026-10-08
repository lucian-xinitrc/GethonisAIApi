import core
import psycopg2
import markdown
import os
import secrets
import requests
import json

from core import utils as ut
from typing import List, Dict
from dotenv import load_dotenv
from pydantic import BaseModel
from datetime import datetime, timedelta

from .authentication import Authentication

from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import (
    FastAPI,
    APIRouter,
    Request,
    Query,
    Header,
    HTTPException
)

from fastapi.responses import (
    StreamingResponse,
    HTMLResponse,
    PlainTextResponse
)

from prometheus_client import Counter, generate_latest


# ============================================================
# ROUTER
# ============================================================

router = APIRouter()

print("========================================")
print("API.PY LOADED")
print("Flipper routes will be registered")
print("========================================")


REQUEST_COUNT = Counter(
    "api_requests_total",
    "Total API requests"
)


# ============================================================
# TEMPLATES
# ============================================================

templates = Jinja2Templates(
    directory="templates"
)


# ============================================================
# MAIN PAGE
# ============================================================

@router.get("/")
def custom_docs(request: Request):
    return templates.TemplateResponse(
        request,
        "index.html"
    )


# ============================================================
# DATES
# ============================================================

@router.post("/dates")
def dates(info: ut.Verf):

    token = info.token

    if token != "12021908":
        return {
            "status": "Invalid token"
        }

    load_dotenv()

    db = Authentication()
    cursor = db.conn.cursor()

    query = """
        SELECT
            friday,
            saturday,
            sunday,
            monday,
            extra,
            extrafri,
            extrasat,
            extrasan,
            extramon
        FROM bubusbirth
        WHERE id = %s
    """

    try:

        cursor.execute(
            query,
            (1,)
        )

        result = cursor.fetchone()

        if result:

            (
                friday,
                saturday,
                sunday,
                monday,
                extra,
                extrafri,
                extrasat,
                extrasan,
                extramon
            ) = result

            return {
                "status": "Success",
                "friday": friday,
                "saturday": saturday,
                "sunday": sunday,
                "monday": monday,
                "extra": extra,
                "extrafri": extrafri,
                "extrasat": extrasat,
                "extrasan": extrasan,
                "extramon": extramon
            }

        return {
            "status": "error"
        }

    except Exception as e:

        db.conn.rollback()

        return {
            "status": str(e)
        }

    finally:

        cursor.close()
        db.conn.close()


# ============================================================
# ARDUINO
# ============================================================

@router.post("/arduino")
def arduino(ardu: ut.ArduinoTemp):

    temp = ardu.temp
    humi = ardu.humi

    load_dotenv()

    db = Authentication()
    cursor = db.conn.cursor()

    query = """
        UPDATE esp32sensorreceiver
        SET
            temp = %s,
            humi = %s
        WHERE id = 1
    """

    try:

        cursor.execute(
            query,
            (temp, humi)
        )

        db.conn.commit()

        return {
            "status": "Succesfully sent!"
        }

    except Exception as e:

        db.conn.rollback()

        return {
            "status": str(e)
        }

    finally:

        cursor.close()
        db.conn.close()


# ============================================================
# ARDUINO BUBU
# ============================================================

@router.post("/arduinobubu")
def arduino_bubu(ardu: ut.ArduinoTemp):

    temp = ardu.temp
    humi = ardu.humi

    load_dotenv()

    db = Authentication()
    cursor = db.conn.cursor()

    query = """
        UPDATE esp32sensorreceiver
        SET
            temp = %s,
            humi = %s
        WHERE id = 2
    """

    try:

        cursor.execute(
            query,
            (temp, humi)
        )

        db.conn.commit()

        return {
            "status": "Succesfully sent!"
        }

    except Exception as e:

        db.conn.rollback()

        return {
            "status": str(e)
        }

    finally:

        cursor.close()
        db.conn.close()


# ============================================================
# TEMPERATURE
# ============================================================

@router.get("/temp")
def temp():

    load_dotenv()

    db = Authentication()
    cursor = db.conn.cursor()

    query = """
        SELECT temp, humi
        FROM esp32sensorreceiver
        WHERE id = %s
    """

    try:

        cursor.execute(
            query,
            (1,)
        )

        result = cursor.fetchone()

        if result:

            temp_value, humi_value = result

            return {
                "status": "Success",
                "temp": temp_value,
                "humi": humi_value
            }

        return {
            "status": "error"
        }

    except Exception as e:

        return {
            "status": str(e)
        }

    finally:

        cursor.close()
        db.conn.close()


# ============================================================
# TEMPERATURE BUBU
# ============================================================

@router.get("/tempbubu")
def temp_bubu():

    load_dotenv()

    db = Authentication()
    cursor = db.conn.cursor()

    query = """
        SELECT temp, humi
        FROM esp32sensorreceiver
        WHERE id = %s
    """

    try:

        cursor.execute(
            query,
            (2,)
        )

        result = cursor.fetchone()

        if result:

            temp_value, humi_value = result

            return {
                "status": "Success",
                "temp": temp_value,
                "humi": humi_value
            }

        return {
            "status": "error"
        }

    except Exception as e:

        return {
            "status": str(e)
        }

    finally:

        cursor.close()
        db.conn.close()


# ============================================================
# GENERATE TOKEN
# ============================================================

@router.get("/genToken")
def generatetoken():

    load_dotenv()

    db = Authentication()
    cursor = db.conn.cursor()

    query = """
        INSERT INTO tokens
        (token, tries)
        VALUES (%s, %s)
    """

    token = "geth-" + secrets.token_urlsafe(16)

    try:

        cursor.execute(
            query,
            (token, 0)
        )

        db.conn.commit()

        return {
            "token": token
        }

    except Exception as e:

        db.conn.rollback()

        print(
            "Eroare la inserare în DB:",
            e
        )

        return {
            "error": str(e)
        }

    finally:

        cursor.close()
        db.conn.close()


# ============================================================
# AUTHORISATION
# ============================================================

@router.post("/api/authorisation")
def check(tryIt: ut.Try):

    try:

        conn = Authentication()

        conn.check_auth(
            tryIt.token
        )

        if conn.auth is True:

            return {
                "Status": "Positive"
            }

    except Exception:

        pass

    return {
        "Status": "Negative"
    }


# ============================================================
# GETHONIS
# ============================================================

@router.post("/api/gethonis")
def response_gethonis(action: ut.Message):

    token = action.headers
    message = action.messages

    if action.stream:

        return ut.streaming(
            token,
            message,
            "text/plain",
            1
        )

    return ut.non_streaming(
        token,
        message,
        "text/plain",
        1
    )


# ============================================================
# GETHONIS DEBATE
# ============================================================

@router.post("/api/gethonisDebate")
def response_gethonis_debate(action: ut.Message):

    if (
        action.messages != ""
        and action.headers != ""
    ):

        token = action.headers
        message = action.messages

        if action.stream:

            return ut.streaming(
                token,
                message,
                "text/plain",
                5
            )

        return ut.non_streaming(
            token,
            message,
            "text/plain",
            5
        )

    return {
        "error": "The parameters cannot be empty!"
    }


# ============================================================
# POST
# ============================================================

@router.post("/api/post")
def get_post(postc: ut.PostContent):

    token = postc.headers
    post_type = postc.type
    message = postc.prompt

    return ut.post_returning(
        token,
        post_type,
        message,
        1
    )


# ============================================================
# CHECK POST
# ============================================================

@router.post("/api/checkpost")
def check_post(check: ut.PostVerify):

    token = check.headers
    idy = check.id

    db = Authentication()

    try:

        db.check_auth(token)

        cursor = db.conn.cursor()

        cursor.execute(
            """
            SELECT content
            FROM public.posts
            WHERE bot_id = %s
            """,
            (idy,)
        )

        result = cursor.fetchone()

        if result:

            cursor.execute(
                """
                DELETE FROM public.posts
                WHERE bot_id = %s
                """,
                (idy,)
            )

            db.conn.commit()

            cursor.close()

            return result

        cursor.close()

        return {
            "Status": "No posts yet."
        }

    finally:

        db.conn.close()


# ============================================================
# ADD POST
# ============================================================

@router.post("/api/addpost")
async def add_post(add: ut.PostAdd):

    token = add.headers
    idy = add.id
    prompty = add.prompt

    date_gen = ut.post_returning(
        token,
        "",
        prompty,
        1
    )

    db = Authentication()

    try:

        db.check_auth(token)

        cursor = db.conn.cursor()

        date = next(date_gen)

        cursor.execute(
            """
            SELECT *
            FROM public.posts
            WHERE bot_id = %s
            """,
            (idy,)
        )

        result = cursor.fetchone()

        if result:

            cursor.execute(
                """
                UPDATE public.posts
                SET content = %s
                WHERE bot_id = %s
                """,
                (date, idy)
            )

        else:

            cursor.execute(
                """
                INSERT INTO public.posts
                (bot_id, content)
                VALUES (%s, %s)
                """,
                (idy, date)
            )

        db.conn.commit()

        cursor.close()

        return {
            "status": "ok"
        }

    finally:

        db.conn.close()


# ============================================================
# OPENAI
# ============================================================

@router.post("/api/openai")
def response_openai(action: ut.Message):

    token = action.headers
    message = action.messages

    if action.stream:

        return ut.streaming(
            token,
            message,
            "text/plain",
            2
        )

    return ut.non_streaming(
        token,
        message,
        "text/plain",
        2
    )


# ============================================================
# GROK
# ============================================================

@router.post("/api/grok")
def response_grok(action: ut.Message):

    token = action.headers
    message = action.messages

    if action.stream:

        return ut.streaming(
            token,
            message,
            "text/plain",
            3
        )

    return ut.non_streaming(
        token,
        message,
        "text/plain",
        3
    )


# ============================================================
# FLIPPER
# ============================================================

FLIPPER_API_TOKEN = os.getenv(
    "FLIPPER_API_TOKEN"
)

if not FLIPPER_API_TOKEN:

    raise RuntimeError(
        "FLIPPER_API_TOKEN is not configured"
    )


class FlipperMessage(BaseModel):

    sender: str
    content: str


def check_flipper_token(token: str):

    if token != FLIPPER_API_TOKEN:

        raise HTTPException(
            status_code=401,
            detail="Invalid Flipper token"
        )


# ============================================================
# FLIPPER - SEND MESSAGE
# ============================================================

@router.post("/messages")
def send_flipper_message(
    message: FlipperMessage,
    x_flipper_token: str = Header(default="")
):

    print("========== FLIPPER POST ==========")

    check_flipper_token(
        x_flipper_token
    )

    content = message.content.strip()
    sender = message.sender.strip()

    print("Sender:", sender)
    print("Content:", content)

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
            (
                sender,
                content
            )
        )

        result = cursor.fetchone()

        db.conn.commit()

        print(
            "Flipper message inserted:",
            result[0]
        )

        return {
            "status": "success",
            "id": result[0],
            "sender": result[1],
            "content": result[2],
            "created_at": result[3].isoformat()
        }

    except Exception as e:

        db.conn.rollback()

        print(
            "FLIPPER POST ERROR:",
            e
        )

        return {
            "status": "error",
            "error": str(e)
        }

    finally:

        cursor.close()
        db.conn.close()


# ============================================================
# FLIPPER - GET MESSAGES
# ============================================================

@router.get("/messages")
def get_flipper_messages(
    after_id: int = Query(
        default=0,
        ge=0
    ),
    limit: int = Query(
        default=20,
        ge=1,
        le=50
    ),
    x_flipper_token: str = Header(default="")
):

    print("========== FLIPPER GET ==========")

    check_flipper_token(
        x_flipper_token
    )

    db = Authentication()
    cursor = db.conn.cursor()

    try:

        query = """
            SELECT
                id,
                sender,
                content,
                created_at
            FROM public.flipper_messages
            WHERE id > %s
            ORDER BY id ASC
            LIMIT %s
        """

        cursor.execute(
            query,
            (
                after_id,
                limit
            )
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

        print(
            "Messages returned:",
            len(messages)
        )

        return {
            "status": "success",
            "messages": messages
        }

    except Exception as e:

        print(
            "FLIPPER GET ERROR:",
            e
        )

        return {
            "status": "error",
            "error": str(e)
        }

    finally:

        cursor.close()
        db.conn.close()


# ============================================================
# ROUTE DEBUG
# ============================================================

print("========================================")
print("REGISTERED ROUTES IN API.PY")
print("========================================")

for route in router.routes:

    print(
        getattr(route, "path", ""),
        getattr(route, "methods", "")
    )

print("========================================")