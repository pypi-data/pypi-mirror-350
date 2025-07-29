# ambientagi/provider/voicecaller.py

import asyncio
import base64
import json

import websockets
from fastapi import FastAPI, Request, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.websockets import WebSocketDisconnect
from twilio.rest import Client
from twilio.twiml.voice_response import Connect, VoiceResponse


class TwilioVoiceAgent:
    def __init__(
        self,
        openai_api_key: str,
        twilio_account_sid: str,
        twilio_auth_token: str,
        twilio_caller_id: str,
        voice: str = "alloy",
        temperature: float = 0.8,
    ):
        self.OPENAI_API_KEY = openai_api_key
        self.client = Client(twilio_account_sid, twilio_auth_token)
        self.twilio_caller_id = twilio_caller_id
        self.voice = voice
        self.temperature = temperature

    def make_call(self, to_number: str, instructions_url: str) -> str:
        """Initiate an outbound call and connect to a voice stream."""
        call = self.client.calls.create(
            to=to_number,
            from_=self.twilio_caller_id,
            url=instructions_url,
        )
        return call.sid

    def register_routes(
        self,
        app: FastAPI,
        system_message: str,
        path_prefix: str = "/voice-agent",
    ):
        """Mounts required routes into a FastAPI app for Twilio voice stream."""
        self.system_message = system_message  # user-defined persona or task

        @app.api_route(f"{path_prefix}/twiml", methods=["GET", "POST"])
        async def stream_twiml(request: Request):
            host = request.url.hostname
            response = VoiceResponse()
            response.say("Connecting to your AI voice assistant now...")
            connect = Connect()
            connect.stream(url=f"wss://{host}{path_prefix}/media-stream")
            response.append(connect)
            return HTMLResponse(str(response), media_type="application/xml")

        @app.websocket(f"{path_prefix}/media-stream")
        async def handle_media_stream(websocket: WebSocket):
            await websocket.accept()
            stream_sid = None
            print("🔊 Media stream connected")

            async with websockets.connect(
                "wss://api.openai.com/v1/realtime?model=gpt-4o-realtime-preview-2024-10-01",
                extra_headers={
                    "Authorization": f"Bearer {self.OPENAI_API_KEY}",
                    "OpenAI-Beta": "realtime=v1",
                },
            ) as openai_ws:

                await self.send_session_update(openai_ws)

                async def receive_from_twilio():
                    nonlocal stream_sid
                    try:
                        async for message in websocket.iter_text():
                            data = json.loads(message)
                            if data["event"] == "media" and openai_ws.open:
                                await openai_ws.send(
                                    json.dumps(
                                        {
                                            "type": "input_audio_buffer.append",
                                            "audio": data["media"]["payload"],
                                        }
                                    )
                                )
                            elif data["event"] == "start":
                                stream_sid = data["start"]["streamSid"]
                    except WebSocketDisconnect:
                        print("🔌 Client disconnected.")
                        if openai_ws.open:
                            await openai_ws.close()

                async def send_to_twilio():
                    try:
                        async for openai_message in openai_ws:
                            response = json.loads(openai_message)
                            if response.get(
                                "type"
                            ) == "response.audio.delta" and response.get("delta"):
                                try:
                                    audio_payload = base64.b64encode(
                                        base64.b64decode(response["delta"])
                                    ).decode("utf-8")
                                    await websocket.send_json(
                                        {
                                            "event": "media",
                                            "streamSid": stream_sid,
                                            "media": {"payload": audio_payload},
                                        }
                                    )
                                except Exception as e:
                                    print("⚠️ Audio processing error:", e)
                    except Exception as e:
                        print("⚠️ Stream error:", e)

                await asyncio.gather(receive_from_twilio(), send_to_twilio())

    async def send_session_update(self, openai_ws):
        update = {
            "type": "session.update",
            "session": {
                "turn_detection": {"type": "server_vad"},
                "input_audio_format": "g711_ulaw",
                "output_audio_format": "g711_ulaw",
                "voice": self.voice,
                "instructions": self.system_message,
                "modalities": ["text", "audio"],
                "temperature": self.temperature,
            },
        }
        await openai_ws.send(json.dumps(update))
