from django.urls import path

from .views import TestCelery

app_name = "orders"

urlpatterns = [
    path("test", TestCelery.as_view(), name="test"),
]
