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


def get_workspace_by_workspace_guid(workspace_guid: str) -> str:
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
            response = stub.GetWorkspace(request)
            return response
        except Exception as e:
            return e


def get_workspace(workspace_guid: None, club_guid: None) -> str:
    with grpc.insecure_channel(server) as channel:
        stub = workspace_service_pb2_grpc.WorkspaceServiceStub(channel)
        if workspace_guid:
            request = workspace_service_pb2.GetWorkspaceRequest(
                workspace_guid=workspace_service_pb2.GUID(value=workspace_guid)
            )
        elif club_guid:
            request = workspace_service_pb2.GetWorkspaceRequest(
                club_guid=workspace_service_pb2.GUID(value=club_guid)
            )
        try:
            response = stub.GetWorkspace(request)
            return response
        except Exception as e:
            return e


def get_workspace_with_users(workspace_guid: None, club_guid: None) -> str:
    with grpc.insecure_channel(server) as channel:
        stub = workspace_service_pb2_grpc.WorkspaceServiceStub(channel)
        if workspace_guid:
            request = workspace_service_pb2.GetWorkspaceWithUsersRequest(
                workspace_guid=workspace_service_pb2.GUID(value=workspace_guid)
            )
        elif club_guid:
            request = workspace_service_pb2.GetWorkspaceWithUsersRequest(
                club_guid=workspace_service_pb2.GUID(value=club_guid)
            )
        try:
            response = stub.GetWorkspaceWithUsers(request)
            return response
        except Exception as e:
            return e


def get_workspace_with_users_only_workspace_guid(workspace_guid: str) -> str:
    with grpc.insecure_channel(server) as channel:
        stub = workspace_service_pb2_grpc.WorkspaceServiceStub(channel)

        request = workspace_service_pb2.GetWorkspaceWithUsersRequest(
            workspace_guid=workspace_service_pb2.GUID(value=workspace_guid)
        )
        try:
            response = stub.GetUserWorkspaces(request)
            return response
        except Exception as e:
            return e


def get_workspace_with_users_only_club_guid(club_guid: str) -> str:
    with grpc.insecure_channel(server) as channel:
        stub = workspace_service_pb2_grpc.WorkspaceServiceStub(channel)

        request = workspace_service_pb2.GetWorkspaceWithUsersRequest(
            club_guid=workspace_service_pb2.GUID(value=club_guid)
        )
        try:
            response = stub.GetWorkspaceWithUsers(request)
            return response
        except Exception as e:
            return e


def get_user_workspaces(user_guid: str) -> str:
    with grpc.insecure_channel(server) as channel:
        stub = workspace_service_pb2_grpc.WorkspaceServiceStub(channel)

        request = workspace_service_pb2.GetUserWorkspacesRequest(
            user_guid=workspace_service_pb2.GUID(value=user_guid))
        try:
            response = stub.GetUserWorkspaces(request)
            return response
        except Exception as e:
            return e


def get_user_in_workspace(workspace_guid: None, club_guid: None, user_guid: str) -> str:
    with grpc.insecure_channel(server) as channel:
        stub = workspace_service_pb2_grpc.WorkspaceServiceStub(channel)
        if workspace_guid:
            request = workspace_service_pb2.GetUserInWorkspaceRequest(
                workspace_guid=workspace_service_pb2.GUID(value=workspace_guid),
                user_guid=workspace_service_pb2.GUID(value=user_guid)
            )
            print('by workspace_guid')
        elif club_guid:
            request = workspace_service_pb2.GetUserInWorkspaceRequest(
                club_guid=workspace_service_pb2.GUID(value=club_guid),
                user_guid=workspace_service_pb2.GUID(value=user_guid)
            )
            print('by club_guid')
        try:
            response = stub.GetUserInWorkspace(request)
            return response
        except Exception as e:
            return f"error: {e}"


