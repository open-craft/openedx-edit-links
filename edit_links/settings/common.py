"""
Common Settings for the edit_links plugin
"""


def plugin_settings(settings):
    """
    Settings specific to the edit_links plugin
    """
    # Mapping between a Course ID and a URL to the git repo/branch/path where the course content is stored.
    settings.EDIT_LINKS_PLUGIN_GIT_REPOS = {}

    # Configurable string to use as the <label> part of the "Edit on <label>" link. Default is "Git".
    settings.EDIT_LINKS_PLUGIN_GIT_EDIT_LABEL = "Git"
