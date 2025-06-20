import core, psycopg2, markdown, os, secrets
from dotenv import load_dotenv
from core import utils as ut
from .authentication import Authentication
from typing import List, Dict
from fastapi import FastAPI, APIRouter
from fastapi.responses import StreamingResponse, HTMLResponse
from pydantic import BaseModel
from datetime import datetime, timedelta

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
                <meta name="viewport" content="width=device-width, initial-scale=1.0" />
                <style>
            body {{
              overflow-x:hidden;
              background-color:#222222;
              width:100%;
              height:100vh;
              font-family:Helvetica;
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

            .text {{
                padding:0% 30% 2% 30%;
                text-align:center;
                color:white;
            }}

            .App-header {{
                min-height: 100vh;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
            }}

            .title {{
                background-color:#6db39f;
                font-size:30px;
                padding:20px 60px;
                margin-bottom:2%;
                color:black;
                border-radius:50px;
                box-shadow:0 0 50px 0 #0b1210;
            }}

            .App-header h1 {{
                margin:0;
            }}

            .Link {{
                transition:0.7s;
                font-weight:bold;
                text-decoration:none;
                color:black;
                padding:10px 20px;
                border:0px;
                border-radius:50px;
            }}

            .Link:hover {{
                transition:0.7s;
                font-weight:bold;
                text-decoration:none;
                color:black;
                padding:10px 20px;
                background-color:#6db39f;
                border-radius:50px;
                box-shadow:0 0 20px 0 #0b1210;
            }}

            .Link:focus {{
                outline:none;
            }}

            .list {{
              width:100%;
              align-items:center;
              display:flex;
              justify-content: center;
            }}

            .main {{
                display:flex;
                justify-content: center;
            }}

            .white-text {{
                color:white;
            }}
            @media only screen and (max-width: 600px) {{
                .title {{
                    background-color:#6db39f;
                    font-size:25px;
                    padding:10px 10px;
                    margin-bottom:2%;
                    color:black;
                    text-align:center;
                    border-radius:50px;
                    box-shadow:0 0 50px 0 #0b1210;
                }}
                .text {{
                    padding:0 20% 2% 20%;
                    margin:0;
                    text-align:center;
                    color:white;
                }}
            }}
                </style>
            </head>
            <body>
            <header class="App-header">
                <h1 class="title center-text">Welcome to Gethonis</h1>
                <section class="text">
                    <p>Gethonis is an API that combines responses from ChatGPT4 and DeepSeek V3. It analyzes the prompt you gave him and he responds with the best version of your response by generating prompt on ChatGPT4 and DeepSeek, compares both responses and it gives the best version of them.</p>
                </section>
                <section class="main">
                    <section class="list white-text">
                        <p>Press on the button to generate a token.</p>
                    </section>   
                </section>
                <section class="main">
                    <section class="list white-text">
                        <p>Token: </p>
                        <pre id="tokenOutput"></pre>
                    </section>   
                </section>
                <section class="main">
                    <section class="list">
                        <button class="Link" onclick="generateToken()">Generate Token</button>
                    </section>
                </section>
                <script>
                    async function generateToken() {{
                        try {{
                            const response = await fetch('/ff12f222abd65e100890215af94c2d02');
                            const data = await response.json();
                            document.getElementById('tokenOutput').textContent = data.token;
                        }} catch (error) {{
                            document.getElementById('tokenOutput').textContent = 'Eroare: ' + error;
                        }}
                    }}
                </script>
                </header>
            </body> 
        </html>
	"""
    return HTMLResponse(content=full_html)

@router.get("/help", response_class=HTMLResponse)
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
        </html>
    """
    return HTMLResponse(content=full_html)

@router.get("/ff12f222abd65e100890215af94c2d02")
def generatetoken():
    load_dotenv()
    SECRET_KEY = str(os.getenv('SECRETKEY'))
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
