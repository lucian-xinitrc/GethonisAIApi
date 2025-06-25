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

def deepseek(message, stream):
    client = OpenAI(api_key=os.getenv("TOKENDEEPSEEK"), base_url=os.getenv("DEEPSEEKBASEURL"))

    response = client.chat.completions.create(
        model=os.getenv("DEEPSEEKMODELNAME"),
        messages=message,
        stream=stream
    )
    if stream:
        for chunk in response:
            if hasattr(chunk.choices[0].delta, "content") and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
    else: 
        yield response.choices[0].message.content
        
