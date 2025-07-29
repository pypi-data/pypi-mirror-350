from zsynctech_maestro_sdk.interfaces.broker import MessageBrokerInterface
from pika.adapters.blocking_connection import BlockingChannel
from pika import BlockingConnection, URLParameters, BasicProperties
from typing import Optional, Dict
import json


ROUTING_KEY_EXECUTIONS = "executions.key"
ROUTING_KEY_TASK_STEP = "task.steps.key"
ROUTING_KEY_TASK = "tasks.key"
EXCHANGE_NAME = "amq.topic"


class RabbitMQ(MessageBrokerInterface):
    def __init__(self, amqp_url: str, instance_id:str):
        self.__amqp_url = amqp_url
        self.__instance_id = instance_id
        self.__exchange_name = EXCHANGE_NAME
        self.__routing_key_executions = ROUTING_KEY_EXECUTIONS
        self.__routing_key_task_step = ROUTING_KEY_TASK_STEP
        self.__routing_key_task = ROUTING_KEY_TASK
        self.__connection: Optional[BlockingConnection] = None
        self.__channel: Optional[BlockingChannel] = None
        self._connect()
        self.declare_queue(queue_name=self.start_queue_name, durable=True)
        self.queue_bind(queue_name=self.start_queue_name,routing_key=self.execution_binding_key)

    @property
    def exchange_name(self) -> str:
        return self.__exchange_name

    @property
    def routing_key_executions(self) -> str:
        return self.__routing_key_executions
    
    @property
    def routing_key_task_step(self) -> str:
        return self.__routing_key_task_step
    
    @property
    def routing_key_task(self) -> str:
        return self.__routing_key_task
    
    @property
    def instance_id(self) -> str:
        return self.__instance_id
    
    @instance_id.setter
    def instance_id(self, value: str) -> None:
        if not isinstance(value, str):
            raise ValueError("Instance ID must be a string")
        self.__instance_id = value

    @property
    def amqp_url(self) -> str:
        return self.__amqp_url
    
    @amqp_url.setter
    def amqp_url(self, value: str) -> None:
        if not isinstance(value, str):
            raise ValueError("AMQP URL must be a string")
        self.__amqp_url = value

    @property
    def channel(self) -> Optional[BlockingChannel]:
        return self.__channel

    @channel.setter
    def channel(self, value: Optional[BlockingChannel]) -> None:
        if not isinstance(value, (BlockingChannel, type(None))):
            raise ValueError("Channel must be a BlockingChannel or None")
        self.__channel = value

    @property
    def connection(self) -> Optional[BlockingConnection]:
        return self.__connection
  
    @connection.setter
    def connection(self, value: Optional[BlockingConnection]) -> None:
        if not isinstance(value, (BlockingConnection, type(None))):
            raise ValueError("Connection must be a BlockingConnection or None")
        self.__connection = value

    @property
    def amqp_url(self) -> str:
        return self.__amqp_url

    @amqp_url.setter
    def amqp_url(self, value: str) -> None:
        if not isinstance(value, str):
            raise ValueError("AMQP URL must be a string")
        self.__amqp_url = value

    @property
    def start_queue_name(self) -> str:
        return f"start_{self.instance_id}"
    
    @property
    def execution_binding_key(self) -> str:
        return f'execution_{self.instance_id}'
    
    @property
    def execution_queue_name(self) -> str:
        return f"execution_{self.instance_id}"

    def queue_bind(self, queue_name, routing_key) -> None:
        if self.channel is None:
            self._connect()
        self.channel.queue_bind(exchange=self.exchange_name, queue=queue_name, routing_key=routing_key)
        print(f" [*] Queue '{queue_name}' bound to exchange '{self.exchange_name}' with routing key '{routing_key}'")

    def declare_queue(self, queue_name: str, durable: bool) -> None:
        if self.channel is None:
            self._connect()
        self.channel.queue_declare(queue=queue_name, durable=durable)
        print(f" [*] Queue '{queue_name}' bound to exchange '{self.exchange_name}'")

    def _connect(self):
        if self.connection is None:
            self.connection = BlockingConnection(URLParameters(self.amqp_url))

        if self.channel is None:
            self.channel = self.connection.channel()

    def publish(self, data: Dict, key: str) -> None:

        MESSAGE_JSON = json.dumps(data)

        self.channel.basic_publish(
            exchange=self.exchange_name, 
            routing_key=key,
            body=MESSAGE_JSON,
            properties=BasicProperties(
                content_type="application/json"
            )
        )

        print(f" [x] Sent '{MESSAGE_JSON}' with routing key '{key}'")

    def close(self) -> None: ...

    def consume(self, queue_name: str, callback) -> None:
        if self.channel is None:
            self._connect()
        self.channel.basic_consume(
            queue=queue_name,
            on_message_callback=callback,
            auto_ack=True
        )
        print(f" [*] Waiting for messages in queue '{queue_name}'. To exit press CTRL+C")
        self.channel.start_consuming()