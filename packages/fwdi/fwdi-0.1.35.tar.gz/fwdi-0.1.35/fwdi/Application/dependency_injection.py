from ..Application.Abstractions.base_task_handler import BaseTaskHandler
from ..Application.TaskHandler.task_handler import TaskHandler
from .Usecase.user_repository import UserRepositoryFWDI

from ..Application.Abstractions.base_task_callback_handler import BaseTaskCallbackHandler
from ..Application.Abstractions.base_user_repository import BaseUserRepositoryFWDI
from ..Application.Abstractions.base_service_collection import BaseServiceCollectionFWDI


from ..Application.TaskCallback.task_callback_handler import TaskCallbackHandler

class DependencyInjection():

    @staticmethod
    def AddApplication(services:BaseServiceCollectionFWDI)->None:
        from ..Application.Abstractions.base_task_queue_manager import BaseTaskQueueManager
        from ..Application.TaskManager.task_queue_manager import TaskQueueManager

        services.AddTransient(BaseUserRepositoryFWDI, UserRepositoryFWDI)
        services.AddSingleton(BaseTaskQueueManager, TaskQueueManager)
        services.AddTransient(BaseTaskCallbackHandler, TaskCallbackHandler)
        services.AddSingleton(BaseTaskHandler, TaskHandler)