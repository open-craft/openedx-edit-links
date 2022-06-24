"""
edit_links Django application initialization.
"""

from django.apps import AppConfig


class EditLinksConfig(AppConfig):
    """
    Configuration for the edit_links Django application.
    """

    name = 'edit_links'

    plugin_app = {
        'settings_config': {
            'lms.djangoapp': {
                'production': {'relative_path': 'settings.production'},
                'common': {'relative_path': 'settings.common'},
            }
        }
    }
