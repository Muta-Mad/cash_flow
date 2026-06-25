from django.contrib import admin
from cash.models import Status, TransactionType, Category, Subcategory, CashFlow


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(TransactionType)
class TransactionTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'transaction_type')


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category')


@admin.register(CashFlow)
class CashFlowAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'date', 'status', 'transaction_type', 
        'category', 'subcategory', 'amount', 'comment_preview',
    )
    list_filter = ('date', 'status', 'transaction_type', 'category', 'subcategory')
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('status', 'transaction_type', 'category', 'subcategory')

    def comment_preview(self, obj):
        if not obj.comment:
            return '-'
        if len(obj.comment) > 50:
            return obj.comment[:50] + '...'
        return obj.comment
    comment_preview.short_description = 'Комментарий'
