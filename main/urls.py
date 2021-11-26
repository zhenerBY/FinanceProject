from django.urls import path, include

from rest_framework.routers import SimpleRouter

from main.views import UsersViewSet


router = SimpleRouter()
router.register('users', UsersViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls))
]