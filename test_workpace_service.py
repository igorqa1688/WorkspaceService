import pytest
from requests import get_all_workspaces, create_workspace, get_workspace_by_workspace_guid, get_workspace_by_club_guid
from requests import (get_workspace, put_user_to_workspace, add_visible_players_to_user,
                      put_user_to_workspace_without_user_workspace_description, get_user_in_workspace,
                      get_user_workspaces, get_workspace_with_users)
from functions import generate_guid, generate_workspace_description, random_role
from global_vars import roles


# test CreateWorkspace
@pytest.mark.smoke
def test_create_workspace():
    club_guid = generate_guid()
    response = create_workspace(club_guid)
    assert len(response.workspace.workspace_guid.value) == 36
    assert response.workspace.club_guid.value == club_guid


# test GetAllWorkspaces
@pytest.mark.smoke
def test_get_all_workspaces():
    response = get_all_workspaces()
    workspaces = response.workspaces
    assert len(workspaces[0].workspace_guid.value) == 36
    assert len(workspaces[0].club_guid.value) == 36
    assert len(workspaces) > 0


# test GetWorkspace by workspace_guid
@pytest.mark.smoke
def test_get_workspace_by_workspace_guid():
    club_guid = generate_guid()
    # Создание workspace
    workspace = create_workspace(club_guid)
    # Получение workspace_guid созданного workspace
    workspace_guid = workspace.workspace.workspace_guid.value
    response = get_workspace_by_workspace_guid(workspace_guid)
    response_workspace_guid = response.workspace.workspace_guid.value
    response_club_guid = response.workspace.club_guid.value

    assert response_workspace_guid == workspace_guid
    assert response_club_guid == club_guid


# test GetWorkspace by club_guid
@pytest.mark.smoke
def test_get_workspace_by_club_guid():
    club_guid = generate_guid()
    # Создание workspace
    workspace = create_workspace(club_guid)
    # Получение workspace_guid созданного workspace
    workspace_guid = workspace.workspace.workspace_guid.value

    response = get_workspace_by_club_guid(club_guid)
    response_workspace_guid = response.workspace.workspace_guid.value
    response_club_guid = response.workspace.club_guid.value

    assert response_workspace_guid == workspace_guid
    assert response_club_guid == club_guid


# test GetWorkspace by club_guid, workspace_guid
@pytest.mark.smoke
def test_get_workspace():
    club_guid = generate_guid()
    # Создание workspace
    workspace = create_workspace(club_guid)
    # Получение workspace_guid созданного workspace
    workspace_guid = workspace.workspace.workspace_guid.value

    response = get_workspace(workspace_guid,club_guid)
    response_workspace_guid = response.workspace.workspace_guid.value
    response_club_guid = response.workspace.club_guid.value

    assert response_workspace_guid == workspace_guid
    assert response_club_guid == club_guid


# test PutUserToWorkspace by workspace role ROLE_OWNER with user_workspace_description
@pytest.mark.smoke
def test_put_user_to_workspace_with_user_workspace_description():
    club_guid = generate_guid()
    user_guid = generate_guid()
    user_role = roles[2]
    user_workspace_description = generate_workspace_description(300)
    # Создание workspace
    workspace = create_workspace(club_guid)
    # Получение workspace_guid созданного workspace
    workspace_guid = workspace.workspace.workspace_guid.value
    # Добавление юзера в в workspace
    response = put_user_to_workspace(workspace_guid, None,  user_guid, user_role, user_workspace_description)
    # Распаковка ответа
    response_workspace_guid = response.workspace_guid.value
    response_club_guid = response.club_guid.value
    response_user_guid = response.user_guid.value
    response_user_workspace_description = response.user_workspace_description
    response_role_in_workspace = response.role_in_workspace

    assert response_workspace_guid == workspace_guid
    assert response_club_guid == club_guid
    assert response_user_guid == user_guid
    assert response_user_workspace_description == user_workspace_description
    assert response_role_in_workspace == roles.index(user_role)


