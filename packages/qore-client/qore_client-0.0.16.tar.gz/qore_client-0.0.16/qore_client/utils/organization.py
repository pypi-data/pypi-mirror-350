import pandas as pd


class OrganizationOperations:
    """Organization operation utilities for QoreClient"""

    def __init__(self, request_method):
        """
        Initialize with the request method from the parent client
        """
        self._request = request_method

    def get_organization_list(self) -> pd.DataFrame:
        """
        조직 목록을 가져옵니다.
        """
        response = self._request("GET", "/api/organization/list")
        return pd.DataFrame(response)

    def get_drive_list(self, organization_id: str) -> pd.DataFrame:
        """
        조직 내 드라이브 목록을 가져옵니다.
        """
        response = self._request("GET", f"/api/organization/{organization_id}/drives")
        return pd.DataFrame(response)
