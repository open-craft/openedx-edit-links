"""
Production settings for edit_links plugin
"""


def plugin_settings(settings):
    """
    Modify the plugin's settings by fetching the environment values
    """
    settings.EDIT_LINKS_PLUGIN_GIT_REPOS = settings.ENV_TOKENS.get(
        'EDIT_LINKS_PLUGIN_GIT_REPOS', settings.EDIT_LINKS_PLUGIN_GIT_REPOS
    )
    settings.EDIT_LINKS_PLUGIN_GIT_EDIT_LABEL = settings.ENV_TOKENS.get(
        'EDIT_LINKS_PLUGIN_GIT_EDIT_LABEL', settings.EDIT_LINKS_PLUGIN_GIT_EDIT_LABEL
    )
