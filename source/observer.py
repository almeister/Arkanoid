from abc import ABC, abstractmethod


class Observer(ABC):
    """
    Interface for objects that should be notified when some event occurs,
    for example: when a collision occurs.
    """

    @abstractmethod
    def on_observed(self, observable) -> None:
        pass


class Observable(ABC):
    """
    Interface for an Observable object that keeps a list of Observers and notifies
    them when some triggering event occurs.
    """

    @abstractmethod
    def add_listener(self, observer: Observer) -> None:
        pass

    @abstractmethod
    def remove_listener(self, observer: Observer) -> None:
        pass

    @abstractmethod
    def notify(self) -> None:
        pass
