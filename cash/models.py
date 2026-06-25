from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

from cash.constants import DECIMAL_PLACES, MAX_DIGITS, MIN_AMOUNT, NAME_MAX_LEN


class NameMixin(models.Model):
    """Миксин для модели с полем name."""
    name = models.CharField(
        verbose_name='Название',
        max_length=NAME_MAX_LEN,
        unique=True,
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Status(NameMixin):
    """Статус.""" 
    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'


class TransactionType(NameMixin):
    """Тип транзакции.""" 
    class Meta:
        verbose_name = 'Тип транзакции'
        verbose_name_plural = 'Типы транзакций'


class Category(models.Model):
    """Категория.""" 
    name = models.CharField(
        verbose_name='Название', 
        max_length=NAME_MAX_LEN,
        unique=True,
    )
    transaction_type = models.ForeignKey(
        TransactionType,
        on_delete=models.PROTECT,
        verbose_name='Тип транзакции',
        related_name='categories',
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    """Подкатегория.""" 
    name = models.CharField(
        verbose_name='Название', 
        max_length=NAME_MAX_LEN,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name='Категория',
        related_name='subcategories',
    )

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'category'], 
                name='unique_subcategory'
            )
        ]

    def __str__(self):
        return self.name


class CashFlow(models.Model):
    """Запись о движении денежных средств."""
    date = models.DateField(
        verbose_name='Дата',
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        verbose_name='Статус',
        related_name='cashflows', 
    )
    transaction_type = models.ForeignKey(
        TransactionType,
        on_delete=models.PROTECT,
        verbose_name='Тип',
        related_name='cashflows',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        verbose_name='Категория',
        related_name='cashflows',
    )
    subcategory = models.ForeignKey(
        Subcategory,
        on_delete=models.PROTECT,
        verbose_name='Подкатегория',
        related_name='cashflows',
    )
    amount = models.DecimalField(
        verbose_name='Сумма',
        max_digits=MAX_DIGITS,
        decimal_places=DECIMAL_PLACES,
        validators=[MinValueValidator(MIN_AMOUNT)],
    )
    comment = models.TextField(
        verbose_name='Комментарий',
        blank=True, 
        null=True,
    )

    class Meta:
        verbose_name = 'Запись ДДС'
        verbose_name_plural = 'Записи ДДС'
        ordering = ('-date',)

    def __str__(self):
        return f'{self.date} - {self.status} - {self.amount}'

    def clean(self):
        """проверка бизнес-правил."""
        errors = {}

        if self.category_id and self.transaction_type_id:
            if self.category.transaction_type_id != self.transaction_type_id:
                errors['category'] = 'Выбранная категория не относится к указанному типу.'
        if self.subcategory_id and self.category_id:
            if self.subcategory.category_id != self.category_id:
                errors['subcategory'] = 'Выбранная подкатегория не относится к указанной категории.'    
        if errors:
            raise ValidationError(errors)