# test PutUserToWorkspace by workspace role ROLE_MANAGER with user_workspace_description
@pytest.mark.smoke
def test_put_user_to_workspace_role_owner():
    club_guid = generate_guid()
    user_guid = generate_guid()
    user_role = roles[1]
    user_workspace_description = ""
    # Создание workspace
    workspace = create_workspace(club_guid)
    # Получение workspace_guid созданного workspace
    workspace_guid = workspace.workspace.workspace_guid.value
    # Добавление юзера в в workspace
    response = put_user_to_workspace(None, club_guid,  user_guid, user_role, "")
    # Распаковка ответа
    response_workspace_guid = response.workspace_guid.value
    response_club_guid = response.club_guid.value
    response_user_guid = response.user_guid.value
    response_role_in_workspace = response.role_in_workspace
    response_user_workspace_description = response.user_workspace_description

    assert response_workspace_guid == workspace_guid
    assert response_club_guid == club_guid
    assert response_user_guid == user_guid
    assert len(response_user_workspace_description) == 0
    assert response_role_in_workspace == roles.index(user_role)


# test PutUserToWorkspace by workspace role ROLE_UNKNOWN with user_workspace_description
@pytest.mark.smoke
def test_put_user_to_workspace_without_user_workspace_description():
    club_guid = generate_guid()
    user_guid = generate_guid()
    user_role = roles[0]
    # Создание workspace
    workspace = create_workspace(club_guid)
    # Получение workspace_guid созданного workspace
    workspace_guid = workspace.workspace.workspace_guid.value
    # Добавление юзера в в workspace
    response = put_user_to_workspace_without_user_workspace_description(workspace_guid, club_guid,  user_guid, user_role)
    # Распаковка ответа
    response_workspace_guid = response.workspace_guid.value
    response_club_guid = response.club_guid.value
    response_user_guid = response.user_guid.value
    response_role_in_workspace = response.role_in_workspace

    assert response_workspace_guid == workspace_guid
    assert response_club_guid == club_guid
    assert response_user_guid == user_guid
    assert response_role_in_workspace == roles.index(user_role)


# test AddVisisblePlayersToUser one player by workspace_guid
@pytest.mark.smoke
def test_add_visible_players_to_user_by_workspace_guid():
    club_guid = generate_guid()
    user_guid = generate_guid()
    players_guid = [generate_guid()]
    user_role = roles[0]

    # Создание workspace
    workspace = create_workspace(club_guid)
    # Получение workspace_guid созданного workspace
    workspace_guid = workspace.workspace.workspace_guid.value
    # Добавление user в workspace
    put_user_to_workspace_without_user_workspace_description(workspace_guid, club_guid,  user_guid, user_role)

    # Отправка запроса на добавление player к user
    response = add_visible_players_to_user(players_guid, workspace_guid, None, user_guid)
    assert len(response.player_ids) == 1
    assert response.player_ids[0] == players_guid[0]


# test AddVisisblePlayersToUser one player by club_guid
@pytest.mark.smoke
def test_add_visible_players_to_user_by_club_guid():
    club_guid = generate_guid()
    user_guid = generate_guid()
    players_guid = [generate_guid()]
    user_role = roles[2]

    # Создание workspace
    workspace = create_workspace(club_guid)
    # Получение workspace_guid созданного workspace
    workspace_guid = workspace.workspace.workspace_guid.value
    # Добавление user в workspace
    put_user_to_workspace_without_user_workspace_description(workspace_guid, club_guid,  user_guid, user_role)

    # Отправка запроса на добавление player к user
    response = add_visible_players_to_user(players_guid, None, club_guid, user_guid)
    assert len(response.player_ids) == 1
    assert response.player_ids[0] == players_guid[0]


