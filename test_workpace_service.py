import pytest
import random
from requests import get_all_workspaces, create_workspace
from requests import (get_workspace, put_user_to_workspace, add_visible_players_to_user,
                      put_user_to_workspace_without_user_workspace_description, get_user_in_workspace,
                      get_user_workspaces, get_workspace_with_users, remove_user_from_workspace,
                      remove_visible_players_from_user)
from functions import generate_guid, generate_workspace_description, random_role
from global_vars import roles


# test CreateWorkspace
@pytest.mark.smoke
def test_create_workspace():
    club_guid = generate_guid()
    response = create_workspace(club_guid)
    assert len(response.workspace.workspace_guid.value) == 36
    assert response.workspace.club_guid.value == club_guid


# test CreateWorkspace без club_guid
@pytest.mark.negative
def test_create_workspace_without_club_guid():
    club_guid = ""
    response = create_workspace(club_guid)
    # Распаковка ответа
    status_code = response.code()
    grpc_details = response.details()
    assert status_code.value[0] == 13
    assert grpc_details == "Internal Error. Check service logs"


# test CreateWorkspace с уже используемым club_guid
@pytest.mark.negative
def test_create_workspace_already_exist_club_guid():
    club_guid = generate_guid()
    # Создание workspace
    create_workspace(club_guid)
    # Создание workspace с уже использванным club_guid
    response = create_workspace(club_guid)
    # Распаковка ответа
    status_code = response.code()
    grpc_details = response.details()
    assert status_code.value[0] == 6
    assert grpc_details == "Object already exists."


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
    response = get_workspace(workspace_guid, None)
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

    response = get_workspace(None, club_guid)
    response_workspace_guid = response.workspace.workspace_guid.value
    response_club_guid = response.workspace.club_guid.value

    assert response_workspace_guid == workspace_guid
    assert response_club_guid == club_guid


# test GetWorkspace с несуществующим workspace_guid
@pytest.mark.negative
def test_get_workspace_workspace_guid_not_exist():
    response = get_workspace(generate_guid(), None)
    # Распаковка ответа
    status_code = response.code()
    grpc_details = response.details()
    assert status_code.value[0] == 5
    assert grpc_details == "Object not found."


# test GetWorkspace с несуществующим workspace_guid
@pytest.mark.negative
def test_get_workspace_club_guid_not_exist():
    response = get_workspace(None, generate_guid())
    # Распаковка ответа
    status_code = response.code()
    grpc_details = response.details()
    assert status_code.value[0] == 5
    assert grpc_details == "Object not found."


# test GetWorkspace без параметров
@pytest.mark.negative
def test_get_workspace_without_params():
    response = get_workspace(None, None)
    print(response)
    # Распаковка ответа
    status_code = response.code()
    grpc_details = response.details()
    assert status_code.value[0] == 13
    assert grpc_details == "Internal Error. Check service logs"


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
def test_put_user_to_workspace_role_manager():
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


# test PutUserToWorkspace by workspace обновление user_role and descr
@pytest.mark.smoke
def test_put_user_to_workspace_user_update_role_and_description():
    club_guid = generate_guid()
    user_guid = generate_guid()
    new_user_role = roles[1]
    user_description = "new description"
    # Создание workspace
    workspace = create_workspace(club_guid)
    # Получение workspace_guid созданного workspace
    workspace_guid = workspace.workspace.workspace_guid.value
    # Добавление юзера в в workspace
    put_user_to_workspace(None, club_guid,  user_guid, roles[2], "")
    # Обновление user в workspace
    response = put_user_to_workspace(None, club_guid,  user_guid, new_user_role, user_description)
    # Распаковка ответа
    response_user_guid = response.user_guid.value
    response_role_in_workspace = response.role_in_workspace
    response_user_workspace_description = response.user_workspace_description
    assert response_user_guid == user_guid
    assert response_user_workspace_description == user_description
    assert response_role_in_workspace == roles.index(new_user_role)


