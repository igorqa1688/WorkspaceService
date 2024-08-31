import grpc
import workspace_service_pb2
import workspace_service_pb2_grpc
from functions import generate_guid
from global_vars import server


def create_workspace(club_guid: str) -> str:
    with grpc.insecure_channel(server) as channel:
        stub = workspace_service_pb2_grpc.WorkspaceServiceStub(channel)

        request = workspace_service_pb2.CreateWorkspaceRequest(
            club_guid=workspace_service_pb2.GUID(value=f"{club_guid}"))
        try:
            response = stub.CreateWorkspace(request)
            return response
        except Exception as error_create_workspace:
            return error_create_workspace


def get_all_workspaces() -> str:
    with grpc.insecure_channel(server) as channel:
        stub = workspace_service_pb2_grpc.WorkspaceServiceStub(channel)

        request = workspace_service_pb2.GetAllWorkspacesResponse()
        try:
            response = stub.GetAllWorkspaces(request)
            return response
        except Exception as e:
            return e


def get_workspace_by_guid(workspace_guid: str) -> str:
    with grpc.insecure_channel(server) as channel:
        stub = workspace_service_pb2_grpc.WorkspaceServiceStub(channel)

        request = workspace_service_pb2.GetWorkspaceRequest(
            workspace_guid=workspace_service_pb2.GUID(value=f"{workspace_guid}"))
        try:
            response = stub.GetWorkspace(request)
            return response
        except Exception as e:
            return e


def get_workspace_by_club_guid(club_guid: str) -> str:
    with grpc.insecure_channel(server) as channel:
        stub = workspace_service_pb2_grpc.WorkspaceServiceStub(channel)

        request = workspace_service_pb2.GetWorkspaceRequest(
            club_guid=workspace_service_pb2.GUID(value=f"{club_guid}"))
        try:
            print(request)
            response = stub.GetWorkspace(request)
            return response
        except Exception as e:
            return e


def get_workspace(workspace_guid: str, club_guid: str) -> str:
    with grpc.insecure_channel(server) as channel:
        stub = workspace_service_pb2_grpc.WorkspaceServiceStub(channel)

        request = workspace_service_pb2.GetWorkspaceRequest(
            club_guid=workspace_service_pb2.GUID(value=f"{club_guid}"),
            workspace_guid=workspace_service_pb2.GUID(value=f"{workspace_guid}"))
        try:
            print(request)
            response = stub.GetWorkspace(request)
            return response
        except Exception as e:
            return e


if __name__ == "__main__":
    club_guid = generate_guid()
    create_workspace(club_guid)
    all_workspaces = get_all_workspaces().workspaces
    print(all_workspaces)
    workspace_guid = all_workspaces[0].workspace_guid.value
    workspace_club_guid = all_workspaces[0].club_guid.value
    print(f"workspace_guid: {workspace_guid}\nworkspace_club_guid: {workspace_club_guid}")
    print(get_workspace_by_club_guid(workspace_club_guid))