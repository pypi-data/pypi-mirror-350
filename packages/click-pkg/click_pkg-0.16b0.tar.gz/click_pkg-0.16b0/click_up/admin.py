from django.contrib import admin
from django.conf import settings

from click_up.models import ClickTransaction


class ClickTransactionAdmin(admin.ModelAdmin):
    """
    Admin Model for ClickTransaction
    """
    list_display = (
        'id',
        'state',
        'transaction_id',
        'account_id',
        'amount',
        'created_at',
        'updated_at',
    )
    search_fields = ('transaction_id', 'account_id')
    list_filter = ('state', 'created_at')
    ordering = ('-created_at',)


if not getattr(settings, 'CLICK_DISABLE_ADMIN', False):
    admin.site.register(ClickTransaction, ClickTransactionAdmin)
