# realtime-websocket-conversation

A Python package for building real-time, streaming websocket conversations between Twilio and OpenAI using FastAPI. This library provides a websocket handler that streams audio between a Twilio client and an OpenAI model, enabling interactive voice assistants and conversational AI applications.

The goal of this package is really to reduce the boilerplate code needed to set up a real-time conversation with OpenAI's models.

## Features
- Real-time audio streaming between Twilio and OpenAI
- FastAPI websocket integration
- Supports OpenAI function calling with simple `@tool` decorator (modified & borrowed from [OpenAI's Agent SDK](https://github.com/openai/openai-agents-python))
  - In your tool function signatures, you can use `state` and `connection` parameters to access mutable state and the OpenAI websocket connection (in case you need to update session settings). If you don't need these, use **kwargs in your function signature, as the decorator will pass them anyway.
- Handles interruptions and audio truncation for natural conversations

## Installation
You can install the package using uv:
```bash
uv add realtime-websocket-conversation
```
or with pip:
```bash
pip install realtime-websocket-conversation
```

## Usage Example

### FastAPI Integration
```python
from fastapi import FastAPI, Request, WebSocket
from fastapi.responses import HTMLResponse
from openai import AsyncOpenAI
from realtime_websocket_conversation import handle_websocket_conversation, tool
from twilio.twiml.voice_response import Connect, VoiceResponse

app = FastAPI()
openai_client = AsyncOpenAI()

@app.get("/incoming-call", response_class=HTMLResponse)
async def incoming_call(request: Request):
    response = VoiceResponse()
    response.say("Connecting your call...")
    host = (
        request.headers.get("X-Forwarded-Host")
        or request.headers.get("Host")
        or request.url.hostname
    )
    connect = Connect()
    connect.stream(url=f"wss://{host}/media-stream")
    response.append(connect)
    return HTMLResponse(content=str(response), media_type="application/xml")

@app.websocket("/media-stream")
async def media_stream(websocket: WebSocket):
    await handle_websocket_conversation(
        websocket=websocket,
        openai_client=openai_client,
        model="gpt-4o-realtime-preview",
        voice="alloy",
        system_message="You are a helpful chat assistant.",
        temperature=0.8,
        tools=[],  # Optionally pass tool functions
        state={},  # Optionally pass a mutable state object, to be passed to tool functions
    )
```
Point your Twilio webhook to the `/incoming-call` endpoint, and the websocket connection will be established when a call is received.

### Registering a Tool Function
```python
from realtime_websocket_conversation import tool

@tool
def get_time(state=None, connection=None):
    from datetime import datetime
    return {"time": datetime.now().isoformat()}
```

Add your tool functions to the `tools` list when calling `handle_websocket_conversation`, i.e. `[get_time]`.
