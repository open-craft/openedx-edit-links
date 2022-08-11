"""
Module contains the openedx_filters pipeline steps offered by the extension.
"""
from urllib.parse import urljoin

from django.conf import settings
from django.utils.translation import gettext as _
from openedx_filters import PipelineStep


class AddEditLink(PipelineStep):
    """
    Adds an "Edit" link pointing the Github/Gitlab editing interface to the XBlock's HTML output.

    Example Usage:

    Add the following configurations to you configuration file

    .. code-block::

        "OPEN_EDX_FILTERS_CONFIG": {
            "org.openedx.learning.verticalblockchild.render.started.v1": {
                "fail_silently": false,
                "pipeline": [
                    "edit_links.pipeline.AddEditLink"
                ]
            }
        }

    """

    def run_filter(self, block, context):  # pylint: disable=arguments-differ
        """
        Add an Edit link to the block data if the block is a HtmlBlock.
        """
        course_id = str(block.course_id)
        git_url = settings.EDIT_LINKS_PLUGIN_GIT_REPOS.get(course_id, None)

        if type(block).__name__ == "HtmlBlockWithMixins" and git_url and not context.get("is_mobile_app", False):
            label = _("Edit on %(site)s") % {"site": settings.EDIT_LINKS_PLUGIN_GIT_EDIT_LABEL}
            link = urljoin(git_url, f"html/{block.url_name}.html")

            def wrapper(fn):
                def wrapped():
                    return (
                        '<div class="edit-link-wrapper">'
                        '<div class="edit-link">'
                        f'<p style="text-align: right;"><a href="{link}" target="_blank">'
                        f'<i class="fa fa-pencil mr-1"></i> {label}</a></p>'
                        '</div>'
                        f'<div class="edit-link-original-content">{fn()}</div>'
                        '</div>'
                    )
                return wrapped
            block.get_html = wrapper(block.get_html)

        return {"block": block, "context": context}