# test AddVisisblePlayersToUser two players
@pytest.mark.smoke
def test_add_visible_players_two_players():
    club_guid = generate_guid()
    user_guid = generate_guid()
    players_count = 2
    players_guid = []
    for i in range(players_count):
        players_guid.append(generate_guid())
    user_role = roles[1]

    # Создание workspace
    workspace = create_workspace(club_guid)
    # Получение workspace_guid созданного workspace
    workspace_guid = workspace.workspace.workspace_guid.value
    # Добавление user в workspace
    put_user_to_workspace_without_user_workspace_description(workspace_guid, club_guid,  user_guid, user_role)

    # Отправка запроса на добавление player к user
    response = add_visible_players_to_user(players_guid, workspace_guid, club_guid, user_guid)

    assert len(response.player_ids) == players_count
    for i in range(len(response.player_ids)):
        assert response.player_ids[i] == players_guid[i], f"error player index: {i}"


# test getUserInWorkspace by_club_guid
@pytest.mark.smoke
def test_get_user_in_workspace_by_workspace():
    club_guid = generate_guid()
    user_guid = generate_guid()
    players_count = 10
    players_guid = []
    for i in range(players_count):
        players_guid.append(generate_guid())
    user_role = roles[1]
    # Создание workspace
    workspace = create_workspace(club_guid)
    # Получение workspace_guid созданного workspace
    workspace_guid = workspace.workspace.workspace_guid.value
    # Добавление user в workspace
    put_user_to_workspace_without_user_workspace_description(workspace_guid, club_guid,  user_guid, user_role)

    # Отправка запроса на добавление player к user
    add_visible_players_to_user(players_guid, workspace_guid, club_guid, user_guid)

    # Отправка запроса на получение юзера
    response = get_user_in_workspace(workspace_guid, None, user_guid)

    assert workspace_guid == response.workspace_guid.value
    assert club_guid == response.club_guid.value
    assert user_guid == response.user_guid.value
    assert response.role_in_workspace == roles.index(user_role)
    assert len(response.visible_player_guids) == players_count
    for i in range(len(response.visible_player_guids)):
        assert response.visible_player_guids[i] in players_guid, f"{response.visible_player_guids[i]} not in players_guid, index: {i}"


# test getUserInWorkspace by_club_guid
@pytest.mark.smoke
def test_get_user_in_workspace_by_workspace():
    club_guid = generate_guid()
    user_guid = generate_guid()
    players_count = 10
    players_guid = []
    for i in range(players_count):
        players_guid.append(generate_guid())
    user_role = roles[1]
    # Создание workspace
    workspace = create_workspace(club_guid)
    # Получение workspace_guid созданного workspace
    workspace_guid = workspace.workspace.workspace_guid.value
    # Добавление user в workspace
    put_user_to_workspace_without_user_workspace_description(workspace_guid, club_guid,  user_guid, user_role)
    # Отправка запроса на добавление player к user
    add_visible_players_to_user(players_guid, workspace_guid, club_guid, user_guid)

    # Отправка запроса на получение юзера - тестируемый запрос
    response = get_user_in_workspace(None, club_guid, user_guid)
    assert workspace_guid == response.workspace_guid.value
    assert club_guid == response.club_guid.value
    assert user_guid == response.user_guid.value
    assert response.role_in_workspace == roles.index(user_role)
    assert len(response.visible_player_guids) == players_count
    for i in range(len(response.visible_player_guids)):
        assert response.visible_player_guids[i] in players_guid, f"{response.visible_player_guids[i]} not in players_guid, index: {i}"


# test getUserWorkspaces one workspace
@pytest.mark.smoke
def test_get_user_workspaces_one_workspace():
    club_guid = generate_guid()
    user_guid = generate_guid()
    players_count = 1
    players_guid = []
    for i in range(players_count):
        players_guid.append(generate_guid())
    user_role = roles[1]
    # Создание workspace
    workspace = create_workspace(club_guid)
    # Получение workspace_guid созданного workspace
    workspace_guid = workspace.workspace.workspace_guid.value
    # Добавление user в workspace
    put_user_to_workspace_without_user_workspace_description(workspace_guid, club_guid,  user_guid, user_role)
    # Отправка запроса на добавление player к user
    add_visible_players_to_user(players_guid, workspace_guid, club_guid, user_guid)

    # Отправка запроса на получение workspaces юзера - тестируемый запрос
    response = get_user_workspaces(user_guid)
    print(response)
    assert workspace_guid == response.user_in_workspaces[0].workspace_guid.value
    assert club_guid == response.user_in_workspaces[0].club_guid.value
    assert user_guid == response.user_in_workspaces[0].user_guid.value
    assert response.user_in_workspaces[0].role_in_workspace == roles.index(user_role)
    assert len(response.user_in_workspaces[0].visible_player_guids) == players_count
    for i in range(len(response.user_in_workspaces[0].visible_player_guids)):
        assert response.user_in_workspaces[0].visible_player_guids[i] in players_guid, f"{response.visible_player_guids[i]} not in players_guid, index: {i}"


