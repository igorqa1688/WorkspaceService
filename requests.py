import grpc
import workspace_service_pb2
import workspace_service_pb2_grpc
from functions import generate_guid
from global_vars import server


def create_workspace(club_guid: str) -> str:
    with grpc.insecure_channel(server) as channel:
        stub = workspace_service_pb2_grpc.WorkspaceServiceStub(channel)

        request = workspace_service_pb2.CreateWorkspaceRequest(
            club_guid=workspace_service_pb2.GUID(value=club_guid))
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


def put_user_to_workspace(workspace_guid: str, club_guid: str, user_guid: str, user_role: str, user_workspace_description: str ) -> str:
    with grpc.insecure_channel(server) as channel:
        stub = workspace_service_pb2_grpc.WorkspaceServiceStub(channel)

        request = workspace_service_pb2.PutUserToWorkspaceRequest(
            #club_guid=workspace_service_pb2.GUID(value=club_guid),
            user_guid=workspace_service_pb2.GUID(value=user_guid),
            user_role=workspace_service_pb2.WorkspaceUserRoleMessage.Value(user_role),
            user_workspace_description=user_workspace_description,
            workspace_guid=workspace_service_pb2.GUID(value=workspace_guid)
        )
        try:
            print(f"request put_user_to_workspace:\n{request}")
            response = stub.PutUserToWorkspace(request)
            return response
        except Exception as e:
            return f"error: {e}"



def add_visible_player_to_user(player_guids: str, workspace_guid: str, club_guid: str, user_guid: str) -> str:
    with grpc.insecure_channel(server) as channel:
        stub = workspace_service_pb2_grpc.WorkspaceServiceStub(channel)
        request = workspace_service_pb2.AddVisiblePlayersToUserRequest(
            #club_guid=workspace_service_pb2.GUID(value=club_guid),
            user_guid=workspace_service_pb2.GUID(value=user_guid),
            player_guids=[player_guids],
            workspace_guid=workspace_service_pb2.GUID(value=workspace_guid)
        )
        try:
            print(f"request add_visible_player_to_user:\n{request}")
            response = stub.AddVisiblePlayersToUser(request)
            return response
        except Exception as e:
            return f"error: {e}"


if __name__ == "__main__":
    club_guid = generate_guid()
    user_guid = generate_guid()
    player_guid = generate_guid()
    user_workspace_description = "UserDescription"
    user_role = "ROLE_OWNER"
    print("\ncreate_workspace response:\n",create_workspace(club_guid))
    all_workspaces = get_all_workspaces().workspaces
    print(all_workspaces[0])
    workspace_guid = all_workspaces[0].workspace_guid.value
    workspace_club_guid = all_workspaces[0].club_guid.value

    print("response put_user_to_workspace:\n", put_user_to_workspace(workspace_guid, workspace_club_guid, user_guid, user_role, user_workspace_description))
    #print("response add_visible_player_to_user\n", add_visible_player_to_user(player_guid, workspace_guid, workspace_club_guid, user_guid))