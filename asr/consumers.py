import json
import numpy as np

from channels.generic.websocket import AsyncWebsocketConsumer
from .stream_service import StreamingASR
from .translator import bn_to_en


class AudioStreamConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        self.asr = StreamingASR()

        await self.accept()

        print("WebSocket Connected")

    async def receive(self, text_data=None, bytes_data=None):

        try:

            # AUDIO STREAM
            if bytes_data:

                audio = np.frombuffer(
                    bytes_data,
                    dtype=np.float32
                )

                result = self.asr.accept_audio(
                    audio.tolist()
                )

                bangla_text = str(result)

                english_text = bn_to_en(bangla_text) if bangla_text else ""

                await self.send(text_data=json.dumps({

                    "partial": bangla_text,
                    "translation": english_text

                }, ensure_ascii=False))

            # CONTROL MESSAGE
            elif text_data:

                msg = json.loads(text_data)

                if msg.get("event") == "end":

                    final_text = self.asr.finish()

                    bangla_final = str(final_text)

                    english_final = bn_to_en(bangla_final) if bangla_final else ""

                    await self.send(text_data=json.dumps({

                        "final": bangla_final,
                        "final_translation": english_final

                    }, ensure_ascii=False))

        except Exception as e:

            print("WEBSOCKET ERROR:", e)

            await self.send(text_data=json.dumps({
                "final": f"ERROR: {str(e)}"
            }))

    async def disconnect(self, close_code):

        print("WebSocket Disconnected")
        