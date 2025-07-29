"""
Allocations API endpoints

This module provides methods for managing image allocations in Frekil projects.
All endpoints require API key authentication and appropriate project permissions.
"""

from typing import List, Dict, Any, Optional, Literal, Union
from .base import BaseAPI


class AllocationsAPI(BaseAPI):
    """
    Allocations API endpoints for managing image allocations in Frekil projects.

    This class provides methods for:
    - Creating and managing individual allocations
    - Bulk operations for allocations
    - Updating reviewer assignments
    - Querying allocation status

    All methods require API key authentication and appropriate project permissions.
    """

    def create(
        self,
        project_id: str,
        image_key: str,
        annotator: str,
        reviewer: str,
        is_ground_truth: bool = False,
    ) -> Dict[str, Any]:
        """
        Create a new allocation for an image.

        Args:
            project_id (str): The UUID of the project
            image_key (str): Full image key (e.g., "images/image1.dcm")
            annotator (str): Annotator's email
            reviewer (str): Reviewer's email
            is_ground_truth (bool, optional): Whether this is a ground truth allocation

        Returns:
            Dict[str, Any]: Created allocation details
        """
        data = {
            "image_key": image_key,
            "annotator": annotator,
            "reviewer": reviewer,
            "is_ground_truth": is_ground_truth,
        }
        return self.client.post(f"projects/{project_id}/allocations/create/", json=data)

    def get(self, project_id: str, allocation_id: str) -> Dict[str, Any]:
        """
        Get details of a specific allocation.

        Args:
            project_id (str): The UUID of the project
            allocation_id (str): The UUID of the allocation

        Returns:
            Dict[str, Any]: Allocation details
        """
        return self.client.get(f"projects/{project_id}/allocations/{allocation_id}/")

    def list(
        self,
        project_id: str,
        image_key: Optional[str] = None,
        annotator: Optional[str] = None,
        reviewer: Optional[str] = None,
        status: Optional[
            Literal["PENDING", "PENDING_REVIEW", "APPROVED", "REJECTED"]
        ] = None,
    ) -> List[Dict[str, Any]]:
        """
        List allocations with optional filtering.

        Args:
            project_id (str): The UUID of the project
            image_key (Optional[str]): Filter by image key
            annotator (Optional[str]): Filter by annotator email
            reviewer (Optional[str]): Filter by reviewer email
            status (Optional[str]): Filter by allocation status

        Returns:
            List[Dict[str, Any]]: List of matching allocations
        """
        params = {
            "image_key": image_key,
            "annotator": annotator,
            "reviewer": reviewer,
            "status": status,
        }
        # Remove None values
        params = {k: v for k, v in params.items() if v is not None}
        return self.client.get(f"projects/{project_id}/allocations/", params=params)

    def update(
        self,
        project_id: str,
        allocation_id: str,
        annotator: Optional[str] = None,
        reviewer: Optional[str] = None,
        is_ground_truth: Optional[bool] = None,
        override_existing_work: bool = False,
    ) -> Dict[str, Any]:
        """
        Update an existing allocation.

        Args:
            project_id (str): The UUID of the project
            allocation_id (str): The UUID of the allocation
            annotator (Optional[str]): New annotator email
            reviewer (Optional[str]): New reviewer email
            is_ground_truth (Optional[bool]): New ground truth status
            override_existing_work (bool): Whether to override existing work

        Returns:
            Dict[str, Any]: Updated allocation details
        """
        data = {
            "annotator": annotator,
            "reviewer": reviewer,
            "is_ground_truth": is_ground_truth,
            "override_existing_work": override_existing_work,
        }
        # Remove None values
        data = {k: v for k, v in data.items() if v is not None}
        return self.client.put(
            f"projects/{project_id}/allocations/{allocation_id}/update/", json=data
        )

    def delete(
        self,
        project_id: str,
        allocation_id: str,
        override_existing_work: bool = False,
    ) -> None:
        """
        Delete an allocation.

        Args:
            project_id (str): The UUID of the project
            allocation_id (str): The UUID of the allocation
            override_existing_work (bool): Whether to override existing work
        """
        params = {"override_existing_work": override_existing_work}
        self.client.delete(
            f"projects/{project_id}/allocations/{allocation_id}/delete/", params=params
        )

    def bulk_create(
        self,
        project_id: str,
        allocations: List[Dict[str, Any]],
        override_existing_work: bool = False,
    ) -> Dict[str, Any]:
        """
        Create multiple allocations in a single request.

        Args:
            project_id (str): The UUID of the project
            allocations (List[Dict[str, Any]]): List of allocation objects:
                [
                    {
                        "image_key": str,      # Full image key
                        "annotator": str,      # Annotator's email
                        "reviewer": str,       # Reviewer's email
                        "is_ground_truth": bool  # Optional, defaults to False
                    },
                    ...
                ]
            override_existing_work (bool): Whether to override existing work

        Returns:
            Dict[str, Any]: Result of the bulk operation
        """
        data = {
            "allocations": allocations,
            "override_existing_work": override_existing_work,
        }
        return self.client.post(
            f"projects/{project_id}/allocations/bulk-create/", json=data
        )

    def bulk_update_reviewers(
        self,
        project_id: str,
        updates: List[Dict[str, Any]],
        override_existing_work: bool = False,
    ) -> Dict[str, Any]:
        """
        Update reviewers for multiple allocations in a single request.

        Args:
            project_id (str): The UUID of the project
            updates (List[Dict[str, Any]]): List of update objects:
                [
                    {
                        "allocation_id": int,        # Required: ID of the allocation
                        "new_reviewer": str          # Required: New reviewer's email
                    },
                    ...
                ]
            override_existing_work (bool): Whether to override existing work

        Returns:
            Dict[str, Any]: Result of the bulk update operation:
                {
                    "status": str,
                    "results": {
                        "updated": List[Dict[str, Any]],
                        "skipped": List[Dict[str, Any]],
                        "failed": List[Dict[str, Any]]
                    },
                    "summary": {
                        "total_updates": int,
                        "successfully_updated": int,
                        "skipped": int,
                        "failed": int
                    }
                }
        """
        data = {
            "updates": updates,
            "override_existing_work": override_existing_work,
        }
        return self.client.post(
            f"projects/{project_id}/allocations/bulk-update-reviewers/", json=data
        )

    def bulk_update_by_filter(
        self,
        project_id: str,
        filter_criteria: Dict[str, Any],
        update_data: Dict[str, Any],
        override_existing_work: bool = False,
    ) -> Dict[str, Any]:
        """
        Update multiple allocations based on filter criteria.

        Args:
            project_id (str): The UUID of the project
            filter_criteria (Dict[str, Any]): Filter criteria:
                {
                    "image_keys": Optional[List[str]],    # List of image keys
                    "annotators": Optional[List[str]],    # List of annotator emails
                    "reviewers": Optional[List[str]],     # List of reviewer emails
                    "status": Optional[str]              # Allocation status
                }
            update_data (Dict[str, Any]): Data to update:
                {
                    "reviewer": Optional[str],           # New reviewer email
                    "annotator": Optional[str],          # New annotator email
                    "is_ground_truth": Optional[bool]    # New ground truth status
                }
            override_existing_work (bool): Whether to override existing work

        Returns:
            Dict[str, Any]: Result of the bulk update operation
        """
        data = {
            "filter": filter_criteria,
            "update": update_data,
            "override_existing_work": override_existing_work,
        }
        return self.client.post(
            f"projects/{project_id}/allocations/bulk-update/", json=data
        )
