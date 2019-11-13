from django.contrib import admin
from .models import Incident, Message
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User



# Register your models here.

@admin.register(Incident)
class IncidentAdmin(admin.ModelAdmin):
    list_display = ('store', 'created', 'problem', 'incident', 'date_solved', 'current_status', 'criticality')
    list_filter = ('store', 'created', 'problem', 'date_solved', 'criticality')
    search_fields = ('store', 'created', 'problem', 'incident', 'date_solved', 'criticality')
    date_hierarchy = 'created'
    ordering = ('store',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('store', 'body')
    list_filter = ('store',)
    search_fields = ('store',)
    ordering = ('store',)



UserAdmin.list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'last_login', 'is_staff')

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.site_header = "Администрирование сайта директора магазина X5"
admin.site.site_title = "Администрирование сайта директора магазина X5"
admin.site.index_title = "Администрирование сайта директора магазина X5"