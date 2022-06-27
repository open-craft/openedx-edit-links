"""
Database models for edit_links.
"""
from django.db import models
from model_utils.models import TimeStampedModel


class EditLinkedCourse(TimeStampedModel):
    """
    Model to store courses and related information to generate the edit links.

    .. no_pii:
    """

    course_id = models.CharField(max_length=255)
    repository_url = models.URLField(max_length=255)
    edit_tool_base_url = models.URLField(max_length=255)

    def __str__(self):
        """
        Get a string representation of this model instance.
        """
        return '<EditLinkedCourse, ID: {} for course: {}>'.format(self.id, self.course_id)
