from abc import ABC


class EventSubscriber(ABC):

    def __init__(self, event_bus):
        self.event_bus = event_bus

    def subscribe(self, event_type, callback):
        self.event_bus.subscribe(event_type, self, callback)

    def __del__(self):
        self.event_bus.unsubscribe(self)
