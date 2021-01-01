from django.urls import path, include


urlpatterns = [
    path("test/", include("orders.urls")),
    path("pt/", include("periodtask.urls")),
]
