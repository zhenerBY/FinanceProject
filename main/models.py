from django.core import validators
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class AdvUser(AbstractUser):
    is_activated = models.BooleanField(default=True,
                                       db_index=True,
                                       verbose_name='Прошел активацию?')

    class Meta(AbstractUser.Meta):
        pass


class Categories(models.Model):
    class CatType(models.TextChoices):
        EXPENSE = 'EXP', _('Expense')
        INCOME = 'INC', _('Income')

    name = models.CharField(max_length=50,
                            db_index=True,
                            unique=True,
                            verbose_name='Нименование категории')
    cat_type = models.CharField(max_length=3, choices=CatType.choices, default=CatType.EXPENSE)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Создано')

    def __str__(self):
        return f'Category - {self.name} : {self.cat_type}'

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Operations(models.Model):
    title = models.CharField(max_length=50, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    amount = models.FloatField(default=0, verbose_name='Величина',
                               validators=[validators.MinValueValidator(0,
                                                                        message='Значение меньше нуля')])
    # Проверка на только положительные значания
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Создано')
    user = models.ForeignKey(AdvUser, on_delete=models.CASCADE,
                             verbose_name='Пользователь', related_name='operations')
    category = models.ForeignKey(Categories, on_delete=models.PROTECT,
                                 verbose_name='Категория', related_name='operations')

    def __str__(self):
        return f"Operation - {self.title} {self.amount}"

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Операция'
        verbose_name_plural = 'Операции'

    pass
