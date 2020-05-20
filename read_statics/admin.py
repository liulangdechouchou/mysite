from django.contrib import admin

# Register your models here.
from .models import ReadNum, ReadDetail


@admin.register(ReadNum)
class ReadNumAdmin(admin.ModelAdmin):
    list_display = ('content_type', 'read_num', 'content_object')


@admin.register(ReadDetail)
class ReadNumAdmin(admin.ModelAdmin):
    list_display = ('date', 'read_num', 'content_object')