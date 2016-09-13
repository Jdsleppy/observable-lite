# observable-lite
A feather-light observer implementation inspired by Reactive Extensions.

Install with `pip install -e git+https://github.com/Jdsleppy/observable-lite#egg=observable-lite`

```python
from observable_lite.observable import Observable

# An Observable publishes data
observable = Observable()
# An observer is a __call__-able that receives data
observer1 = lambda data: print('I heard {}'.format(data))
subscription1 = observable.subscribe(observer1)
observable('the cat')
# --> I heard the cat

observer2 = lambda data: print('I heard {}, too!'.format(data))
subscription2 = observable.subscribe(observer2)
observable('the dog')
# --> I heard the dog
# --> I heard the dog, too!

# Selectively unsubscribe observers
subscription1.unsubscribe()
observable('the washing machine')
# --> I heard the washing machine, too!
```
