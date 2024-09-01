1. Установить зависимости из файла requirements.txt Используемая версия python: 3.12;
2. Перетащить в папку с проектом *.proto файл;
3. Выполнить команду в папке с .proto файлом: python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. proto_file_name.proto; 
3.1. Для пагинации (если имеется): protoc --python_out=. --proto_path=. Protos/.proto
4. В файле global_vars.py задать актуальный адрес сервера и порт.
5. Файл с запросами: requests.py остальные файлы примеры или зависимости.
6. Файл с тестами: test_workspace_service.py остальные файлы примеры или зависимости.
