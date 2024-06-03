from django.contrib import admin
from .models import *
# Register your models here.
class WorkspaceAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'owner', 'created_at', 'updated_at')
    list_filter = ('owner', 'created_at', 'updated_at')
    search_fields = ('name', 'owner__username')

admin.site.register(Workspace, WorkspaceAdmin)