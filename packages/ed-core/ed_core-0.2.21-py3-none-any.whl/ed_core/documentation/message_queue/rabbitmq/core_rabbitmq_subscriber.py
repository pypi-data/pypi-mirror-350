from ed_infrastructure.documentation.message_queue.rabbitmq.rabbitmq_producer import \
    RabbitMQProducer

from ed_core.application.features.delivery_job.dtos.create_delivery_job_dto import \
    CreateDeliveryJobDto
from ed_core.documentation.message_queue.rabbitmq.abc_core_rabbitmq_subscriber import \
    ABCCoreRabbitMQSubscriber
from ed_core.documentation.message_queue.rabbitmq.core_queue_descriptions import \
    CoreQueueDescriptions


class CoreRabbitMQSubscriber(ABCCoreRabbitMQSubscriber):
    def __init__(self, connection_url: str) -> None:
        self._connection_url = connection_url
        self._queues = CoreQueueDescriptions(connection_url)

    def create_delivery_job(
        self, create_delivery_job_dto: CreateDeliveryJobDto
    ) -> None:
        queue = self._queues.get_queue("create_delivery_job")
        producer = RabbitMQProducer[CreateDeliveryJobDto](
            queue["connection_parameters"]["url"],
            queue["connection_parameters"]["queue"],
        )
        producer.start()
        producer.publish(create_delivery_job_dto)
        producer.stop()
