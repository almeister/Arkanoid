from abc import ABC


class EventSubscriber(ABC):

    def __init__(self, event_bus):
        self.event_bus = event_bus

    def __del__(self):
        self.event_bus.unsubscribe(self)
