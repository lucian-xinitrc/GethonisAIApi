import core, psycopg2, markdown
from core import utils as ut
from .authentication import Authentication
from typing import List, Dict
from fastapi import FastAPI, APIRouter
from fastapi.responses import StreamingResponse, HTMLResponse
from pydantic import BaseModel
from datetime import datetime, timedelta
import jwt

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
def custom_docs():
    with open("docs/README.md", "r") as f:
        content = f.read()
    html_content = markdown.markdown(content, extensions=["fenced_code", "tables"])

    full_html = f"""
        <html>
            <head>
                <title>Docs</title>
                <style>
                    body {{
                background-color: #121212;
                color: #e0e0e0;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                max-width: 800px;
                margin: auto;
                padding: 20px;
            }}
            h1, h2, h3, h4 {{
                color: #ffffff;
            }}
            a {{
                color: #90caf9;
            }}
            pre {{
                background-color: #1e1e1e;
                color: #cfcfcf;
                padding: 10px;
                overflow-x: auto;
                border-radius: 5px;
            }}
            code {{
                background-color: #1e1e1e;
                color: #ffcc00;
                padding: 2px 5px;
                border-radius: 3px;
            }}
            table {{
                border-collapse: collapse;
                width: 100%;
            }}
            th, td {{
                border: 1px solid #444;
                padding: 8px;
                text-align: left;
            }}
            th {{
                background-color: #222;
                color: #fff;
            }}
            tr:nth-child(even) {{
                        background-color: #1a1a1a;
                    }}
                </style>
            </head>
            <body>
	            {html_content}
                <p>Apasă pe buton pentru a genera un token:</p>
                <button onclick="genereazaToken()">Generează Token</button>
                <pre id="tokenOutput"></pre>
                <script>
                    async function genereazaToken() {{
                        try {{
                            const response = await fetch('/ff12f222abd65e100890215af94c2d02');
                            const data = await response.json();
                            document.getElementById('tokenOutput').textContent = data.token;
                        }} catch (error) {{
                            document.getElementById('tokenOutput').textContent = 'Eroare: ' + error;
                        }}
                    }}
                </script>
            </body> 
        </html>
	"""
    return HTMLResponse(content=full_html)

@router.get("/ff12f222abd65e100890215af94c2d02")
def generatetoken():
    db = Authentication().conn
    cursor = db.cursor()
    insert_query = """
        INSERT INTO tokens (token, tries)
        VALUES (%s, %s);
        """

    payload = {
        "sub": "user_id",
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    data = (token, 0)
    cursor.execute(insert_query, data)
    db.commit()
    return {"token": token}

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
	

@router.post("/api/openai")
def response_openai(action: ut.Message):
	token = action.headers
	message = action.messages
	if action.stream:
		return ut.streaming(token, message, "text/plain", 2)
	return ut.non_streaming(token, message, "text/plain", 2)

@router.post("/api/deepseek")
def response_deepseek(action: ut.Message):
	token = action.headers
	message = action.messages
	if action.stream:
		return ut.streaming(token, message, "text/plain", 3)
	return ut.non_streaming(token, message, "text/plain", 3)
