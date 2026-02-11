from django.contrib import admin
from .models import InverterData


@admin.register(InverterData)
class InverterDataAdmin(admin.ModelAdmin):
    list_display = (
        'timestamp',
        'current_power_display',
        'daily_yield_display',
        'monthly_yield',
        'total_yield',
        'daily_earnings',
        'co2_saved'
    )

    ordering = ('-timestamp',)
    list_filter = ('timestamp',)
    readonly_fields = ('timestamp',)

    def current_power_display(self, obj):
        return f"{obj.current_power} kW"

    current_power_display.short_description = "Power (kW)"

    def daily_yield_display(self, obj):
        return f"{obj.daily_yield} kWh"

    daily_yield_display.short_description = "Daily Yield"