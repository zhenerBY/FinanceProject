from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, IsAuthenticated
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken

from main.models import Category, AdvUser, Operation
from main.serializers import UsersSerializer, OperationsSerializer, CategoriesSerializer


class UsersViewSet(viewsets.ModelViewSet):

    queryset = AdvUser.objects.all()
    serializer_class = UsersSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]
    # permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAuthenticatedOrReadOnly]
        elif self.action == 'create':
            permission_classes = [IsAuthenticatedOrReadOnly]
        elif self.action == 'register':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticatedOrReadOnly]
        return [permission() for permission in permission_classes]

    @action(methods=['POST'], detail=False, url_path="register")
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
        refresh = RefreshToken.for_user(u)
        res_data = {
            "user": UsersSerializer(u).data,
            "token": {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }
        return Response(res_data, status=status.HTTP_201_CREATED)


class OperationsViewSet(viewsets.ModelViewSet):
    queryset = Operation.objects.all()
    serializer_class = OperationsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_superuser:
            queryset = queryset.filter(user_id=self.request.user.id)
        return queryset


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    # permission_classes = [IsAuthenticated]