# test PutUserToWorkspace by workspace обновление user_role and descr
@pytest.mark.smoke
def test_put_user_to_workspace_user_update_description():
    club_guid = generate_guid()
    user_guid = generate_guid()
    user_role = roles[1]
    user_description = "new description"
    # Создание workspace
    workspace = create_workspace(club_guid)
    # Получение workspace_guid созданного workspace
    workspace_guid = workspace.workspace.workspace_guid.value
    # Добавление юзера в в workspace
    put_user_to_workspace(None, club_guid,  user_guid, user_role, "Описание")
    # Обновление user в workspace
    response = put_user_to_workspace(None, club_guid,  user_guid, user_role, user_description)
    # Распаковка ответа
    response_user_guid = response.user_guid.value
    response_role_in_workspace = response.role_in_workspace
    response_user_workspace_description = response.user_workspace_description
    assert response_user_guid == user_guid
    assert response_user_workspace_description == user_description
    assert response_role_in_workspace == roles.index(user_role)


# test PutUserToWorkspace by workspace обновление user_role and descr
@pytest.mark.smoke
def test_put_user_to_workspace_user_update_role():
    club_guid = generate_guid()
    user_guid = generate_guid()
    new_user_role = roles[1]
    user_description = "new description"
    # Создание workspace
    workspace = create_workspace(club_guid)
    # Получение workspace_guid созданного workspace
    workspace_guid = workspace.workspace.workspace_guid.value
    # Добавление юзера в в workspace
    put_user_to_workspace(None, club_guid,  user_guid, roles[0], user_description)
    # Обновление user в workspace
    response = put_user_to_workspace(None, club_guid,  user_guid, new_user_role, user_description)
    # Распаковка ответа
    response_user_guid = response.user_guid.value
    response_role_in_workspace = response.role_in_workspace
    response_user_workspace_description = response.user_workspace_description
    assert response_user_guid == user_guid
    assert response_user_workspace_description == user_description
    assert response_role_in_workspace == roles.index(new_user_role)


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
    response = put_user_to_workspace_without_user_workspace_description(None, club_guid,  user_guid, user_role)
    # Распаковка ответа
    response_workspace_guid = response.workspace_guid.value
    response_club_guid = response.club_guid.value
    response_user_guid = response.user_guid.value
    response_role_in_workspace = response.role_in_workspace

    assert response_workspace_guid == workspace_guid
    assert response_club_guid == club_guid
    assert response_user_guid == user_guid
    assert response_role_in_workspace == roles.index(user_role)


# test PutUserToWorkspace добавление user к несуществующему workspace
@pytest.mark.negative
def test_put_user_to_workspace_non_exist_workspace():
    club_guid = generate_guid()
    user_guid = generate_guid()
    user_role = roles[0]
    response = put_user_to_workspace_without_user_workspace_description(None, club_guid,  user_guid, user_role)
    # Распаковка ответа
    status_code = response.code()
    grpc_details = response.details()
    assert status_code.value[0] == 5
    assert grpc_details == "Object not found."


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


# test AddVisisblePlayersToUser one player by workspace_guid user состоит в другом workspace
@pytest.mark.negative
def test_add_visible_players_to_user_another_workspace():
    user_guid = generate_guid()
    players_guid = [generate_guid()]
    user_role = roles[2]

    # Создание workspace в который будет добавлен user
    workspace_a = create_workspace(generate_guid())
    # Создание workspace в который будет добавляться player
    workspace_b = create_workspace(generate_guid())
    # Получение workspace_guid созданного workspace в который будет добавлен user
    workspace_guid_a = workspace_a.workspace.workspace_guid.value
    workspace_guid_b = workspace_b.workspace.workspace_guid.value
    # Добавление user в workspace_a
    put_user_to_workspace_without_user_workspace_description(workspace_guid_a, None,  user_guid, user_role)

    # Отправка запроса на добавление player к user состоящем в другом workspace
    response = add_visible_players_to_user(players_guid, workspace_guid_b, None, user_guid)
    # Распаковка ответа
    status_code = response.code()
    grpc_details = response.details()
    assert status_code.value[0] == 5
    assert grpc_details == "User not found in workspace."


