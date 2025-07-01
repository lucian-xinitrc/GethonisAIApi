import os, openai, dotenv
from random import randint
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

def openai(message, stream):
    client = OpenAI(api_key=os.getenv("TOKENOPENAI"))
    response = client.chat.completions.create(
        model='gpt-4o',
        messages=message,
        stream=stream
    )
    if stream:
        for chunk in response:
            if hasattr(chunk.choices[0].delta, "content") and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
    else:
        yield response.choices[0].message.content

def secondai(ainame, message, stream):
    creds = { 
        1:{
            'token': os.getenv("TOKENGROK"),
            'baseUrl': os.getenv("GROKBASEURL"),
            'modelName': os.getenv("GROKMODELNAME")
        },
        2:{
            'token': os.getenv("TOKENDEEPSEEK"),
            'baseUrl': os.getenv("DEEPSEEKBASEURL"),
            'modelName': os.getenv("DEEPSEEKMODELNAME")
        }        
    }
    client = OpenAI(api_key=creds[ainame]['token'], base_url=creds[ainame]['baseUrl'])

    response = client.chat.completions.create(
        model=creds[ainame]['modelName'],
        messages=message,
        stream=stream
    )
    if stream:
        for chunk in response:
            if hasattr(chunk.choices[0].delta, "content") and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
    else: 
        yield response.choices[0].message.content
        
