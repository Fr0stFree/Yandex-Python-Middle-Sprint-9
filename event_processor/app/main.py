from typing import Literal

from settings import Settings
from src.extractor import EventExtractor
from src.transformer import EventTransformer
from src.loader import EventLoader
from src.consumers import KafkaBroker, RabbitBroker


def get_broker(broker: Literal['kafka', 'rabbitmq']) -> KafkaBroker | RabbitBroker:
    if broker == 'kafka':
        return KafkaBroker(broker_url=settings.kafka_url, topic=settings.kafka_topic)
    elif broker == 'rabbitmq':
        return RabbitBroker(host=settings.rabbitmq_host, port=settings.rabbitmq_port,
                            user=settings.rabbitmq_user, password=settings.rabbitmq_password,
                            exchange_name=settings.rabbitmq_exchange, queue_name=settings.rabbitmq_queue_name)


if __name__ == '__main__':
    settings = Settings()
    extractor = EventExtractor(message_broker=get_broker(settings.selected_broker))
    transformer = EventTransformer()
    loader = EventLoader()

    for events in extractor.start():
        transformed_events = transformer.transform(events)
        loader.load(transformed_events)