def put_user_to_workspace(workspace_guid: None, club_guid: None, user_guid: str, user_role: str, user_workspace_description: None ) -> str:
    with grpc.insecure_channel(server) as channel:
        stub = workspace_service_pb2_grpc.WorkspaceServiceStub(channel)
        if workspace_guid:
            request = workspace_service_pb2.PutUserToWorkspaceRequest(
                user_guid=workspace_service_pb2.GUID(value=user_guid),
                user_role=workspace_service_pb2.WorkspaceUserRoleMessage.Value(user_role),
                user_workspace_description=user_workspace_description,
                workspace_guid=workspace_service_pb2.GUID(value=workspace_guid)
            )
        elif club_guid:
            request = workspace_service_pb2.PutUserToWorkspaceRequest(
                club_guid=workspace_service_pb2.GUID(value=club_guid),
                user_guid=workspace_service_pb2.GUID(value=user_guid),
                user_role=workspace_service_pb2.WorkspaceUserRoleMessage.Value(user_role),
                user_workspace_description=user_workspace_description,
            )
        try:
            response = stub.PutUserToWorkspace(request)
            return response
        except Exception as e:
            return f"error: {e}"


def put_user_to_workspace_without_user_workspace_description(workspace_guid: None, club_guid: None, user_guid: str, user_role: str) -> str:
    with grpc.insecure_channel(server) as channel:
        stub = workspace_service_pb2_grpc.WorkspaceServiceStub(channel)
        if workspace_guid:
            request = workspace_service_pb2.PutUserToWorkspaceRequest(
                user_guid=workspace_service_pb2.GUID(value=user_guid),
                user_role=workspace_service_pb2.WorkspaceUserRoleMessage.Value(user_role),
                workspace_guid=workspace_service_pb2.GUID(value=workspace_guid)
            )
        elif club_guid:
            request = workspace_service_pb2.PutUserToWorkspaceRequest(
                club_guid=workspace_service_pb2.GUID(value=club_guid),
                user_guid=workspace_service_pb2.GUID(value=user_guid),
                user_role=workspace_service_pb2.WorkspaceUserRoleMessage.Value(user_role),
            )
        try:
            response = stub.PutUserToWorkspace(request)
            return response
        except Exception as e:
            return f"error: {e}"


def add_visible_players_to_user(player_guids: list, workspace_guid: None, club_guid: None, user_guid: str) -> str:
    with grpc.insecure_channel(server) as channel:
        stub = workspace_service_pb2_grpc.WorkspaceServiceStub(channel)
        if workspace_guid:
            request = workspace_service_pb2.AddVisiblePlayersToUserRequest(
                user_guid=workspace_service_pb2.GUID(value=user_guid),
                player_guids=player_guids,
                workspace_guid=workspace_service_pb2.GUID(value=workspace_guid)
        )
        elif club_guid:
            request = workspace_service_pb2.AddVisiblePlayersToUserRequest(
                club_guid=workspace_service_pb2.GUID(value=club_guid),
                user_guid=workspace_service_pb2.GUID(value=user_guid),
                player_guids=player_guids,
            )
        try:
            response = stub.AddVisiblePlayersToUser(request)
            return response
        except Exception as e:
            return e


def remove_user_from_workspace(workspace_guid: None, club_guid: None, user_guid: str) -> str:
    with grpc.insecure_channel(server) as channel:
        stub = workspace_service_pb2_grpc.WorkspaceServiceStub(channel)
        if workspace_guid:
            request = workspace_service_pb2.RemoveUserFromWorkspaceRequest(
                workspace_guid=workspace_service_pb2.GUID(value=workspace_guid),
                user_guid=workspace_service_pb2.GUID(value=user_guid)
            )
        elif club_guid:
            request = workspace_service_pb2.RemoveUserFromWorkspaceRequest(
                club_guid=workspace_service_pb2.GUID(value=club_guid),
                user_guid=workspace_service_pb2.GUID(value=user_guid)
            )
        try:
            stub.RemoveUserFromWorkspace(request)
            return 0
        except Exception as e:
            return e