# test AddVisisblePlayersToUser without players by workspace_guid
@pytest.mark.smoke
def test_add_visible_players_to_user_without_players():
    club_guid = generate_guid()
    user_guid = generate_guid()
    players_guid = []
    user_role = roles[2]

    # Создание workspace
    workspace = create_workspace(club_guid)
    # Получение workspace_guid созданного workspace
    workspace_guid = workspace.workspace.workspace_guid.value
    # Добавление user в workspace
    put_user_to_workspace_without_user_workspace_description(workspace_guid, None,  user_guid, user_role)

    # Отправка запроса на добавление player к user
    response = add_visible_players_to_user(players_guid, workspace_guid, None, user_guid)
    assert len(response.player_ids) == 0


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
    response = add_visible_players_to_user(players_guid, workspace_guid, None, user_guid)

    assert len(response.player_ids) == players_count
    for i in range(len(response.player_ids)):
        assert response.player_ids[i] == players_guid[i], f"error player index: {i}"


# test AddVisisblePlayersToUser игрок добавлен разным user'ам
@pytest.mark.smoke
def test_dd_visible_players_different_users():
    count = 2
    user_guids = [generate_guid() for u in range(count)]
    user_role = roles[random.randint(0, len(roles)-1)]
    players_guids = [generate_guid() for p in range(count)]
    workspaces = []
    workspaces_guids = []
    # Блок когда отвечающий за добавление player_guid'ов r user'ам
    for i in range(count):
        # Создание workspaces
        workspaces.append(create_workspace(generate_guid()))
        # Получение guid созданных workspaces
        workspaces_guids.append(workspaces[i].workspace.workspace_guid.value)
        # Добавление user в workspace
        put_user_to_workspace_without_user_workspace_description(workspaces_guids[i], None,  user_guids[i], user_role)
        # Добавление player к игроку
        response = add_visible_players_to_user(players_guids, workspaces_guids[i], None, user_guids[i])
        # Ответ содержит переданный player_guid
        assert response.player_ids[i] in players_guids

    # Получение информации о user в workspace
    for i in range(count):
        user_in_workspace = get_user_in_workspace(workspaces_guids[i], None, user_guids[i])
        # player_guid есть в списке visible_player_guids user'a
        assert user_in_workspace.visible_player_guids[i] in players_guids



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


# test getUserInWorkspace by club_guid
@pytest.mark.smoke
def test_get_user_in_workspace_by_club_guid():
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


# test getUserInWorkspace user состоит в другом workspace
@pytest.mark.negative
def test_get_user_in_workspace_by_user_from_another_workspace():
    user_guid_b = generate_guid()
    players_count = 1
    players_guid = []
    for i in range(players_count):
        players_guid.append(generate_guid())
    user_role = roles[1]
    workspaces = []
    for i in range(2):
        workspaces.append(generate_guid())
    # Создание workspace в который будет помещен user
    workspace_a = create_workspace(workspaces[0])
    # Создание workspace который будет передан в запрос
    workspace_b = create_workspace(workspaces[1])
    # Получение workspace_guid созданного workspace_a
    workspace_guid_a = workspace_a.workspace.workspace_guid.value
    # Получение workspace_guid  который будет запрошен
    workspace_guid_b = workspace_b.workspace.workspace_guid.value
    # Добавление user в workspace_b
    put_user_to_workspace_without_user_workspace_description(workspace_guid_b, None,  user_guid_b, user_role)
    # Отправка запроса на добавление player к user в workspace_b
    add_visible_players_to_user(players_guid, workspace_guid_b, None, user_guid_b)
    # Отправка запроса на получение юзера
    response = get_user_in_workspace(workspace_guid_a, None, user_guid_b)
    # Распаковка ответа
    status_code = response.code()
    grpc_details = response.details()
    assert status_code.value[0] == 5
    assert grpc_details == "Object not found."


# test getUserInWorkspace user_guid не передан
@pytest.mark.negative
def test_get_user_in_workspace_without_user_guid():
    # Создание workspace в который будет помещен user
    workspace = create_workspace(generate_guid())
    # Получение workspace_guid созданного workspace
    workspace_guid = workspace.workspace.workspace_guid.value
    # Отправка запроса на получение юзера
    response = get_user_in_workspace(workspace_guid, None, "")
    # Распаковка ответа
    status_code = response.code()
    grpc_details = response.details()
    assert status_code.value[0] == 13
    assert grpc_details == "Internal Error. Check service logs"


