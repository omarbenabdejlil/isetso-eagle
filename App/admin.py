from django.contrib import admin
from .models import Machine

# Register your models here.
class MachineAdmin(admin.ModelAdmin):
    list_display = ['hostName', 'hostOs', 'ip', 'interface', 'date_posted']
    ordering = ['-date_posted']
    search_fields = ('date_posted', 'hostName', 'hostOs', 'ip', 'interface')

admin.site.register(Machine, MachineAdmin)