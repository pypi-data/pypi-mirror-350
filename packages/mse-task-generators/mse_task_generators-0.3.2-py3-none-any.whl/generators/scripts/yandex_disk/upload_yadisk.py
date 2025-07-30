from dotenv import load_dotenv
from generators.scripts.yandex_disk.client_wrapper import ClientWrapper


def upload_file_to_yadisk(local_path, filename, token):
    # Загружаем переменные окружения из файла .env
    load_dotenv()
    # Путь на Яндекс.Диске, куда будет загружен файл
    remote_directory_path = "/C_code_generators/"
    # Полный путь к файлу на Яндекс.Диске, включая имя файла
    remote_path = remote_directory_path + filename
    # Создаем экземпляр ClientWrapper для работы с Яндекс.Диском
    if token:
        cw = ClientWrapper(token)
    else:
        cw = ClientWrapper()
    if cw.token_exists:
        # Загружаем файл из локальной файловой системы на Яндекс.Диск
        cw.upload_file_to_disk(local_path, remote_path)
        # Проверяем, существует ли файл по указанному пути
        cw.check_file_exists_on_yadisk(remote_path)
    else:
        print("Невозможно загрузить файл на Яндекс.Диск без токена")



