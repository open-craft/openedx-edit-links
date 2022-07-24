"""
Tests for pipeline.py
"""
from django.test import TestCase, override_settings
from openedx_filters.learning.filters import VerticalBlockChildRenderStarted


class HtmlBlockWithMixins:
    """
    Mock of the mixed class of xmodule.html_module.HtmlBlock to test the filter pipeline.

    Arguments:
        course_id (str): id of the course
        url_name (str): the file name to which the HTML link will be created
        data (str): the HTML content of the block
    """
    def __init__(self, course_id, url_name, data):
        self.course_id = course_id
        self.url_name = url_name
        self.data = data


@override_settings(
    OPEN_EDX_FILTERS_CONFIG={
        "org.openedx.learning.verticalblockchild.render.started.v1": {
            "fail_silently": False,
            "pipeline": [
                "edit_links.pipeline.AddEditLink"
            ]
        }
    },
    EDIT_LINKS_PLUGIN_GIT_REPOS={},
    EDIT_LINKS_PLUGIN_GIT_EDIT_LABEL="Git",
)
class TestAddEditLinkPipeline(TestCase):
    """
    Testcase for the AddEditLink openedx-filters pipeline.
    """

    def setUp(self) -> None:
        super().setUp()

        self.original_content = "<p>Test content</p>"
        self.block = HtmlBlockWithMixins(
            "course-v1:demo+course+2022", "chapter-01", self.original_content
        )

    def test_pipeline_does_nothin_when_not_configured(self):
        """
        Check that the input fragment is unchanged when there is no
        configuration for a course.
        """
        print(type(self.block).__name__)
        block, context = VerticalBlockChildRenderStarted.run_filter(
            block=self.block, context={}
        )
        self.assertEqual(block.data, self.original_content)
        self.assertEqual(context, {})

    @override_settings(
        EDIT_LINKS_PLUGIN_GIT_REPOS={
            "course-v1:demo+course+2022": "https://github.com/user/repo/folder/"
        },
        EDIT_LINKS_PLUGIN_GIT_EDIT_LABEL="Github"
    )
    def test_pipeline_adds_edit_link_when_configured(self):
        """
        Check that the edit link is added to the block data when the course is
        configured with git repo url
        """
        block, context = VerticalBlockChildRenderStarted.run_filter(
            block=self.block, context={}
        )

        self.assertIn(self.original_content, block.data)
        self.assertIn("https://github.com/user/repo/folder/html/chapter-01.html", block.data)
        self.assertIn("Edit on Github", block.data)
        self.assertEqual(context, {})