# test getUserInWorkspace передан user_guid не состоящий ни в одном workspace
@pytest.mark.negative
def test_get_user_in_workspace_non_exist_user():
    club_guid = generate_guid()
    user_guid = generate_guid()
    # Создание workspace
    create_workspace(club_guid)

    # Отправка запроса на получение юзера - тестируемый запрос
    response = get_user_in_workspace(None, club_guid, user_guid)
    # Распаковка ответа
    status_code = response.code()
    grpc_details = response.details()
    assert status_code.value[0] == 5
    assert grpc_details == "Object not found."


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
    assert workspace_guid == response.user_in_workspaces[0].workspace_guid.value
    assert club_guid == response.user_in_workspaces[0].club_guid.value
    assert user_guid == response.user_in_workspaces[0].user_guid.value
    assert response.user_in_workspaces[0].role_in_workspace == roles.index(user_role)
    assert len(response.user_in_workspaces[0].visible_player_guids) == players_count
    for i in range(len(response.user_in_workspaces[0].visible_player_guids)):
        assert response.user_in_workspaces[0].visible_player_guids[i] in players_guid, f"{response.visible_player_guids[i]} not in players_guid, index: {i}"


# test getUserWorkspaces user_guid = null
@pytest.mark.negative
def test_get_user_workspaces_one_workspace():
    user_guid = ""

    # Отправка запроса на получение workspaces юзера - тестируемый запрос
    response = get_user_workspaces(user_guid)
    # Распаковка ответа
    status_code = response.code()
    grpc_details = response.details()
    assert status_code.value[0] == 13
    assert grpc_details == "Internal Error. Check service logs"


# test getUserWorkspaces without workspace(s)
@pytest.mark.smoke
def test_get_user_workspaces_without_workspaces():
    user_guid = generate_guid()

    # Отправка запроса на получение workspaces юзера - тестируемый запрос
    response = get_user_workspaces(user_guid)

    assert len(str(response)) == 0


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
def test_add_visible_players_dublicate_player():
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
    user_role = roles[1]
    # Создание workspace
    workspace = create_workspace(club_guid)
    # Получение workspace_guid созданного workspace
    workspace_guid = workspace.workspace.workspace_guid.value
    # Добавление user в workspace
    put_user_to_workspace_without_user_workspace_description(workspace_guid, club_guid,  user_guid, user_role)

    # Отправка тестируемого запроса
    response = get_workspace_with_users(workspace_guid, None)

    assert response.users[0].user_guid.value == user_guid
    assert response.users[0].role_in_workspace == roles.index(user_role)
    assert response.users[0].workspace_guid.value == workspace_guid
    assert response.users[0].club_guid.value == club_guid
    assert response.workspace.workspace_guid.value == workspace_guid
    assert response.workspace.club_guid.value == club_guid


# test GetWorkspaceWithUsers by club_guid
@pytest.mark.smoke
def test_get_workspace_with_users_by_club_guid_one_user():
    club_guid = generate_guid()
    user_guid = generate_guid()
    user_role = roles[1]
    # Создание workspace
    workspace = create_workspace(club_guid)
    # Получение workspace_guid созданного workspace
    workspace_guid = workspace.workspace.workspace_guid.value
    # Добавление user в workspace
    put_user_to_workspace_without_user_workspace_description(workspace_guid, club_guid,  user_guid, user_role)

    # Отправка тестируемого запроса
    response = get_workspace_with_users(None, club_guid)

    assert response.users[0].user_guid.value == user_guid
    assert response.users[0].role_in_workspace == roles.index(user_role)
    assert response.users[0].workspace_guid.value == workspace_guid
    assert response.users[0].club_guid.value == club_guid
    assert response.workspace.workspace_guid.value == workspace_guid
    assert response.workspace.club_guid.value == club_guid


# test GetWorkspaceWithUsers by club_guid
@pytest.mark.smoke
def test_get_workspace_without_users():
    club_guid = generate_guid()
    user_guid = generate_guid()
    # Создание workspace
    workspace = create_workspace(club_guid)
    # Получение workspace_guid созданного workspace
    workspace_guid = workspace.workspace.workspace_guid.value

    # Отправка тестируемого запроса
    response = get_workspace_with_users(None, club_guid)
    assert "users" not in str(response)


