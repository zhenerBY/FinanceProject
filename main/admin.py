from django.contrib import admin

from .models import AdvUser, Categories, Operations

# class BbAdmin(admin.ModelAdmin) :
#     list_display = (’title’, ’content’, ’price’, ’published’)
#     list_display_links = (’title’, ’content’)
#     search_fields = (’title’, ’content’, )
# # admin.site.register(Bb, BbAdmin)

class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'expense', 'income', 'created_at')
    list_display_links = ('name',)
    search_fields = ('name',)
    ordering = ('name',)
    # radio_fields = {'operation': admin.VERTICAL}

    # name = models.CharField(max_length=50,
    #                         db_index=True,
    #                         unique=True,
    #                         verbose_name='Нименование категории')
    # expense = models.BooleanField(default=None, null=True, blank=True, db_index=True, verbose_name='Расход?')
    # income = models.BooleanField(default=None, null=True, blank=True, db_index=True, verbose_name='Доход?')
    # created_at


admin.site.register(AdvUser)
admin.site.register(Categories, CategoriesAdmin)
admin.site.register(Operations)
