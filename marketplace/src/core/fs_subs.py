from faststream.rabbit import RabbitRouter
from loguru import logger

from src.core.config import settings

router = RabbitRouter()


@router.subscriber(settings.faststream.user_registered_event)
async def send_success_register_email(email: str) -> None:
    logger.debug(f"send_success_register_email {email}")
