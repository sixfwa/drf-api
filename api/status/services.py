import dataclasses
import datetime
from typing import TYPE_CHECKING

from django.shortcuts import get_object_or_404
from rest_framework import exceptions

from user import services as user_service
from . import models as status_models

if TYPE_CHECKING:
    from models import Status
    from user.models import User


@dataclasses.dataclass
class StatusDataClass:
    content: str
    date_published: datetime.datetime = None
    user: user_service.UserDataClass = None
    id: int = None

    @classmethod
    def from_instance(cls, status_model: "Status") -> "StatusDataClass":
        return cls(
            content=status_model.content,
            date_published=status_model.date_published,
            id=status_model.id,
            user=status_model.user,
        )


def create_status(user, status: "StatusDataClass") -> "StatusDataClass":
    status_create = status_models.Status.objects.create(
        content=status.content, user=user
    )
    return StatusDataClass.from_instance(status_model=status_create)


def get_user_status(user: "User") -> list["StatusDataClass"]:
    user_status = status_models.Status.objects.filter(user=user)

    return [
        StatusDataClass.from_instance(single_status) for single_status in user_status
    ]


def get_user_status_detail(status_id: int) -> "StatusDataClass":
    status = get_object_or_404(status_models.Status, pk=status_id)

    return StatusDataClass.from_instance(status_model=status)


def delete_user_status(user: "User", status_id: int) -> "StatusDataClass":
    status = get_object_or_404(status_models.Status, pk=status_id)
    if user.id != status.user.id:
        raise exceptions.PermissionDenied("You're not the user fool")
    status.delete()


def update_user_status(user: "User", status_id: int, status_data: "StatusDataClass"):
    status = get_object_or_404(status_models.Status, pk=status_id)
    if user.id != status.user.id:
        raise exceptions.PermissionDenied("You're not the user fool")

    status.content = status_data.content
    status.save()

    return StatusDataClass.from_instance(status_model=status)
