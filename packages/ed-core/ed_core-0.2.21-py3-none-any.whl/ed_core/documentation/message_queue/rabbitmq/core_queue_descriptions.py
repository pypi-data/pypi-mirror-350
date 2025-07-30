from ed_domain.documentation.message_queue.rabbitmq.abc_queue_descriptions import \
    ABCQueueDescriptions
from ed_domain.documentation.message_queue.rabbitmq.definitions.queue_description import \
    QueueDescription

from ed_core.application.features.delivery_job.dtos.create_delivery_job_dto import \
    CreateDeliveryJobDto
from ed_core.common.generic_helpers import get_config


class CoreQueueDescriptions(ABCQueueDescriptions):
    def __init__(self, connection_url: str) -> None:
        self._config = get_config()
        self._connection_url = connection_url

        self._descriptions: list[QueueDescription] = [
            {
                "name": "create_delivery_job",
                "connection_parameters": {
                    "url": self._connection_url,
                    "queue": "delivery_job",
                },
                "durable": True,
                "request_model": CreateDeliveryJobDto,
            }
        ]

    @property
    def descriptions(self) -> list[QueueDescription]:
        return self._descriptions
