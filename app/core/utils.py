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