# test getUserWorkspaces one workspace
@pytest.mark.smoke
def test_get_user_workspaces_two_workspace():
    user_guid = generate_guid()
    players_count = 1
    workspaces_count = 2
    clubs_guids = []
    players_guid = []
    for i in range(players_count):
        players_guid.append(generate_guid())
    user_role = roles[1]
    # Генерация workspaces_guid's
    for i in range(workspaces_count):
        clubs_guids.append(generate_guid())

    for i in range(workspaces_count):
        # Создание workspace
        workspace = create_workspace(clubs_guids[i])
        # Получение workspace_guid созданного workspace
        workspace_guid = workspace.workspace.workspace_guid.value
        # Добавление user в workspace
        put_user_to_workspace_without_user_workspace_description(workspace_guid, clubs_guids[i],  user_guid, user_role)
        # Отправка запроса на добавление player к user
        add_visible_players_to_user(players_guid, workspace_guid, clubs_guids[i], user_guid)

        # Отправка запроса на получение workspaces юзера - тестируемый запрос
        response = get_user_workspaces(user_guid)
        assert workspace_guid == response.user_in_workspaces[i].workspace_guid.value
        assert clubs_guids[i] == response.user_in_workspaces[i].club_guid.value
        assert user_guid == response.user_in_workspaces[i].user_guid.value
        assert response.user_in_workspaces[i].role_in_workspace == roles.index(user_role)
        assert len(response.user_in_workspaces[i].visible_player_guids) == players_count
        for p in range(len(response.user_in_workspaces[i].visible_player_guids)):
            assert response.user_in_workspaces[i].visible_player_guids[p] in players_guid, f"{response.visible_player_guids[p]} not in players_guid, index: {p}"


# test AddVisisblePlayersToUser добавление уже добавленного player
@pytest.mark.negative
def test_add_visible_players_dublicate_user():
    club_guid = generate_guid()
    user_guid = generate_guid()
    players_guid = []
    player_guid = generate_guid()
    for i in range(2):
        players_guid.append(player_guid)
    user_role = roles[1]
    # Создание workspace
    workspace = create_workspace(club_guid)
    # Получение workspace_guid созданного workspace
    workspace_guid = workspace.workspace.workspace_guid.value
    # Добавление user в workspace
    put_user_to_workspace_without_user_workspace_description(workspace_guid, club_guid,  user_guid, user_role)

    # Отправка запроса на добавление player к user
    response = add_visible_players_to_user(players_guid, workspace_guid, club_guid, user_guid)
    # Распаковка ответа
    status_code = response.code()
    grpc_details = response.details()
    assert status_code.value[0] == 13
    assert grpc_details == "Internal Error. Check service logs"


# test GetWorkspaceWithUsers by workspace_guid
@pytest.mark.smoke
def test_get_workspace_with_users_by_workspace_guid_one_user():
    club_guid = generate_guid()
    user_guid = generate_guid()
    players_guid = []
    player_guid = generate_guid()
    for i in range(2):
        players_guid.append(player_guid)
    user_role = roles[1]
    # Создание workspace
    workspace = create_workspace(club_guid)
    # Получение workspace_guid созданного workspace
    workspace_guid = workspace.workspace.workspace_guid.value
    # Добавление user в workspace
    put_user_to_workspace_without_user_workspace_description(workspace_guid, club_guid,  user_guid, user_role)
    response = get_workspace_with_users(workspace_guid, None)
    print(f"\n{response}\n")
    response_user_guid = response.users[0].user_guid.value
    assert response_user_guid == user_guid
