from ed_domain.common.exceptions import ApplicationException, Exceptions
from ed_domain.core.entities.delivery_job import DeliveryJobStatus
from ed_domain.core.repositories.abc_unit_of_work import ABCUnitOfWork
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_core.application.common.responses.base_response import BaseResponse
from ed_core.application.features.common.dtos import TrackOrderDto
from ed_core.application.features.order.requests.queries import TrackOrderQuery


@request_handler(TrackOrderQuery, BaseResponse[TrackOrderDto])
class TrackOrderQueryHandler(RequestHandler):
    def __init__(self, uow: ABCUnitOfWork):
        self._uow = uow

    async def handle(self, request: TrackOrderQuery) -> BaseResponse[TrackOrderDto]:
        if order := self._uow.order_repository.get(id=request.order_id):
            if "delivery_job_id" not in order:
                return BaseResponse[TrackOrderDto].success(
                    "Order fetched successfully.",
                    TrackOrderDto.from_entities(
                        order,
                        self._uow,
                    ),
                )

            delivery_job = self._uow.delivery_job_repository.get(
                id=order["delivery_job_id"]
            )
            assert delivery_job is not None, "Delivery job not found"

            if delivery_job["status"] in [
                DeliveryJobStatus.AVAILABLE,
                DeliveryJobStatus.COMPLETED,
                DeliveryJobStatus.FAILED,
                DeliveryJobStatus.CANCELLED,
            ]:
                return BaseResponse[TrackOrderDto].success(
                    "Order fetched successfully.",
                    TrackOrderDto.from_entities(
                        order,
                        self._uow,
                        delivery_job=delivery_job,
                    ),
                )

            driver_id = delivery_job.get("driver_id")
            assert driver_id is not None, "Driver ID not found"

            driver = self._uow.driver_repository.get(id=driver_id)
            assert driver is not None, "Driver not found"

            return BaseResponse[TrackOrderDto].success(
                "Order fetched successfully.",
                TrackOrderDto.from_entities(
                    order,
                    self._uow,
                    delivery_job=delivery_job,
                    driver=driver,
                ),
            )

        raise ApplicationException(
            Exceptions.NotFoundException,
            "Order not found.",
            [f"Order with id {request.order_id} not found."],
        )