def remove_visible_players_from_user(workspace_guid: None, club_guid: None, user_guid: str, player_guids: str) -> str:
    with grpc.insecure_channel(server) as channel:
        stub = workspace_service_pb2_grpc.WorkspaceServiceStub(channel)
        if workspace_guid:
            request = workspace_service_pb2.RemoveVisiblePlayersFromUserRequest(
                user_guid=workspace_service_pb2.GUID(value=user_guid),
                workspace_guid=workspace_service_pb2.GUID(value=workspace_guid),
                player_guids=player_guids
            )
        elif club_guid:
            request = workspace_service_pb2.RemoveVisiblePlayersFromUserRequest(
                club_guid=workspace_service_pb2.GUID(value=club_guid),
                user_guid=workspace_service_pb2.GUID(value=user_guid),
                player_guids=player_guids

            )
        else:
            return f"error remove_visible_players_from_user: workspace_guid {workspace_guid}, club_guid {club_guid}"
        try:
            stub.RemoveVisiblePlayersFromUser(request)
            return 0
        except Exception as e:
            return f"error: {e}"


if __name__ == "__main__":
    # Генерация club_guid для создания workspace
    club_guid = generate_guid()
    # Гененрация user_guid
    user_guid = generate_guid()
    player_guid = generate_guid()
    # Заполнение списка players_guid
    players_guid = []
    for i in range(2):
        players_guid.append(generate_guid())
    user_workspace_description = "UserDescription"
    user_role = "ROLE_OWNER"

    all_workspaces = get_all_workspaces().workspaces
    workspace_guid = all_workspaces[0].workspace_guid.value
    workspace_club_guid = all_workspaces[0].club_guid.value

    # CreateWorkspace
    print("\ncreate_workspace response:\n", create_workspace(club_guid), "\n--")
    # AllWorkspaces
    print(f"{all_workspaces[0]}, user_guid: {user_guid}\n--")

    # PutUserToWorkspace
    print("response put_user_to_workspace:\n", put_user_to_workspace(workspace_guid, workspace_club_guid, user_guid, user_role, user_workspace_description), "\n--")

    # AddVisisblePlayersToUser
    print("response add_visible_players_to_user\n", add_visible_players_to_user(players_guid, workspace_guid, workspace_club_guid, user_guid), "\n--")

    # GetUserInWorkspace
    print(f"response get_user_in_workspace:\n{get_user_in_workspace(workspace_guid, workspace_club_guid, user_guid)}\n---")
    # GetUserWorkspaces
    print(f"response get_user_workspaces:\n{get_user_workspaces(user_guid)}\n---")

    #GetWorkspaceWithUsers
    print(f"response get_workspace_with_users:\n{get_workspace_with_users(workspace_guid, workspace_club_guid)}\n---")
    print(f"response get_workspace_with_users_only_workspace_guid:\n{get_workspace_with_users_only_workspace_guid(workspace_guid)}\n---")
    print(f"response get_workspace_with_users_only_club_guid:\n{get_workspace_with_users_only_club_guid(workspace_club_guid)}\n---")

    #GetWorkspace
    print(f"response get_workspace:\n{get_workspace(workspace_guid, workspace_club_guid)}\n---")
    print(f"response get_workspace_by_club_guid:\n{get_workspace_by_club_guid(workspace_club_guid)}\n---")
    print(f"response get_workspace_by_workspace_guid:\n{get_workspace_by_workspace_guid(workspace_guid)}\n---")


    # RemoveVisiblePlayersFromUser
    print(f"response remove_visible_players_from_user:\n{remove_visible_players_from_user(workspace_guid, None, user_guid, players_guid)}\n---")
    # RemoveUserFromWorkspace
    print(f"response remove_user_from_workspace:\n{remove_user_from_workspace(workspace_guid, club_guid, user_guid)}\n---")