# test GetWorkspaceWithUsers two users
@pytest.mark.smoke
def test_get_workspace_with_users_two_user():
    club_guid = generate_guid()
    users_guids = []
    for i in range(2):
        users_guids.append(generate_guid())
    user_role = roles[1]
    # Создание workspace
    workspace = create_workspace(club_guid)
    # Получение workspace_guid созданного workspace
    workspace_guid = workspace.workspace.workspace_guid.value
    # Добавление user в workspace
    for user in users_guids:
        put_user_to_workspace_without_user_workspace_description(workspace_guid, club_guid,  user, user_role)

    # Отправка тестируемого запроса
    response = get_workspace_with_users(workspace_guid, None)

    for user in range(len(response.users)):
        assert response.users[user].user_guid.value in users_guids
        assert response.users[user].role_in_workspace == roles.index(user_role)
        assert response.users[user].workspace_guid.value == workspace_guid
        assert response.users[user].club_guid.value == club_guid
        assert response.workspace.workspace_guid.value == workspace_guid
        assert response.workspace.club_guid.value == club_guid


# test removeUserFromWorkspace by club_guid
@pytest.mark.smoke
def test_remove_user_from_workspace_by_workspace_guid():
    club_guid = generate_guid()
    user_guid = generate_guid()
    user_role = roles[1]

    # Создание workspace
    workspace = create_workspace(club_guid)
    # Получение workspace_guid созданного workspace
    workspace_guid = workspace.workspace.workspace_guid.value
    # Добавление user в workspace
    put_user_to_workspace_without_user_workspace_description(workspace_guid, None,  user_guid, user_role)

    # Отправка тестируемого запроса
    response = remove_user_from_workspace(workspace_guid, None, user_guid)
    assert response == 0


# test removeUserFromWorkspace удаление несуществующего user
@pytest.mark.negative
def test_remove_user_from_workspace_no_exist_user():
    club_guid = generate_guid()
    user_guid = generate_guid()

    # Создание workspace
    workspace = create_workspace(club_guid)
    # Получение workspace_guid созданного workspace
    workspace_guid = workspace.workspace.workspace_guid.value

    # Отправка тестируемого запроса
    response = remove_user_from_workspace(workspace_guid, None, user_guid)
    assert len(str(response)) != 0


# test removeUserFromWorkspace удаление user из другого workspace
@pytest.mark.smoke
def test_remove_user_from_workspace_another_workspace_guid():
    count = 2
    user_guids = [generate_guid() for i in range(count)]
    user_role = roles[random.randint(0, len(roles)-1)]
    workspaces = []
    workspaces_guids = []
    for i in range(count):
        workspaces.append(create_workspace(generate_guid()))
        workspaces_guids.append(workspaces[i].workspace.workspace_guid.value)
        # Добавление user в workspace
        put_user_to_workspace_without_user_workspace_description(workspaces_guids[i], None,  user_guids[i], user_role)
    # Получение workspace guid которого был передан в запрос
    get_workspace = get_workspace_with_users(workspaces_guids[1], None)
    # Получение workspace guid которого был передан в запрос
    assert get_workspace.users[0].user_guid.value == user_guids[1]
    # Отправка тестируемого запроса
    response = remove_user_from_workspace(workspaces_guids[0], None, user_guids[1])
    assert len(str(response)) != 0


# test removeUserFromWorkspace by club_guid
@pytest.mark.smoke
def test_remove_user_from_workspace_by_club_guid():
    club_guid = generate_guid()
    user_guid = generate_guid()
    user_role = roles[1]

    # Создание workspace
    workspace = create_workspace(club_guid)
    # Получение workspace_guid созданного workspace
    workspace_guid = workspace.workspace.workspace_guid.value
    # Добавление user в workspace
    put_user_to_workspace_without_user_workspace_description(workspace_guid, None,  user_guid, user_role)

    # Отправка тестируемого запроса
    response = remove_user_from_workspace(None, club_guid, user_guid)
    assert len(response) == 0


