"""
Module defining the admin views.
"""
from django.contrib import admin

from .models import EditLinkedCourse


class EditLinkedCourseAdmin(admin.ModelAdmin):
    pass


admin.site.register(EditLinkedCourse, EditLinkedCourseAdmin)
