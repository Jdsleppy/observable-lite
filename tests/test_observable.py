import unittest.mock as mock

from observable_lite.observable import Observable


class MockFactory(object):
    def one(self):
        """
        :rtype: unittest.mock.MagicMock
        """
        return mock.MagicMock()

    def get(self, number):
        """
        :rtype: list[unittest.mock.MagicMock]
        """
        return [self.one() for _ in range(number)]


def test_single_subscription():
    """
    A single subscriber should receive notifications.
    """
    observable = Observable()
    observer = MockFactory().one()
    subscription = observable.subscribe(observer)
    assert not observer.called

    observable('message')
    assert observer.call_count == 1
    observer.assert_called_with('message')

    observable('another message')
    assert observer.call_count == 2
    observer.assert_called_with('another message')


def test_multiple_subscriptions():
    """
    Multiple subscribers should receive the same notifications.
    """
    observable = Observable()
    observers = MockFactory().get(3)
    subscriptions = [observable.subscribe(observer) for observer in observers]

    for observer in observers:
        assert not observer.called

    observable('message')
    for observer in observers:
        assert observer.call_count == 1
        observer.assert_called_with('message')

    observable('another message')
    for observer in observers:
        assert observer.call_count == 2
        observer.assert_called_with('another message')


def test_unsubscription():
    """
    Only unsubscribed observers should stop receiving notifications.
    """
    observable = Observable()
    observers = MockFactory().get(3)
    subscriptions = [observable.subscribe(observer) for observer in observers]

    observable('message')

    subscriptions[1].unsubscribe()
    unsubscribed_observer = observers.pop(1)
    observable('another message')
    for observer in observers:
        assert observer.call_count == 2
        observer.assert_called_with('another message')

    unsubscribed_observer.assert_called_with('message')


def test_duplicate_subscriptions():
    """
    Multiple subscriptions of a single observer should function the same as
    single subscriptions of multiple observers.
    """
    observable = Observable()
    observer = MockFactory().one()
    subscriptions = [observable.subscribe(observer) for _ in range(3)]
    assert not observer.called

    observable('message')
    assert observer.call_count == 3
    assert observer.call_args_list == [mock.call('message')] * 3

    observable('another message')
    assert observer.call_count == 6
    assert observer.call_args_list == (
        [mock.call('message')] * 3 + [mock.call('another message')] * 3
    )


def test_duplicate_unsubscriptions():
    """
    Unsubscribing any of multiple subscriptions of a single observer should
    interrupt only the unsubscribed individual instance.
    """
    observable = Observable()
    observer = MockFactory().one()
    subscriptions = [observable.subscribe(observer) for _ in range(3)]
    assert not observer.called

    observable('message')

    subscriptions[1].unsubscribe()
    observable('another message')

    assert observer.call_count == 5
    assert observer.call_args_list == (
        [mock.call('message')] * 3 + [mock.call('another message')] * 2
    )


def test_no_subscriptions():
    """
    No error should be raised if no subscriptions exist.
    """
    observable = Observable()
    observable('message')