# test removeVisiblePlayerFromUser one player by club_guid
@pytest.mark.smoke
def test_remove_visible_players_from_user_by_club_guid_one_player():
    club_guid = generate_guid()
    user_guid = generate_guid()
    user_role = roles[1]
    players_guids = []
    for i in range(1):
        players_guids.append(generate_guid())
    # Создание workspace
    workspace = create_workspace(club_guid)
    # Получение workspace_guid созданного workspace
    workspace_guid = workspace.workspace.workspace_guid.value
    # Добавление user в workspace
    put_user_to_workspace_without_user_workspace_description(workspace_guid, None,  user_guid, user_role)
    # Добавление player к игроку
    add_visible_players_to_user(players_guids, workspace_guid, club_guid, user_guid)

    # Отправка тестируемого запроса
    response = remove_visible_players_from_user(None, club_guid, user_guid, players_guids)
    assert len(response) == 0


# test removeVisiblePlayerFromUser two players by workspace_guid
@pytest.mark.smoke
def test_remove_visible_players_from_user_by_workspace_guid_two_player():
    club_guid = generate_guid()
    user_guid = generate_guid()
    user_role = roles[1]
    players_guids = []
    for i in range(2):
        players_guids.append(generate_guid())
    # Создание workspace
    workspace = create_workspace(club_guid)
    # Получение workspace_guid созданного workspace
    workspace_guid = workspace.workspace.workspace_guid.value
    # Добавление user в workspace
    put_user_to_workspace_without_user_workspace_description(workspace_guid, None,  user_guid, user_role)
    # Добавление player к игроку
    add_visible_players_to_user(players_guids, workspace_guid, club_guid, user_guid)

    # Отправка тестируемого запроса
    response = remove_visible_players_from_user(workspace_guid, None, user_guid, players_guids)
    assert len(response) == 0


# test removeVisiblePlayerFromUser 2/4 players by club_guid
@pytest.mark.smoke
def test_remove_visible_players_from_user_by_workspace_guid_two_player():
    club_guid = generate_guid()
    user_guid = generate_guid()
    user_role = roles[1]
    players_guids = []
    for i in range(4):
        players_guids.append(generate_guid())
    deleted_player = [players_guids[0],players_guids[3]]
    # Создание workspace
    workspace = create_workspace(club_guid)
    # Получение workspace_guid созданного workspace
    workspace_guid = workspace.workspace.workspace_guid.value
    # Добавление user в workspace
    put_user_to_workspace_without_user_workspace_description(workspace_guid, None,  user_guid, user_role)
    # Добавление player к игроку
    add_visible_players_to_user(players_guids, workspace_guid, club_guid, user_guid)
    # Отправка тестируемого запроса
    get_workspace_with_users(workspace_guid, None)
    response = remove_visible_players_from_user(None, club_guid, user_guid, deleted_player)
    workspace_after_delete_player = get_workspace_with_users(workspace_guid, None)
    players_in_workspace = workspace_after_delete_player.users[0].visible_player_guids

    assert len(response) == 0
    assert len(players_in_workspace) == 2
    for i in range(len(deleted_player)):
        assert deleted_player[i] not in players_in_workspace


# test removeVisiblePlayerFromUser удаление всех player'ов у user
@pytest.mark.smoke
def test_remove_visible_players_from_user_all_player():
    club_guid = generate_guid()
    user_guid = generate_guid()
    user_role = roles[1]
    players_guids = []
    for i in range(2):
        players_guids.append(generate_guid())
    # Создание workspace
    workspace = create_workspace(club_guid)
    # Получение workspace_guid созданного workspace
    workspace_guid = workspace.workspace.workspace_guid.value
    # Добавление user в workspace
    put_user_to_workspace_without_user_workspace_description(workspace_guid, None,  user_guid, user_role)
    # Добавление player к игроку
    add_visible_players_to_user(players_guids, workspace_guid, club_guid, user_guid)
    # Отправка тестируемого запроса
    response = remove_visible_players_from_user(None, club_guid, user_guid, players_guids)
    # Получение user после удаления игроков
    workspace_after_delete_player = get_workspace_with_users(workspace_guid, None)
    # Получение оставшихся игроков
    players_in_workspace = workspace_after_delete_player.users[0].visible_player_guids

    assert len(response) == 0
    assert len(players_in_workspace) == 0
    assert players_guids not in players_in_workspace


