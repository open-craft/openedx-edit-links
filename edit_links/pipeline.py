"""
Module contains the openedx_filters pipeline steps offered by the extension.
"""
from urllib.parse import urlparse

from openedx_filters import PipelineStep

from edit_links.models import EditLinkedCourse


class AddEditLink(PipelineStep):
    """
    Adds an "Edit" link pointing the Github/Gitlab editing interface
    to the XBlock's HTML output.

    Example Usage:

    Add the following configurations to you configuration file

        "OPEN_EDX_FILTERS_CONFIG": {
            "org.openedx.learning.xblock.render.started.v1": {
                "fail_silently": false,
                "pipeline": [
                    "edit_links.pipeline.AddEditLink"
                ]
            }
        }
    """
    def get_repo_host(self, link):
        """
        Parses the provided link and returns the public repositor hosting service name.
        Eg., Github, Gitlab

        Arguments:
            link (str): URL of the repository
        
        Returns:
            name of the public repository hosting service or the domain name as string
        """
        o = urlparse(link)
        if "github" in o.hostname:
            return "Github"
        if "gitlab" in o.hostname:
            return "Gitlab"
        # let's just return the hostname in case if it not Gitlab or Github
        return o.hostname

    def run_filter(self, block, context, template_name):  # pylint: disable=arguments-differ
        block_id = next((child.block_id for child in block.children), "")
        if block_id:
            course_id = context["course"].id
            config = EditLinkedCourse.objects.get(course_id=course_id)
            if config:
                repo_host = self.get_repo_host(config.repository_url)
                edit_link = f"""<div class="edit-link" style="position:absolute;top:0;right:1rem;">
                <a href="{config.edit_tool_base_url}/{block_id}.html" target="_blank">
                    <i class="fa fa-pencil"></i>
                    Edit on {repo_host}
                </a>
                </div>
                """
                context["fragment"].add_content(edit_link)
        return {"context": context, "template_name": template_name}