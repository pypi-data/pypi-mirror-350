from abc import ABC, abstractmethod

class BaseTaskManager(ABC):
    @abstractmethod

    # на данный момент этот метод не востребован
    # def set_settings(self, settings):
    #     """Задать настройки для задач."""
    #     pass

    @abstractmethod
    def create_task():
        """Создать задачу с определенными деталями."""
        pass

    # на данный момент этот метод не востребован
    # @abstractmethod
    # def set_verification_settings(self, verification_settings):
    #     """Задать настройки проверки задачи (под вопросом)."""
    #     pass

    @abstractmethod
    def verify_task():
        """Проверить задачу на основе заданных настроек проверки."""
        pass