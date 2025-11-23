from faststream.rabbit import RabbitRouter

from src.core.config import settings
from src.core.email.utils import send_email

router = RabbitRouter()


@router.subscriber(settings.faststream.user_registered_event)
async def send_success_register_email(email: str) -> None:
    await send_email(
        email,
        "Welcome to marketplace!",
        "Welcome to marketplace!",
    )
