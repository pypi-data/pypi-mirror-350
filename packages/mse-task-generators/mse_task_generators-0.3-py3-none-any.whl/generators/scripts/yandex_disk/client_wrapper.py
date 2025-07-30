import os
import yadisk


class ClientWrapper:
    """Обертка для работы с Яндекс.Диском."""

    def __init__(self, api_token=None):
        """
        Инициализация экземпляра ClientWrapper.

        :param api_token: Токен API для доступа к Яндекс.Диску. Если не указан, 
                          будет загружен из переменной окружения 'YADISK_TOKEN'.
        """
        # Устанавливаем токен API: если он передан, используем его, иначе загружаем из окружения
        self.api_token = api_token if api_token else os.getenv('YADISK_TOKEN')
        # Создаем клиент Яндекс.Диска с использованием токена
        self.client = yadisk.Client(token=self.api_token)
        # Существует ли токен
        self.token_exists = True if self.api_token else False

    def upload_file_to_disk(self, local_path, remote_path, overwrite=True):
        """
        Загружает файл с локального пути на Яндекс.Диск.

        :param local_path: Путь к локальному файлу, который нужно загрузить.
        :param remote_path: Путь на Яндекс.Диске, куда будет загружен файл.
        :param overwrite: Флаг, указывающий, следует ли перезаписывать файл, 
                          если он уже существует на Яндекс.Диске.
        :return: Результат загрузки файла.
        """
        # Загружаем файл на Яндекс.Диск и возвращаем результат
        return self.client.upload(local_path, remote_path, overwrite=overwrite)

    def check_file_exists_on_yadisk(self, remote_path):
        """
        Проверяет наличие файла на Яндекс.Диске.

        :param remote_path: Путь к файлу на Яндекс.Диске.
        :exists(remote_path): True, если файл существует, иначе False.
        """
        # Проверяем, существует ли файл по указанному пути
        if self.client.exists(remote_path):
            print("Исполняемый файл успешно загружен на Яндекс.Диск")
        else:
            print("Ошибка: файл не загружен на Яндекс.Диск")

    def download_file_from_disk(self, remote_path, local_path, overwrite=True):
        """
        Скачивает файл с Яндекс.Диска на локальный компьютер.

        :param remote_path: Путь к файлу на Яндекс.Диске.
        :param local_path: Локальный путь для сохранения файла.
        :param overwrite: Если True, перезаписывает существующий локальный файл. 
                        Если False и файл существует - пропускает загрузку.
        :raises Exception: Если файл не существует на Яндекс.Диске.
        """
        if not self.client.exists(remote_path):
            raise Exception(f"Исполняемый файл '{remote_path}' не найден на Яндекс.Диске")

        # Если файл существует локально и overwrite=False - пропускаем загрузку
        if os.path.exists(local_path) and not overwrite:
            print(f"Исполняемый файл '{local_path}' уже существует. Загрузка пропущена (overwrite=False).")
            return

        # Скачиваем файл (автоматически перезаписывает, если overwrite=True)
        self.client.download(remote_path, local_path)
        print(f"Исполняемый файл успешно скачан: {local_path}")

