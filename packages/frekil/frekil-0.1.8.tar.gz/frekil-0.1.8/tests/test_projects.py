"""
Tests for the Projects API
"""
import unittest
from unittest import mock

from frekil import FrekilClient


class TestProjectsAPI(unittest.TestCase):
    """Tests for the ProjectsAPI class"""

    def setUp(self):
        """Set up a client instance for each test"""
        self.api_key = "test-api-key"
        self.client = FrekilClient(api_key=self.api_key)
        self.projects_api = self.client.projects

    @mock.patch("frekil.client.FrekilClient.get")
    def test_list(self, mock_get):
        """Test listing projects"""
        # Mock response
        mock_projects = [
            {
                "id": "project-id-1",
                "name": "Project 1",
                "description": "Project 1 description",
                "role": "annotator",
                "created_at": "2025-01-01T00:00:00Z",
                "updated_at": "2025-01-02T00:00:00Z",
                "is_ct_scan": False,
                "tags": ["tag1", "tag2"],
            }
        ]
        mock_get.return_value = mock_projects

        # Call the method
        result = self.projects_api.list()

        # Verify
        mock_get.assert_called_once_with("projects/")
        self.assertEqual(result, mock_projects)

    @mock.patch("frekil.client.FrekilClient.get")
    def test_get_membership(self, mock_get):
        """Test getting project membership"""
        # Mock response
        mock_memberships = [
            {
                "user_id": "user-id-1",
                "email": "user1@example.com",
                "name": "User 1",
                "role": "annotator",
                "percentage": 50,
                "is_active": True,
                "is_project_admin": False,
                "created_at": "2025-01-01T00:00:00Z",
                "updated_at": "2025-01-02T00:00:00Z",
            }
        ]
        mock_get.return_value = mock_memberships

        # Call the method
        project_id = "project-id-1"
        result = self.projects_api.get_membership(project_id)

        # Verify
        mock_get.assert_called_once_with(f"projects/{project_id}/membership/")
        self.assertEqual(result, mock_memberships)

    @mock.patch("frekil.client.FrekilClient.post")
    def test_bulk_allocate_images(self, mock_post):
        """Test bulk allocating images"""
        # Mock response
        mock_result = {
            "status": "success",
            "message": "Successfully processed allocations",
            "created_count": 1,
            "updated_count": 0,
            "overridden_count": 0,
            "total_allocations": 1,
            "override_used": False,
        }
        mock_post.return_value = mock_result

        # Call the method
        project_id = "project-id-1"
        allocations = [
            {
                "image_key": "image1.jpg",
                "annotators": ["annotator1@example.com"],
                "reviewers": ["reviewer1@example.com"],
            }
        ]
        result = self.projects_api.bulk_allocate_images(
            project_id=project_id, allocations=allocations, override_existing_work=False
        )

        # Verify
        mock_post.assert_called_once_with(
            f"projects/{project_id}/bulk-allocate/",
            json={"allocations": allocations, "override_existing_work": False},
        )
        self.assertEqual(result, mock_result)


if __name__ == "__main__":
    unittest.main()
