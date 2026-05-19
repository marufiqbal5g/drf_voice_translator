import json
import numpy as np
from channels.generic.websocket import AsyncWebsocketConsumer
from .stream_service import StreamingASR


class AudioStreamConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.asr = StreamingASR()
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):

        if bytes_data:

            # Convert raw PCM float32
            import numpy as np

            audio = np.frombuffer(bytes_data, dtype=np.float32)

            result = self.asr.accept_audio(audio.tolist())

            await self.send(text_data=json.dumps({
                "partial": str(result)
            }, ensure_ascii=False))

        elif text_data:

            msg = json.loads(text_data)

            if msg.get("event") == "end":

                final_text = self.asr.finish()

                await self.send(text_data=json.dumps({
                    "final": str(final_text)
                }, ensure_ascii=False))

    async def disconnect(self, close_code):
        pass