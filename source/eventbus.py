from queue import SimpleQueue
from types import LambdaType
from typing import List, Dict, Tuple

from eventsubscriber import EventSubscriber
from gameevent import GameEvent


class EventBus:

    def __init__(self):
        self.event_queue: SimpleQueue[GameEvent] = SimpleQueue()
        # event_subscriptions a Dict of {event_type : (EventSubscriber, callback)}
        self.event_subscriptions: Dict[List[Tuple[EventSubscriber, LambdaType]]] = {}

    def subscribe(self, event_type, subscriber: EventSubscriber, callback):
        if event_type not in self.event_subscriptions:
            self.event_subscriptions[event_type] = [(subscriber, callback)]
        else:
            self.event_subscriptions[event_type].append(subscriber, callback)

    def unsubscribe(self, subscriber):
        for event, subscribers in self.event_subscriptions:
            for sub in subscribers:
                if sub[0] == subscriber:
                    subscribers.remove(sub)  # TODO: Fix, find and slice

    def publish(self, event):
        self.event_queue.put(event)

    def update(self):
        while not self.event_queue.empty():
            event = self.event_queue.get()
            if event.TYPE in self.event_subscriptions:
                for subscriber, callback in self.event_subscriptions[event.TYPE]:
                    callback(event)
