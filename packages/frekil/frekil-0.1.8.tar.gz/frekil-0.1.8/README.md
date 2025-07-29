# Frekil SDK

The official Python SDK for the Frekil API.

## Installation

```bash
pip install frekil
```

## Usage

### Authentication

To use the SDK, you'll need an API key from your Frekil account:

```python
from frekil import FrekilClient

# Initialize the client with your API key
client = FrekilClient(api_key="your-api-key")

# Optionally specify a custom base URL (e.g., for development)
client = FrekilClient(
    api_key="your-api-key",
    base_url="https://dev.notatehq.com/api/sdk"
)
```

### Working with Projects

#### List Projects

Get all projects the authenticated user has access to:

```python
# Get all projects
projects = client.projects.list()

# Example response:
# [
#     {
#         "id": "uuid",
#         "name": "Project Name",
#         "description": "Project Description",
#         "role": "ADMIN",  # User's role in the project
#         "created_at": "2024-03-21T10:00:00Z",
#         "updated_at": "2024-03-21T10:00:00Z",
#         "is_ct_scan": true,
#         "tags": ["tag1", "tag2"]
#     },
#     ...
# ]
```

#### Get Project Membership

Get membership details for a specific project including user roles and status:

```python
# Get project membership
project_id = "project-uuid"
memberships = client.projects.get_membership(project_id)

# Example response:
# [
#     {
#         "user_id": "uuid",
#         "email": "user@example.com",
#         "name": "User Name",  # Full name or email if name not set
#         "role": "ADMIN",      # User's role in the project
#         "percentage": 100,    # User's allocation percentage
#         "is_active": true,    # Whether the user is active
#         "is_project_admin": true,  # Whether user is project admin
#         "created_at": "2024-03-21T10:00:00Z",
#         "updated_at": "2024-03-21T10:00:00Z"
#     },
#     ...
# ]
```

#### Get Project Images

Get all images in a project:

```python
# Get project images
project_id = "project-uuid"
images = client.projects.get_images(project_id)

# Example response:
# [
#     {
#         "id": "images/image1.dcm",  # Full image key
#         "filename": "image1.dcm",   # Just the filename
#         "created_at": "2024-03-21T10:00:00Z",
#         "updated_at": "2024-03-21T10:00:00Z"
#     },
#     ...
# ]
```

#### Get Project Allocations

Get all allocations in a project, including user roles for both annotators and reviewers:

```python
# Get project allocations
project_id = "project-uuid"
allocations = client.projects.get_allocations(project_id)

# Example response:
# [
#     {
#         "allocation_id": "uuid",
#         "image_id": "images/image1.dcm",  # Full image key
#         "image_filename": "image1.dcm",   # Just the filename
#         "annotator_email": "annotator@example.com",  # May be null
#         "reviewer_email": "reviewer@example.com",    # May be null
#         "status": "PENDING",  # One of: PENDING, PENDING_REVIEW, APPROVED, REJECTED
#         "created_at": "2024-03-21T10:00:00Z",
#         "is_ground_truth": false
#     },
#     ...
# ]
```

#### Bulk Allocate Images

Allocate images to specific annotators and reviewers:

```python
# Allocate images to specific annotators and reviewers
project_id = "project-uuid"
allocations = [
    {
        "image_key": "images/image1.dcm",  # Full image key
        "annotators": ["annotator1@example.com", "annotator2@example.com"],
        "reviewers": ["reviewer1@example.com", "reviewer2@example.com"]
    },
    {
        "image_key": "images/image2.dcm",
        "annotators": ["annotator1@example.com"],
        "reviewers": ["reviewer1@example.com"]
    }
]

# Set override_existing_work=True to override allocations even if work has been done
result = client.projects.bulk_allocate_images(
    project_id=project_id,
    allocations=allocations,
    override_existing_work=False
)

# Example success response:
# {
#     "status": "success",
#     "message": "Successfully processed allocations",
#     "created_count": 5,      # Number of new allocations created
#     "updated_count": 2,      # Number of existing allocations updated
#     "overridden_count": 1,   # Number of allocations with work that were overridden
#     "total_allocations": 8,  # Total number of allocations processed
#     "override_used": true    # Whether override_existing_work was used
# }

# Example validation error response:
# {
#     "status": "validation_failed",
#     "errors": ["Missing image_key in allocation 1"],
#     "invalid_users": [
#         {
#             "email": "user@example.com",
#             "role": "annotator",
#             "reason": "User is not a project member with annotator role",
#             "allocation_index": 1,
#             "image_key": "image1.dcm"
#         }
#     ],
#     "existing_work": [
#         {
#             "image_key": "image1.dcm",
#             "annotator": "annotator@example.com",
#             "reviewer": "reviewer@example.com",
#             "allocation_index": 1,
#             "existing_work": [
#                 {
#                     "type": "annotation",
#                     "user": "annotator@example.com",
#                     "created_at": "2024-03-21T10:00:00Z",
#                     "status": "completed"
#                 }
#             ],
#             "message": "Cannot modify allocation as work has already been done",
#             "can_override": true
#         }
#     ],
#     "message": "Please fix the following issues before proceeding:",
#     "instructions": {
#         "invalid_users": "Ensure all users exist and have the correct project role",
#         "existing_work": "Cannot modify allocations where work has already been done. Use override_existing_work=true to force changes.",
#         "errors": "Fix any missing or invalid data in the request"
#     },
#     "override_available": true,
#     "override_instructions": "To override existing work, set override_existing_work=true in the request body"
# }
```

## Error Handling

The SDK uses custom exception classes to handle API errors:

```python
from frekil.exceptions import FrekilAPIError, FrekilClientError

try:
    projects = client.projects.list()
except FrekilClientError as e:
    # Handle client errors (e.g., authentication issues, invalid parameters)
    print(f"Client error: {e} (Status: {e.status_code})")
    print(f"Error details: {e.error_details}")
except FrekilAPIError as e:
    # Handle API errors (e.g., server issues)
    print(f"API error: {e} (Status: {e.status_code})")
    print(f"Error details: {e.error_details}")
```

## Development

### Setup

```bash
# Clone the repository
git clone https://github.com/notatehq/frekil-python-sdk.git
cd frekil-python-sdk

# Install dependencies
pip install -e ".[dev]"
```

### Testing

```bash
pytest
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.