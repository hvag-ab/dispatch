from django.urls import path

from .views import TestCelery,Te

app_name = "orders"

urlpatterns = [
    path("test", TestCelery.as_view(), name="test"),
    path("te", Te.as_view(), name="test2"),
]