# test removeVisiblePlayerFromUser player_guids не переданы
@pytest.mark.smoke
def test_remove_visible_players_from_user_without_players():
    club_guid = generate_guid()
    user_guid = generate_guid()
    user_role = roles[1]
    players_guids = []
    players_count = 2
    for i in range(players_count):
        players_guids.append(generate_guid())
    # Создание workspace
    workspace = create_workspace(club_guid)
    # Получение workspace_guid созданного workspace
    workspace_guid = workspace.workspace.workspace_guid.value
    # Добавление user в workspace
    put_user_to_workspace_without_user_workspace_description(workspace_guid, None,  user_guid, user_role)
    # Добавление player к игроку
    add_visible_players_to_user(players_guids, workspace_guid, club_guid, user_guid)
    # Отправка тестируемого запроса
    response = remove_visible_players_from_user(None, club_guid, user_guid, [])
    # Получение user после удаления игроков
    workspace_after_delete_player = get_workspace_with_users(workspace_guid, None)
    # Получение оставшихся игроков
    players_in_workspace = workspace_after_delete_player.users[0].visible_player_guids
    assert len(players_in_workspace) == players_count
    for i in range(players_count):
        assert players_guids[i] in players_in_workspace


# test removeVisiblePlayerFromUser player_guids передан guid несуществующего player
@pytest.mark.negative
def test_remove_visible_players_from_user_no_exist_player_guid():
    club_guid = generate_guid()
    user_guid = generate_guid()
    user_role = roles[1]
    players_guids = []
    players_count = 2
    for i in range(players_count):
        players_guids.append(generate_guid())
    # Создание workspace
    workspace = create_workspace(club_guid)
    # Получение workspace_guid созданного workspace
    workspace_guid = workspace.workspace.workspace_guid.value
    # Добавление user в workspace
    put_user_to_workspace_without_user_workspace_description(workspace_guid, None,  user_guid, user_role)
    # Добавление player к игроку
    add_visible_players_to_user(players_guids, workspace_guid, club_guid, user_guid)
    # Отправка тестируемого запроса
    response = remove_visible_players_from_user(None, club_guid, user_guid, [generate_guid()])

    assert len(str(response)) != 0


# test removeVisiblePlayerFromUser удаление player другого игрока
@pytest.mark.negative
def test_remove_visible_players_from_user_different_user():
    count = 2
    user_guids = [generate_guid() for u in range(count)]
    user_role = roles[random.randint(0, len(roles)-1)]
    players_guids = [generate_guid() for p in range(count)]
    unique_player_guid = [generate_guid()]
    workspaces = []
    workspaces_guids = []
    for i in range(count):
        # Создание workspaces
        workspaces.append(create_workspace(generate_guid()))
        # Получение guid созданных workspaces
        workspaces_guids.append(workspaces[i].workspace.workspace_guid.value)
        # Добавление user в workspace
        put_user_to_workspace_without_user_workspace_description(workspaces_guids[i], None,  user_guids[i], user_role)
        # Добавление player к игроку
        add_visible_players_to_user(players_guids, workspaces_guids[i], None, user_guids[i])

    # Добавление уникального игрока к одному из user
    add_visible_players_to_user(unique_player_guid, workspaces_guids[0], None, user_guids[0])
    # Отправка тестируемого запроса
    response = remove_visible_players_from_user(workspaces_guids[1], None, user_guids[1], unique_player_guid)

    # Получение workspace c уникальным player_guid
    workspace_with_unique_player_id = get_workspace_with_users(workspaces_guids[0], None)
    # player_guid не удален если передан несоответствующий workspace_guid
    assert len(workspace_with_unique_player_id.users[0].visible_player_guids) == count+1

    # Получение workspace без уникального player_guid
    workspace_without_unique_player_id = get_workspace_with_users(workspaces_guids[1], None)
    # Список player_guid не изменился
    assert len(workspace_without_unique_player_id.users[0].visible_player_guids) == count

    assert len(str(response)) != 0
