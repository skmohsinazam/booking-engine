from django.contrib import admin
from django.utils.html import format_html
from .models import Service, Booking


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'duration_minutes', 'price', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        'customer_name',
        'customer_phone',
        'service',
        'booking_date',
        'start_time',
        'status',
        'whatsapp_action',
    )
    list_filter = ('status', 'booking_date', 'service')
    search_fields = ('customer_name', 'customer_phone')

    def whatsapp_action(self, obj):
        url = obj.get_whatsapp_url()
        return format_html(
            '<a style="background:#25D366; color:#fff; font-weight:bold; padding:4px 8px; border-radius:4px; text-decoration:none;" href="{}" target="_blank">WhatsApp Confirmation</a>',
            url
        )
    whatsapp_action.short_description = "Alert Customer"