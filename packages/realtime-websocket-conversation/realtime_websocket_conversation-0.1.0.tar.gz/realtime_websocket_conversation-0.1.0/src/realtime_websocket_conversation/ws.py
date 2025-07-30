import asyncio
import base64
import json
import logging
from typing import Any

from agents import function_tool
from fastapi import WebSocket, WebSocketDisconnect
from openai import AsyncOpenAI


class FunctionToolInfo:
    def __init__(self, func):
        self.function_tool = function_tool(func)
        for remove_param in ["state", "connection", "kwargs"]:
            self.function_tool.params_json_schema["properties"].pop(remove_param, None)
        self.callable = func

    def __call__(self, *args, **kwargs):
        return self.callable(*args, **kwargs)


def tool(func):
    """
    Decorator to register a function as a tool for the AI to use.
    Your function should either include arguments for state and connection, or include **kwargs.
    State and connection will be passed back to the function when it is called, so that the state
    or the connection session may be updated by the function.
    """
    return FunctionToolInfo(func)


async def handle_websocket_conversation(
    websocket: WebSocket,
    openai_client: AsyncOpenAI,
    model: str = "gpt-4o-realtime-preview",
    voice: str = "alloy",
    system_message: str = "You are a helpful chat assistant.",
    temperature: float = 0.8,
    tools: list[FunctionToolInfo] = [],
    state: Any = None,
):
    """
    Handle the websocket conversation with the client and OpenAI.

    Args:
        websocket (WebSocket): The websocket connection with the client.
        openai_client (AsyncOpenAI): The OpenAI client for communication.
        model (str): The model to be used by OpenAI.
        voice (str): The voice to be used for audio responses.
        system_message (str): The system message for the assistant.
        temperature (float): The temperature setting for the model.
        tools (list[FunctionToolInfo]): The list of tools available for the AI (optional).
        state (Any): The state to be passed to the tools, if any. This should be a mutable object. (optional).
    """
    logging.info("Client connected")
    await websocket.accept()
    async with openai_client.beta.realtime.connect(model=model) as connection:
        stream_sid = None
        response_transcript = ""

        # State variables for interruption handling
        latest_media_timestamp = 0
        response_start_timestamp_twilio = None
        last_assistant_item = None
        mark_queue = []

        await connection.session.update(
            session={
                "turn_detection": {"type": "server_vad"},
                "input_audio_format": "g711_ulaw",
                "output_audio_format": "g711_ulaw",
                "voice": voice,
                "instructions": system_message,
                "modalities": ["text", "audio"],
                "temperature": temperature,
                "input_audio_transcription": {"model": "whisper-1"},
                "tools": [
                    {
                        "type": "function",
                        "name": tool.function_tool.name,
                        "description": tool.function_tool.description,
                        "parameters": tool.function_tool.params_json_schema,
                    }
                    for tool in tools
                ],
                "tool_choice": "auto",
            }
        )

        await connection.conversation.item.create(
            item={
                "type": "message",
                "role": "user",
                "content": [{"type": "input_text", "text": "Say hello to the user!"}],
            }
        )
        await connection.response.create()

        async def send_mark():
            """Send a mark event to track audio position"""
            if stream_sid:
                mark_event = {
                    "event": "mark",
                    "streamSid": stream_sid,
                    "mark": {"name": "responsePart"},
                }
                await websocket.send_json(mark_event)
                mark_queue.append("responsePart")

        async def handle_speech_started_event():
            """Handle interruption when caller starts speaking"""
            nonlocal response_start_timestamp_twilio, last_assistant_item
            logging.info("Handling speech interruption")

            if mark_queue and response_start_timestamp_twilio is not None:
                elapsed_time = latest_media_timestamp - response_start_timestamp_twilio
                logging.info(f"Elapsed time for truncation: {elapsed_time}ms")

                if last_assistant_item:
                    logging.info(f"Truncating response with ID: {last_assistant_item}")
                    await connection.conversation.item.truncate(
                        item_id=last_assistant_item, content_index=0, audio_end_ms=elapsed_time
                    )

                await websocket.send_json({"event": "clear", "streamSid": stream_sid})

                mark_queue.clear()
                last_assistant_item = None
                response_start_timestamp_twilio = None

        async def receive_from_twilio():
            """Receive messages from the Twilio websocket."""
            nonlocal stream_sid, latest_media_timestamp
            try:
                async for message in websocket.iter_text():
                    data = json.loads(message)
                    if data["event"] == "start":
                        stream_sid = data["streamSid"]
                    elif data["event"] == "media":
                        latest_media_timestamp = int(data.get("media", {}).get("timestamp", 0))
                        await connection.input_audio_buffer.append(audio=data["media"]["payload"])
                    elif data["event"] == "mark":
                        if mark_queue:
                            mark_queue.pop(0)
            except WebSocketDisconnect:
                logging.warning("Client disconnected.")
                await connection.close()

        async def receive_from_openai():
            """Receive events from the OpenAI connection."""
            nonlocal response_transcript, last_assistant_item, response_start_timestamp_twilio
            try:
                async for event in connection:
                    if event.type == "response.audio.delta" and event.delta and stream_sid:
                        audio_payload = base64.b64encode(base64.b64decode(event.delta)).decode(
                            "utf-8"
                        )
                        audio_delta = {
                            "event": "media",
                            "streamSid": stream_sid,
                            "media": {"payload": audio_payload},
                        }
                        await websocket.send_json(audio_delta)

                        if response_start_timestamp_twilio is None:
                            response_start_timestamp_twilio = latest_media_timestamp
                            logging.info(
                                f"Setting start timestamp for response: {response_start_timestamp_twilio}ms"
                            )

                        if hasattr(event, "item_id"):
                            last_assistant_item = event.item_id

                        await send_mark()

                    if event.type == "response.audio_transcript.delta":
                        response_transcript += event.delta

                    if event.type == "conversation.item.input_audio_transcription.completed":
                        logging.info(f"===> USER: {event.transcript}")

                    if event.type == "response.audio_transcript.done":
                        logging.info(f"===> ASSISTANT: {response_transcript}")
                        response_transcript = ""

                    if event.type == "input_audio_buffer.speech_started":
                        logging.info("Speech started detected - possible interruption")
                        await handle_speech_started_event()

                    if event.type == "response.done":
                        made_function_call = False
                        if event.response.status == "completed" and event.response.output:
                            for output in event.response.output:
                                if output.type == "function_call":
                                    call_id = output.call_id or ""
                                    name = output.name
                                    arguments = json.loads(output.arguments or "{}")
                                    logging.info(
                                        f"Function call {call_id}: {name} with arguments: {arguments}"
                                    )
                                    tool: FunctionToolInfo = next(
                                        (t for t in tools if t.function_tool.name == name),
                                        None,
                                    )
                                    if not tool:
                                        result = "Function not found."
                                    else:
                                        try:
                                            result = await tool(
                                                **arguments
                                                | {"state": state, "connection": connection}
                                            )
                                        except Exception as e:
                                            logging.error(f"Error calling function: {e}")
                                            result = str(e)

                                    logging.info(f"{call_id} call result: {result}")
                                    await connection.conversation.item.create(
                                        item={
                                            "type": "function_call_output",
                                            "call_id": call_id,
                                            "output": result,
                                        }
                                    )
                                    made_function_call = True
                        if made_function_call:
                            await connection.response.create()

            except Exception as e:
                logging.error(f"OpenAI Error: {e}")

        await asyncio.gather(receive_from_openai(), receive_from_twilio())
