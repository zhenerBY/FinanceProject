from django.contrib import admin

from .models import AdvUser, Categories, Operations


class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'expense', 'income', 'created_at')
    list_display_links = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


class AdvUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'is_superuser', 'is_active')
    list_display_links = ('username', 'first_name', 'last_name',)
    search_fields = ('username', 'first_name', 'last_name', 'email',)
    ordering = ('username',)


class OperationsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'amount', 'user', 'category',)
    list_display_links = ('title', 'user',)
    search_fields = ('title', 'description',)
    ordering = ('-created_at',)


admin.site.register(AdvUser, AdvUserAdmin)
admin.site.register(Categories, CategoriesAdmin)
admin.site.register(Operations, OperationsAdmin)
