from datetime import UTC, datetime, timedelta
from math import asin, cos, radians, sin, sqrt

from ed_domain.core.entities.delivery_job import WayPoint, WayPointType
from ed_domain.core.repositories import ABCUnitOfWork
from ed_domain.queues.common.abc_subscriber import ABCSubscriber
from ed_domain.queues.ed_optimization.business_model import LocationModel
from ed_domain.queues.ed_optimization.order_model import OrderModel
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_optimization.application.common.responses.base_response import \
    BaseResponse
from ed_optimization.application.contracts.infrastructure.api.abc_api import \
    ABCApi
from ed_optimization.application.contracts.infrastructure.cache.abc_cache import \
    ABCCache
from ed_optimization.application.features.order.requests.commands import \
    ProcessOrderCommand
from ed_optimization.common.logging_helpers import get_logger

LOG = get_logger()
RADIUS_OF_EARTH_KM = 6371  # Radius of Earth in kilometers
MAX_BATCH_SIZE = 2
MAX_WAIT_TIME = timedelta(minutes=5)


@request_handler(ProcessOrderCommand, BaseResponse[None])
class ProcessOrderCommandHandler(RequestHandler):
    def __init__(
        self,
        uow: ABCUnitOfWork,
        subscriber: ABCSubscriber[OrderModel],
        cache: ABCCache[list[OrderModel]],
        api: ABCApi,
    ):
        self._cache_key = "pending_delivery_job"
        self._uow = uow
        self._cache = cache
        self._api = api
        subscriber.add_callback_function(self._process_order)

    async def handle(self, request: ProcessOrderCommand) -> BaseResponse[None]:
        self._process_order(request.model)
        return BaseResponse[None].success(
            message="Order processed successfully",
            data=None,
        )

    def _process_order(self, message: OrderModel) -> None:
        LOG.info(f"Received message: {message}")
        pending_orders = self._get_pending_orders()

        if not pending_orders:
            LOG.info("No pending orders, initializing queue with current order.")
            self._save_pending_orders([message])
            return

        oldest_order = pending_orders[0]
        if datetime.now(UTC) - oldest_order["create_datetime"] > MAX_WAIT_TIME:
            LOG.info("Oldest order too old. Forcing batch flush.")
            self._flush_pending_orders(pending_orders + [message])
            return

        if self._is_match(message, pending_orders):
            LOG.info("Order matches current batch. Appending.")
            pending_orders.append(message)
        else:
            LOG.info(
                "Order does not match current batch. Flushing and starting new batch."
            )
            self._flush_pending_orders(pending_orders)
            pending_orders = [message]

        if len(pending_orders) >= MAX_BATCH_SIZE:
            LOG.info("Batch size threshold reached. Flushing.")
            self._flush_pending_orders(pending_orders)
        else:
            self._save_pending_orders(pending_orders)

    def _is_match(self, order: OrderModel, pending_orders: list[OrderModel]) -> bool:
        # Match if within time and distance threshold
        for existing in pending_orders:
            time_delta = abs(
                (
                    order["latest_time_of_delivery"]
                    - existing["latest_time_of_delivery"]
                ).total_seconds()
            )

            if time_delta > 1800:  # 30 mins
                return False
            if (
                self._haversine_distance_km(
                    order["business"]["location"], existing["business"]["location"]
                )
                > 5
            ):
                return False
        return True

    def _flush_pending_orders(self, orders: list[OrderModel]) -> None:
        LOG.info(f"Flushing {len(orders)} orders into a DeliveryJob.")

        waypoints = self._optimize_waypoints(
            [
                {
                    "order_id": order["id"],
                    "type": waypoint_type,
                    "eta": order["latest_time_of_delivery"],
                    "sequence": sequence,
                }
                for order in orders
                for waypoint_type, sequence in [
                    (WayPointType.PICKUP, 0),
                    (WayPointType.DROP_OFF, 1),
                ]
            ]
        )

        create_delivery_job_response = self._api.core_api.create_delivery_job(
            {
                "waypoints": waypoints,
                "estimated_distance_in_kms": 0.0,
                "estimated_completion_time": datetime.now(UTC) + timedelta(hours=1),
                "estimated_time_in_minutes": 60,
                "estimated_payment": 0.0,
            }
        )
        if not create_delivery_job_response["is_success"]:
            LOG.error(
                f"Failed to create delivery job: {create_delivery_job_response['message']}"
            )
        else:
            self._cache.set(self._cache_key, [])  # clear cache
            LOG.info("Delivery job created and persisted (stub).")

    def _get_pending_orders(self) -> list[OrderModel]:
        if pending := self._cache.get(self._cache_key):
            return pending
        return []

    def _save_pending_orders(self, orders: list[OrderModel]) -> None:
        self._cache.set(self._cache_key, orders)
        LOG.info(f"Saved {len(orders)} orders to pending cache.")

    def _haversine_distance_km(self, loc1: LocationModel, loc2: LocationModel) -> float:
        lat1, lon1 = loc1["latitude"], loc1["longitude"]
        lat2, lon2 = loc2["latitude"], loc2["longitude"]
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2

        c = 2 * asin(sqrt(a))
        return c * RADIUS_OF_EARTH_KM

    def _optimize_waypoints(self, waypoints: list[WayPoint]) -> list[WayPoint]:
        # Placeholder for actual optimization logic
        return waypoints
