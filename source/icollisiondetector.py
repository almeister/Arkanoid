from abc import ABC, abstractmethod


class ICollisionDetectorListener(ABC):
    """
    Interface for objects that should be notified when some event occurs,
    for example: when a collision occurs.
    """

    @abstractmethod
    def on_collision(self, observable) -> None:
        pass


class ICollisionDetector(ABC):
    """
    Interface for an Observable object that keeps a list of Observers and notifies
    them when some triggering event occurs.
    """

    @abstractmethod
    def add_listener(self, observer: ICollisionDetectorListener) -> None:
        pass

    @abstractmethod
    def remove_listener(self, observer: ICollisionDetectorListener) -> None:
        pass

    @abstractmethod
    def notify(self) -> None:
        pass
