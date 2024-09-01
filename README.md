Установить зависимости из файла requirements.txt;
Перетащить в папку с проектом *.proto файл;
Выполнить команду в папке с .proto файлом: python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. proto_file_name.proto; 
Для пагинации (если имеется): protoc --python_out=. --proto_path=. Protos/.proto
В файле global_vars.py задать актуальный адрес сервера и порт.
Используемая версия python: 3.12
Файл с запросами: requests.py остальные файлы примеры или зависимости.
Файл с тестами: test_workspace_service.py остальные файлы примеры или зависимости.
