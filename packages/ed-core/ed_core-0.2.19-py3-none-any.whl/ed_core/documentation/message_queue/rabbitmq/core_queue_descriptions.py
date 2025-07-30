from ed_domain.documentation.message_queue.rabbitmq.abc_queue_descriptions import \
    ABCQueueDescriptions
from ed_domain.documentation.message_queue.rabbitmq.definitions.queue_description import \
    QueueDescription

from ed_core.application.features.delivery_job.dtos.create_delivery_job_dto import \
    CreateDeliveryJobDto


class CoreQueueDescriptions(ABCQueueDescriptions):
    def __init__(self, connection_url: str) -> None:
        self._descriptions: list[QueueDescription] = [
            {
                "name": "delivery_job",
                "connection_url": connection_url,
                "durable": True,
                "request_model": CreateDeliveryJobDto,
            }
        ]

    @property
    def descriptions(self) -> list[QueueDescription]:
        return self._descriptions
