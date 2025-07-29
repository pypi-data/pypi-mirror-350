"""
Tests for the Projects API
"""
import unittest
from unittest import mock

from frekil import FrekilClient
from frekil.exceptions import FrekilClientError


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

    @mock.patch("frekil.client.FrekilClient.get")
    def test_get_images(self, mock_get):
        """Test getting project images"""
        # Mock response
        mock_images = [
            {
                "id": "images/image1.dcm",
                "filename": "image1.dcm",
                "created_at": "2025-01-01T00:00:00Z",
                "updated_at": "2025-01-02T00:00:00Z",
            }
        ]
        mock_get.return_value = mock_images

        # Call the method
        project_id = "project-id-1"
        result = self.projects_api.get_images(project_id)

        # Verify
        mock_get.assert_called_once_with(f"projects/{project_id}/images/")
        self.assertEqual(result, mock_images)

    @mock.patch("frekil.client.FrekilClient.get")
    def test_get_allocations(self, mock_get):
        """Test getting project allocations"""
        # Mock response
        mock_allocations = [
            {
                "allocation_id": "alloc-id-1",
                "image_id": "images/image1.dcm",
                "image_filename": "image1.dcm",
                "annotator_email": "annotator1@example.com",
                "reviewer_email": "reviewer1@example.com",
                "status": "PENDING",
                "created_at": "2025-01-01T00:00:00Z",
                "is_ground_truth": False,
            }
        ]
        mock_get.return_value = mock_allocations

        # Call the method
        project_id = "project-id-1"
        result = self.projects_api.get_allocations(project_id)

        # Verify
        mock_get.assert_called_once_with(f"projects/{project_id}/allocations/")
        self.assertEqual(result, mock_allocations)

    @mock.patch("frekil.client.FrekilClient.post")
    def test_bulk_allocate_images_success(self, mock_post):
        """Test successful bulk allocation of images"""
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
                "image_key": "images/image1.dcm",
                "annotators": ["annotator1@example.com"],
                "reviewers": ["reviewer1@example.com"],
            }
        ]
        result = self.projects_api.bulk_allocate_images(
            project_id=project_id,
            allocations=allocations,
            override_existing_work=False,
        )

        # Verify
        mock_post.assert_called_once_with(
            f"projects/{project_id}/bulk-allocate/",
            json={"allocations": allocations, "override_existing_work": False},
        )
        self.assertEqual(result, mock_result)

    @mock.patch("frekil.client.FrekilClient.post")
    def test_bulk_allocate_images_validation_error(self, mock_post):
        """Test bulk allocation with validation errors"""
        # Mock response for validation error
        mock_error_response = mock.Mock()
        mock_error_response.status_code = 400
        mock_error_response.json.return_value = {
            "status": "validation_failed",
            "message": "Validation failed",
            "errors": ["Invalid user email"],
            "invalid_users": [
                {
                    "email": "invalid@example.com",
                    "role": "annotator",
                    "reason": "User does not exist",
                    "allocation_index": 0,
                    "image_key": "images/image1.dcm",
                }
            ],
            "existing_work": [],
            "instructions": {
                "invalid_users": "Please ensure all users exist and have correct roles",
            },
            "override_available": False,
        }

        mock_post.side_effect = FrekilClientError(
            "Client error: Validation failed", response=mock_error_response
        )

        # Call the method and expect exception
        project_id = "project-id-1"
        allocations = [
            {
                "image_key": "images/image1.dcm",
                "annotators": ["invalid@example.com"],
                "reviewers": ["reviewer1@example.com"],
            }
        ]

        with self.assertRaises(FrekilClientError) as context:
            self.projects_api.bulk_allocate_images(
                project_id=project_id,
                allocations=allocations,
                override_existing_work=False,
            )

        # Verify error details
        error = context.exception
        self.assertEqual(error.status_code, 400)
        self.assertEqual(error.error_details["status"], "validation_failed")
        self.assertIn("invalid_users", error.error_details)

    @mock.patch("frekil.client.FrekilClient.post")
    def test_bulk_allocate_images_existing_work(self, mock_post):
        """Test bulk allocation with existing work"""
        # Mock response for existing work error
        mock_error_response = mock.Mock()
        mock_error_response.status_code = 400
        mock_error_response.json.return_value = {
            "status": "validation_failed",
            "message": "Existing work found",
            "errors": ["Cannot modify allocations with existing work"],
            "invalid_users": [],
            "existing_work": [
                {
                    "image_key": "images/image1.dcm",
                    "annotator": "annotator1@example.com",
                    "reviewer": "reviewer1@example.com",
                    "allocation_index": 0,
                    "existing_work": [
                        {
                            "type": "annotation",
                            "user": "annotator1@example.com",
                            "created_at": "2025-01-01T00:00:00Z",
                            "status": "completed",
                        }
                    ],
                    "message": "Annotation exists for this image",
                    "can_override": True,
                }
            ],
            "instructions": {
                "existing_work": "Use override_existing_work=True to override",
            },
            "override_available": True,
            "override_instructions": "Set override_existing_work=True to override existing work",
        }

        mock_post.side_effect = FrekilClientError(
            "Client error: Existing work found", response=mock_error_response
        )

        # Call the method and expect exception
        project_id = "project-id-1"
        allocations = [
            {
                "image_key": "images/image1.dcm",
                "annotators": ["annotator2@example.com"],  # Different annotator
                "reviewers": ["reviewer1@example.com"],
            }
        ]

        with self.assertRaises(FrekilClientError) as context:
            self.projects_api.bulk_allocate_images(
                project_id=project_id,
                allocations=allocations,
                override_existing_work=False,
            )

        # Verify error details
        error = context.exception
        self.assertEqual(error.status_code, 400)
        self.assertEqual(error.error_details["status"], "validation_failed")
        self.assertIn("existing_work", error.error_details)
        self.assertTrue(error.error_details["override_available"])

    @mock.patch("frekil.client.FrekilClient.post")
    def test_bulk_allocate_images_with_override(self, mock_post):
        """Test bulk allocation with override_existing_work=True"""
        # Mock response for successful override
        mock_result = {
            "status": "success",
            "message": "Successfully processed allocations with overrides",
            "created_count": 0,
            "updated_count": 1,
            "overridden_count": 1,
            "total_allocations": 1,
            "override_used": True,
        }
        mock_post.return_value = mock_result

        # Call the method with override
        project_id = "project-id-1"
        allocations = [
            {
                "image_key": "images/image1.dcm",
                "annotators": ["annotator2@example.com"],
                "reviewers": ["reviewer1@example.com"],
            }
        ]
        result = self.projects_api.bulk_allocate_images(
            project_id=project_id,
            allocations=allocations,
            override_existing_work=True,
        )

        # Verify
        mock_post.assert_called_once_with(
            f"projects/{project_id}/bulk-allocate/",
            json={"allocations": allocations, "override_existing_work": True},
        )
        self.assertEqual(result, mock_result)
        self.assertTrue(result["override_used"])
        self.assertEqual(result["overridden_count"], 1)


if __name__ == "__main__":
    unittest.main()
