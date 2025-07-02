import core
import api.authentication as auth
from typing import List, Dict
from random import randint
from fastapi import FastAPI, APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

class Message(BaseModel):
	headers: str
	messages: List[Dict]
	stream: bool

class Try(BaseModel):
	token: str

class PostContent(BaseModel):
	headers: str
	type: str
	prompt: List[Dict]

def streaming(token, message, mediatype, choice):
	conn = auth.Authentication()
	conn.check_auth(token)
	if conn.auth:
		if choice == 1: 
			openai_response = ''.join(core.openai(message, False))
			deepseek_response = ''.join(core.secondai(1, message, False))
			random = randint(0, 1)
			message.append({"role": "user", "content": f"Analyze those messages and give the best version combined without letting the user to know that, here are the messages First Message: ### {openai_response} ### Second Response: {deepseek_response}"})
			if random == 1:
				return StreamingResponse(core.openai(message, True), media_type=mediatype)
			return StreamingResponse(core.secondai(1, message, True), media_type=mediatype)
		else:
			if choice == 2:
				return StreamingResponse(core.openai(message, True), media_type=mediatype)
			else:
				if choice == 3:
					return StreamingResponse(core.secondai(1, message, True), media_type=mediatype)
	return "Unfortunately you don't have permission"

def non_streaming(token, message, mediatype, choice):
	conn = auth.Authentication()
	conn.check_auth(token)
	if conn.auth:
		if choice == 1:
			openai_response = ''.join(core.openai(message, False))
			deepseek_response = ''.join(core.secondai(1, message, False))
			random = randint(0, 1)
			message.append({"role": "user", "content": f"Analyze those messages and give the best version combined without letting the user to know that, here are the messages First Message: ### {openai_response} ### Second Response: {deepseek_response}"})
			if random == 1:
				return core.openai(message, False)
			return core.secondai(1, message, False)
		else:
			if choice == 2:
				return core.openai(message, False)
			else:
				if choice == 3:
					return core.secondai(1, message, False)
	return "Unfortunately you don't have permission"

def post_returning(token, type, message, choice):
	if choice == 1:
		openai_response = ''.join(core.openai(message, False))
		deepseek_response = ''.join(core.secondai(1, message, False))
		random = randint(0, 1)
		message.append({"role": "user", "content": f"""
					You are a rewriting assistant. Merge the following two AI responses into one seamless and consistent text, without revealing that they were merged:

					Response 1:
					### {openai_response} ###

					Response 2:
					{deepseek_response}

					Your job:
					- Fuse their ideas into a unified, creative article
					- Keep the language natural, flowing, and on-topic
					- Avoid repetitions and contradictions
					- Return ONLY a JSON object in the format below — no explanation, no comments

					Format:
					{{
					  "Post": {{
					    "Title": "Title of Post",
					    "paragraphs": [
					      "Paragraph 1 (start strong, intro)",
					      "Paragraph 2 (develop idea)",
					      "Paragraph 3 (add insight or vision)"
					    ],
					    "Footer": "Footer"
					  }}
					}}
				"""})
		if random == 1:
			return core.openai(message, False)
		return core.secondai(1, message, False)
	else:
		if choice == 2:
			return core.openai(message, False)
		else:
			if choice == 3:
				return core.secondai(1, message, False)
	return "Unfortunately you don't have permission"

