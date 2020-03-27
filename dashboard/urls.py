from django.urls import path
from dashboard.views import (
    index, client
)

app_name = "dashboard"
urlpatterns = [
    path("", index, name="index"),
    path("client/", client, name="default-client"),
    path("client/<slug:clientslug>/", client, name="client"),
]