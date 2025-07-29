from abc import ABC, abstractmethod


class MessageBrokerInterface(ABC):
    amqp_url: str
    instance_id:str
    routing_key_executions:str
    routing_key_task_step:str
    routing_key_task:str
    exchange_name:str

    @abstractmethod
    def queue_bind(self, queue_name: str, routing_key: str) -> None: ...

    @abstractmethod
    def declare_queue(self, queue_name: str, durable: bool) -> None: ...

    @abstractmethod
    def publish(self, data: dict, key: str) -> None: ...

    @abstractmethod
    def _connect(self) -> None: ...

    @abstractmethod
    def close(self) -> None: ...

    @abstractmethod
    def consume(self, queue_name: str, callback) -> None: ...
