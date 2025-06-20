import core, psycopg2, markdown
from core import utils as ut
from .authentication import Authentication
from typing import List, Dict
from fastapi import FastAPI, APIRouter
from fastapi.responses import StreamingResponse, HTMLResponse
from pydantic import BaseModel

router = APIRouter()

@router.get("/help", response_class=HTMLResponse)
def custom_docs():
    with open("docs/", "r") as f:
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
            </body> 
        </html>
	"""
    return HTMLResponse(content=full_html)

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
