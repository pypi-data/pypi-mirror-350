from zsynctech_maestro_sdk.interfaces.broker import MessageBrokerInterface
from zsynctech_maestro_sdk.models.execution import ExecutionModel
from zsynctech_maestro_sdk.models.step import StepModel
from zsynctech_maestro_sdk.models.task import TaskModel
from retry import retry
from typing import Type


class MaestroSDK:

    def __init__(self, broker: MessageBrokerInterface):
        """
        Initialize the MaestroSDK with a message broker.

        :param broker: An instance of a class that implements the MessageBrokerInterface.
        :type broker: MessageBrokerInterface
        :raises ValueError: If the broker is not an instance of MessageBrokerInterface.
        """
        self.broker = broker
        self.instance_id = broker.instance_id
        self.__execution: ExecutionModel = ExecutionModel()
        self.__step: StepModel = StepModel()
        self.__task: TaskModel = TaskModel()

    @property
    def step(self) -> StepModel:
        return self.__step
    
    @step.setter
    def step(self, step: StepModel):
        if not isinstance(step, StepModel):
            raise ValueError("step must be an instance of StepModel")
        self.__step = step

    @property
    def execution(self) -> ExecutionModel:
        return self.__execution

    @execution.setter
    def execution(self, execution: ExecutionModel):
        if not isinstance(execution, ExecutionModel):
            raise ValueError("execution must be an instance of ExecutionModel")
        self.__execution = execution

    @property
    def task(self) -> TaskModel:
        return self.__task

    @task.setter
    def task(self, task: TaskModel):
        if not isinstance(task, TaskModel):
            raise ValueError("task must be an instance of TaskModel")
        self.__task = task

    def send_step(self) -> None:
        self.broker.publish(self.step.model_dump(), self.broker.routing_key_task_step)

    def send_task(self) -> None:
        self.broker.publish(self.task.model_dump(), self.broker.routing_key_task)
    
    def send_execution(self) -> None:
        self.broker.publish(self.execution.model_dump(), self.broker.routing_key_executions)

    @retry(tries=3, delay=2)
    def listener(self, callback) -> None:
        self.broker.consume(
            queue_name=self.broker.start_queue_name,
            callback=callback
        )
