class Subscription(object):

    def __init__(self, unsubscribe_callable, observer):
        self._unsubscribe_callable = unsubscribe_callable
        self._observer = observer

    def unsubscribe(self):
        self._unsubscribe_callable(self._observer)
