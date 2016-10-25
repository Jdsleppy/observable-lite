from .subscription import Subscription


class Observable(object):
    """
    Objects of this type publish data to be consumed by any of its subscribing
    observers.
    """

    def __init__(self):
        self.observers = []

    def __call__(self, data=None):
        for observer in self.observers:
            observer(data)

    def subscribe(self, observer):
        """
        Subscribe a callback to all future publications.

        :param observer: A callable to be called with each publication.

        :return: A handle to the subscription, to be used for unsubscribing.
        :rtype: observable_lite.subscription.Subscription
        """
        self.observers.append(observer)
        return Subscription(self._unsubscribe, observer)

    def _unsubscribe(self, observer):
        self.observers.remove(observer)
