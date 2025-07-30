from abc import ABCMeta, abstractmethod

from ed_core.application.features.delivery_job.dtos.create_delivery_job_dto import \
    CreateDeliveryJobDto


class ABCCoreRabbitMQSubscriber(metaclass=ABCMeta):
    @abstractmethod
    def create_delivery_job(
        self, create_delivery_job_dto: CreateDeliveryJobDto
    ) -> None: ...
