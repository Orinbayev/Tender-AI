from django.contrib import admin
from .models import TenderOrder


@admin.register(TenderOrder)
class TenderOrderAdmin(admin.ModelAdmin):
    list_display = ["company_name", "tender_title", "status", "created_at"]
    list_filter = ["status"]
    search_fields = ["company_name", "tender_title"]
    readonly_fields = ["generated_document", "created_at"]
