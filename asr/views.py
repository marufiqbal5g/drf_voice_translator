import os

from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import AudioSerializer
from .sherpa_service import transcribe_audio


class AudioToTextAPIView(APIView):

    def post(self, request):

        serializer = AudioSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        audio = serializer.validated_data[
            "audio"
        ]

        save_path = (
            f"media/{audio.name}"
        )

        with open(
            save_path,
            "wb+"
        ) as f:

            for chunk in audio.chunks():
                f.write(chunk)

        text = transcribe_audio(
            save_path
        )

        return Response({
            "text": text
        })