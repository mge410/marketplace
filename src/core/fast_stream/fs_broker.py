__all__ = ("broker",)

from faststream.rabbit import RabbitBroker

from src.core.config import settings

broker = RabbitBroker(str(settings.faststream.url))
