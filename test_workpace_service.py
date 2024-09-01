import pytest
from requests import get_all_workspaces


# test GetAllWorkspaces
def test_get_all_workspaces():
    response = get_all_workspaces()
    assert len(response.workspaces) > 0