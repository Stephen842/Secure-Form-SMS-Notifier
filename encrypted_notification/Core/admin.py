from django.contrib import admin
from django.db.models import Q
from .models import Health, Reply

# Register your models here.
class HealthAdmin(admin.ModelAdmin):
    list_display = ('name', 'submitted_at')
    search_fields = ('name',)

    pass

class ReplyAdmin(admin.ModelAdmin):
    list_display = ('message',)

    pass

admin.site.register(Health, HealthAdmin)
admin.site.register(Reply, ReplyAdmin)