from django.urls import path
from .views import AudioToTextAPIView, test_page

urlpatterns = [
    path("speech-to-text/", AudioToTextAPIView.as_view()),

    # 🔥 ADD THIS
    path("test/", test_page),
]