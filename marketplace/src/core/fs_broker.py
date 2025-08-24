__all__ = ("broker",)

from faststream.rabbit import RabbitBroker

from src.core.config import settings

broker = RabbitBroker(settings.faststream.url)

# app = FastStream(broker)
