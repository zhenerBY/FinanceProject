from django.db.models import Q, Sum
from django.http import QueryDict
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_api_key.permissions import HasAPIKey

from main.models import Category, AdvUser, Operation, ApiUser
from main.serializers import UsersSerializer, OperationsSerializer, CategoriesSerializer, ApiUsersSerializer, \
    ExtendedOperationsSerializer


class UsersViewSet(viewsets.ModelViewSet):
    queryset = AdvUser.objects.all()
    serializer_class = UsersSerializer
    permission_classes = [IsAdminUser]

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

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_superuser:
            queryset = queryset.filter(id=self.request.user.id)
        return queryset

    @action(methods=['POST'], detail=False, url_path="register")
    def register(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        email = request.data.get('email')
        u = AdvUser(username=username)
        u.set_password(password)
        if first_name is not None:
            u.first_name = first_name
        if last_name is not None:
            u.last_name = last_name
        if email is not None:
            u.email = email
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
    permission_classes = [HasAPIKey]

    # Времмено оставил, как функционал для авторизованных юзеров
    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     if not self.request.user.is_superuser:
    #         queryset = queryset.filter(user_id=self.request.user.id)
    #     return queryset
    #
    # def perform_create(self, serializer):
    #     if self.request.user.is_superuser:
    #         serializer.save()
    #     # пользователь может создать операции только под своим юзером.
    #     elif self.request.user.is_authenticated:
    #         return serializer.save(user=self.request.user)
    #     else:
    #         serializer.save()

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_active=True)
        if self.request.method in ('GET', 'DELETE', 'PUT', 'PATH'):
            try:
                queryset = queryset.filter(user__chat_id=self.request.data['chat_id'])
            except KeyError:
                queryset = queryset
            try:
                queryset = queryset.filter(category=self.request.data['category'])
            except KeyError:
                queryset = queryset
        return queryset

    # отлавливаем и переопледеляем request.data, если есть в запросе 'chat_id'
    def get_serializer(self, *args, **kwargs):
        if self.request.data.get("chat_id") is not None:
            user = ApiUser.objects.get(chat_id=self.request.data['chat_id']).pk
            self.request.data['user'] = user
        return super().get_serializer(*args, **kwargs)

    # shows the user's income and expenses (2 numbers)
    @action(methods=['GET'], detail=False, url_path="balance")
    def balance(self, request):
        chat_id = request.data.get('chat_id')
        u = ApiUser.objects.get(chat_id=chat_id)
        q_inc = Q(user_id=u.pk) & Q(category__cat_type='INC') & Q(is_active=True)
        q_exp = Q(user_id=u.pk) & Q(category__cat_type='EXP') & Q(is_active=True)
        inc = Operation.objects.aggregate(inc=Sum('amount', filter=q_inc))
        exp = Operation.objects.aggregate(exp=Sum('amount', filter=q_exp))
        res_data = {
            "user": ApiUsersSerializer(u).data,
            "balance": {
                **inc,
                **exp,
            }
        }
        return Response(res_data, status=status.HTTP_200_OK)

    # show user's category balance
    @action(methods=['GET'], detail=False, url_path="cat_balance")
    def cat_balance(self, request):
        chat_id = request.data.get('chat_id')
        u = ApiUser.objects.get(chat_id=chat_id)
        cat_type = request.data.get('cat_type')
        q = Q(user_id=u.pk) & Q(category__cat_type=cat_type) & Q(is_active=True)
        categories = {}
        for operation in Operation.objects.filter(q):
            if operation.category.name in categories.keys():
                categories[operation.category.name] += operation.amount
            else:
                categories[operation.category.name] = operation.amount
        res_data = {
            "user": ApiUsersSerializer(u).data,
            "categories": categories
        }
        return Response(res_data, status=status.HTTP_200_OK)


# уже не надо
# переопределяем, чтобы создавалась запись по chat_id, а не ApiUser.id.
# При этом сохранена возможность использовать ApiUser.id, если не указан chat_id
# def create(self, request, *args, **kwargs):
#     print(request.data)
#     print(type(request.data))
#     # import pdb
#     # pdb.set_trace()
#     # if isinstance(request.data, QueryDict):
#     #     try:
#     #         chat_id=self.request.data['chat_id']
#     #     except KeyError:
#     #         pass
#     # try:
#     #     chat_id=self.request.data['chat_id']
#     # except KeyError:
#     #     pass
#     try:
#         print('change', request.data)
#         request.data['user'] = ApiUser.objects.get(chat_id=self.request.data['chat_id']).pk
#     except KeyError:
#         pass
#     print(request.data)
#     serializer = self.get_serializer(data=request.data)
#     serializer.is_valid(raise_exception=True)
#     self.perform_create(serializer)
#     headers = self.get_success_headers(serializer.data)
#     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


# после переопределения create - не нужно. Пока не удаляю.
# def perform_create(self, serializer):
#     # пользователь может создать операции только под своим юзером.
#     # Только для создания(POST). ПРи необходимости можно и другие методы сделать.
#     try:
#         print('userPK', type(ApiUser.objects.get(chat_id=self.request.data['chat_id']).pk))
#         serializer.save(user=ApiUser.objects.get(chat_id=self.request.data['chat_id']))
#     except KeyError:
#         serializer.save()


class ExtendedOperationsViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Operation.objects.all()
    serializer_class = ExtendedOperationsSerializer
    permission_classes = [HasAPIKey]

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_active=True)
        if self.request.method in ('GET'):
            try:
                queryset = queryset.filter(user__chat_id=self.request.data['chat_id'])
            except KeyError:
                queryset = queryset
        return queryset

    # отлавливаем и переопледеляем request.data, если есть в запросе 'chat_id'
    def get_serializer(self, *args, **kwargs):
        if self.request.data.get("chat_id") is not None:
            user = ApiUser.objects.get(chat_id=self.request.data['chat_id']).pk
            self.request.data['user'] = user
        return super().get_serializer(*args, **kwargs)


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = [HasAPIKey]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.method in ('GET'):
            try:
                # queryset = queryset.filter(operations__user__chat_id=self.request.data['chat_id'])
                queryset = queryset.filter(operations__user__chat_id=self.request.data['chat_id']).distinct()
            except KeyError:
                queryset = queryset
        return queryset


class ApiUsersViewSet(viewsets.ModelViewSet):
    queryset = ApiUser.objects.all()
    serializer_class = ApiUsersSerializer
    permission_classes = [HasAPIKey]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.method in ('GET', 'DELETE', 'PUT', 'PATH'):
            try:
                queryset = queryset.filter(chat_id=self.request.data['chat_id'])
            except KeyError:
                queryset = queryset
        return queryset
