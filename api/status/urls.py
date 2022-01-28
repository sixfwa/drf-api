from django.urls import path

from . import apis

urlpatterns = [
    path("status/", apis.StatusCreateListApi.as_view(), name="status"),
    path(
        "status/<int:status_id>/",
        apis.StatusRetrieveUpdateDelete.as_view(),
        name="status_detail",
    ),
]
