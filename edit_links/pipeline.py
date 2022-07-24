"""
Module contains the openedx_filters pipeline steps offered by the extension.
"""
from urllib.parse import urljoin, urlparse

from django.conf import settings
from django.utils.translation import gettext as _

from openedx_filters import PipelineStep


class AddEditLink(PipelineStep):
    """
    Adds an "Edit" link pointing the Github/Gitlab editing interface to the XBlock's HTML output.

    Example Usage:

    Add the following configurations to you configuration file

        "OPEN_EDX_FILTERS_CONFIG": {
            "org.openedx.learning.verticalblockchild.render.started.v1": {
                "fail_silently": false,
                "pipeline": [
                    "edit_links.pipeline.AddEditLink"
                ]
            }

    """

    def run_filter(self, block, context):  # pylint: disable=arguments-differ
        """
        Executes the filter which checks if the block is a html block and then wraps the content
        in a div containing the Edit link.
        """
        course_id = str(block.course_id)
        git_url = settings.EDIT_LINKS_PLUGIN_GIT_REPOS.get(course_id, None)

        if type(block).__name__ == "HtmlBlockWithMixins" and git_url and not context.get("is_mobile_app", False):
            label = _("Edit on %(site)s") % {"site": settings.EDIT_LINKS_PLUGIN_GIT_EDIT_LABEL}
            link = urljoin(git_url, f"html/{block.url_name}.html")

            wrapped = f"""
<div class="edit-link-wrapper">
    <div class="edit-link">
        <p style="text-align: right;"><a href="{link}" target="_blank"><i class="fa fa-pencil"></i> {label}</a></p>
    </div>
    <div class="edit-link-original-content">
    {block.data}
    </div>
</div>
"""
            block.data = wrapped
            # Let's not mark this change as dirty as that would save the edit link permanently
            # This needed because the XBlock render() function has the sideeffect of saving all
            # the dirty fields.
            #
            # Ref: https://github.com/openedx/XBlock/blob/d6932fa6203ecf5938b18a880f7f546cb37f5d63/xblock/runtime.py#L849-L850
            block._clear_dirty_fields()  # pylint: disable=protected-access

        return {"block": block, "context": context}
