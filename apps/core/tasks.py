from celery import shared_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@shared_task(name="default:dynamic_routing_task_one")
def dynamic_routing_task_one():
    logger.info("Example One")


@shared_task(name="low_priority:dynamic_routing_task_two")
def dynamic_routing_task_two():
    logger.info("Example Two")


@shared_task(name="high_priority:dynamic_routing_task_three")
def dynamic_routing_task_three():
    logger.info("Example Three")
