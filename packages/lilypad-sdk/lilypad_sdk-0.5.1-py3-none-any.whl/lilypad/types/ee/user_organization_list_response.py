# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List
from typing_extensions import TypeAlias

from .user_organization_table import UserOrganizationTable

__all__ = ["UserOrganizationListResponse"]

UserOrganizationListResponse: TypeAlias = List[UserOrganizationTable]
