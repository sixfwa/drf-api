from rest_framework import views
from rest_framework import permissions
from rest_framework import response
from rest_framework import status as rest_status

from user import authentication
from . import serializer as status_serializer
from . import services


class StatusCreateListApi(views.APIView):
    authentication_classes = (authentication.CustomUserAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = status_serializer.StatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        serializer.instance = services.create_status(user=request.user, status=data)

        return response.Response(data=serializer.data)

    def get(self, request):
        status_collection = services.get_user_status(user=request.user)
        serializer = status_serializer.StatusSerializer(status_collection, many=True)
        return response.Response(data=serializer.data)


class StatusRetrieveUpdateDelete(views.APIView):
    authentication_classes = (authentication.CustomUserAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, status_id):
        status = services.get_user_status_detail(status_id=status_id)
        serializer = status_serializer.StatusSerializer(status)
        return response.Response(data=serializer.data)

    def delete(self, request, status_id):
        services.delete_user_status(user=request.user, status_id=status_id)
        return response.Response(status=rest_status.HTTP_204_NO_CONTENT)

    def put(self, request, status_id):
        serializer = status_serializer.StatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        status = serializer.validated_data
        serializer.instance = services.update_user_status(
            user=request.user, status_id=status_id, status_data=status
        )

        return response.Response(data=serializer.data)
