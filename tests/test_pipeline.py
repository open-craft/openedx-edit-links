"""
Tests for pipeline.py
"""
from unittest.mock import Mock

from django.test import TestCase, override_settings
from openedx_filters.learning.filters import XBlockRenderStarted  # pylint: disable=no-name-in-module

from edit_links.models import EditLinkedCourse
from edit_links.pipeline import AddEditLink


@override_settings(
    OPEN_EDX_FILTERS_CONFIG={
        "org.openedx.learning.xblock.render.started.v1": {
            "fail_silently": False,
            "pipeline": [
                "edit_links.pipeline.AddEditLink"
            ]
        }
    }
)
class TestAddEditLinkPipeline(TestCase):
    """
    Testcase for the AddEditLink openedx-filters pipeline.
    """

    def setUp(self) -> None:
        super().setUp()

        self.course_id = "test-course-id"
        self.course = Mock()
        self.course.id = self.course_id

        class MockBlock:
            def __init__(self):
                self.block_id = "my-block-id"

        self.block = Mock()
        self.block.children = [MockBlock()]

        self.fragment = Mock()
        self.context = {
            "fragment": self.fragment,
            "course": self.course,
        }

    def test_pipeline_does_nothin_when_not_configured(self):
        """
        Check that the input fragment is unchanged when there is no
        configuration for a course.
        """
        _ = XBlockRenderStarted.run_filter(
            block=self.block, context=self.context, template_name="template.html"
        )
        self.fragment.add_content.assert_not_called()

    def test_pipeline_adds_edit_link_when_configured(self):
        """
        Check that an Edit link is appended to the fragment when a course is
        configured with EditLinkedCourse.
        """
        config = EditLinkedCourse(
            course_id=self.course_id,
            repository_url="https://gitlab.com/my/repo",
            edit_tool_base_url="https://edit.tool/-/"
        )
        config.save()
        _ = XBlockRenderStarted.run_filter(
            block=self.block, context=self.context, template_name="template.html"
        )
        self.fragment.add_content.assert_called_once()
        link = "https://edit.tool/-/my-block-id.html"
        self.assertIn(link, self.fragment.add_content.call_args[0][0])

    def test_get_repo_host_identifies_correct_services(self):
        """
        Check that the get_repo_host utility function identifies known services and
        returns url hostname for unknown ones
        """
        step = AddEditLink("filter-type", [])
        self.assertEqual(step.get_repo_host("https://gitlab.com/hello"), "Gitlab")
        self.assertEqual(step.get_repo_host("https://github.com/hello"), "Github")
        self.assertEqual(step.get_repo_host("https://my.custom-repo-host.com/hello"), "my.custom-repo-host.com")
