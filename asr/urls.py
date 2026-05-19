from django.urls import path

from .views import AudioToTextAPIView

urlpatterns = [
    path(
        "speech-to-text/",
        AudioToTextAPIView.as_view()
    )
]