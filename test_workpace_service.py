import pytest
from requests import get_all_workspaces


def test_get_all_workspaces():
    response = get_all_workspaces()
    assert len(response.workspaces) > 0