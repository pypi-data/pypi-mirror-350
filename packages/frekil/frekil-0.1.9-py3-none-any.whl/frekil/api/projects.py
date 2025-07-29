"""
Projects API endpoints

This module provides methods for interacting with Frekil's Project Management API.
All endpoints require API key authentication and appropriate project permissions.
"""

from typing import List, Dict, Any, Optional, Literal
from .base import BaseAPI


class ProjectsAPI(BaseAPI):
    """
    Projects API endpoints for managing Frekil projects, images, and allocations.

    This class provides methods for:
    - Listing and managing projects
    - Managing project memberships
    - Handling image allocations
    - Bulk operations for image assignments

    All methods require API key authentication and appropriate project permissions.
    """

    def list(self) -> List[Dict[str, Any]]:
        """
        List all projects the authenticated user has access to.

        This endpoint returns a list of projects where the API key owner is a member.
        Each project includes metadata about the user's role and project settings.

        Returns:
            List[Dict[str, Any]]: List of projects with their metadata:
                [
                    {
                        "id": str,              # Project UUID
                        "name": str,            # Project name
                        "description": str,     # Project description
                        "role": str,            # User's role (ADMIN, ANNOTATOR, REVIEWER)
                        "created_at": str,      # ISO 8601 timestamp
                        "updated_at": str,      # ISO 8601 timestamp
                        "is_ct_scan": bool,     # Whether project is for CT scans
                        "tags": List[str]       # Project tags
                    },
                    ...
                ]

        Raises:
            FrekilAPIError: If the API server encounters an error
            FrekilClientError: If the request is invalid or unauthorized
        """
        return self.client.get("projects/")

    def get_membership(self, project_id: str) -> List[Dict[str, Any]]:
        """
        Get detailed membership information for a specific project.

        This endpoint returns a list of all users who are members of the project,
        including their roles, status, and allocation percentages. The API key owner
        must have access to the project to use this endpoint.

        Args:
            project_id (str): The UUID of the project

        Returns:
            List[Dict[str, Any]]: List of project memberships:
                [
                    {
                        "user_id": str,         # User UUID
                        "email": str,           # User's email
                        "name": str,            # User's full name or email
                        "role": str,            # User's role (ADMIN, ANNOTATOR, REVIEWER)
                        "percentage": int,      # User's allocation percentage
                        "is_active": bool,      # Whether user account is active
                        "is_project_admin": bool,  # Whether user is project admin
                        "created_at": str,      # ISO 8601 timestamp
                        "updated_at": str       # ISO 8601 timestamp
                    },
                    ...
                ]

        Raises:
            FrekilClientError: If project_id is invalid or user lacks access
            FrekilAPIError: If the API server encounters an error
        """
        return self.client.get(f"projects/{project_id}/membership/")

    def get_images(self, project_id: str) -> List[Dict[str, Any]]:
        """
        Get all images in a project.

        This endpoint returns metadata for all images that have been allocated in the project.
        The API key owner must have access to the project to use this endpoint.

        Args:
            project_id (str): The UUID of the project

        Returns:
            List[Dict[str, Any]]: List of images with their metadata:
                [
                    {
                        "id": str,              # Full image key (e.g., "images/image1.dcm")
                        "filename": str,        # Just the filename (e.g., "image1.dcm")
                        "created_at": str,      # ISO 8601 timestamp
                        "updated_at": str       # ISO 8601 timestamp
                    },
                    ...
                ]

        Raises:
            FrekilClientError: If project_id is invalid or user lacks access
            FrekilAPIError: If the API server encounters an error
        """
        return self.client.get(f"projects/{project_id}/images/")

    def get_allocations(self, project_id: str) -> List[Dict[str, Any]]:
        """
        Get all image allocations in a project.

        This endpoint returns detailed information about how images are allocated to
        annotators and reviewers, including the current status of each allocation.
        The API key owner must have access to the project to use this endpoint.

        Args:
            project_id (str): The UUID of the project

        Returns:
            List[Dict[str, Any]]: List of allocations with their metadata:
                [
                    {
                        "allocation_id": str,   # Allocation UUID
                        "image_id": str,        # Full image key
                        "image_filename": str,  # Just the filename
                        "annotator_email": Optional[str],  # Annotator's email or null
                        "reviewer_email": Optional[str],   # Reviewer's email or null
                        "status": Literal["PENDING", "PENDING_REVIEW", "APPROVED", "REJECTED"],
                        "created_at": str,      # ISO 8601 timestamp
                        "is_ground_truth": bool # Whether this is a ground truth allocation
                    },
                    ...
                ]

        Note:
            Status values indicate the current state of the allocation:
            - PENDING: No annotation or review done yet
            - PENDING_REVIEW: Annotation completed, waiting for review
            - APPROVED: Review completed and approved
            - REJECTED: Review completed and rejected

        Raises:
            FrekilClientError: If project_id is invalid or user lacks access
            FrekilAPIError: If the API server encounters an error
        """
        return self.client.get(f"projects/{project_id}/allocations/")

    def bulk_allocate_images(
        self,
        project_id: str,
        allocations: List[Dict[str, Any]],
        override_existing_work: bool = False,
    ) -> Dict[str, Any]:
        """
        Bulk allocate images to annotators and reviewers.

        This endpoint allows you to create or update multiple image allocations in a single request.
        The API key owner must be a project administrator to use this endpoint.

        The endpoint performs several validations:
        1. Verifies all users exist and have appropriate project roles
        2. Checks for existing work (annotations/reviews) that would be affected
        3. Validates the allocation data format
        4. Handles conflicts with existing allocations

        Args:
            project_id (str): The UUID of the project
            allocations (List[Dict[str, Any]]): List of allocation objects:
                [
                    {
                        "image_key": str,      # Full image key (e.g., "images/image1.dcm")
                        "annotators": List[str],  # List of annotator emails
                        "reviewers": List[str]    # List of reviewer emails
                    },
                    ...
                ]
            override_existing_work (bool, optional): Whether to override existing work.
                If False (default), allocations with existing work will be rejected.
                If True, will override allocations even if work has been done.

        Returns:
            Dict[str, Any]: Result of the allocation operation:
                {
                    "status": Literal["success", "validation_failed"],
                    "message": str,            # Success or error message
                    "created_count": int,      # Number of new allocations created
                    "updated_count": int,      # Number of existing allocations updated
                    "overridden_count": int,   # Number of allocations with work that were overridden
                    "total_allocations": int,  # Total number of allocations processed
                    "override_used": bool      # Whether override_existing_work was used
                }

        Raises:
            FrekilClientError: If validation fails, with detailed error information:
                {
                    "status": "validation_failed",
                    "errors": List[str],       # List of general validation errors
                    "invalid_users": List[Dict[str, Any]],  # Invalid user details:
                        [
                            {
                                "email": str,           # User's email
                                "role": str,            # "annotator" or "reviewer"
                                "reason": str,          # Why the user is invalid
                                "allocation_index": int,# Index in allocations list
                                "image_key": str        # Affected image key
                            }
                        ]
                    "existing_work": List[Dict[str, Any]],  # Existing work details:
                        [
                            {
                                "image_key": str,
                                "annotator": str,
                                "reviewer": str,
                                "allocation_index": int,
                                "existing_work": List[Dict[str, Any]]:
                                    [
                                        {
                                            "type": Literal["annotation", "review"],
                                            "user": str,
                                            "created_at": str,
                                            "status": str
                                        }
                                    ],
                                "message": str,
                                "can_override": bool
                            }
                        ]
                    "message": str,            # General error message
                    "instructions": Dict[str, str],  # How to fix the errors
                    "override_available": bool,      # Whether override is possible
                    "override_instructions": str     # How to use override
                }
            FrekilAPIError: If the API server encounters an error

        Note:
            - All users must be project members with appropriate roles
            - Annotators must have ANNOTATOR role
            - Reviewers must have REVIEWER role
            - The API key owner must be a project administrator
            - Image keys must be valid and exist in the project
            - Existing work (annotations/reviews) will be preserved unless overridden
        """
        data = {
            "allocations": allocations,
            "override_existing_work": override_existing_work,
        }
        return self.client.post(f"projects/{project_id}/bulk-allocate/", json=data)
