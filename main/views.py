from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from main.models import Categories, AdvUser, Operations
from main.serializers import UsersSerializer

class UsersViewSet(viewsets.ModelViewSet):
    queryset = AdvUser.objects.all()
    serializer_class = UsersSerializer

    @action(methods=['POST'], detail=False, url_path="registers")
    def register(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        email = request.data.get('email')
        u = AdvUser(username=username, email=email)
        u.set_password(password)
        if first_name is not None:
            u.first_name = first_name
        if last_name is not None:
            u.last_name = last_name
        u.save()
        res_data = {
            "user": UsersSerializer(u).data,
            # "token": {
            #     'refresh': str(refresh),
            #     'access': str(refresh.access_token),
            # }
        }
        return Response(res_data, status=status.HTTP_201_CREATED)