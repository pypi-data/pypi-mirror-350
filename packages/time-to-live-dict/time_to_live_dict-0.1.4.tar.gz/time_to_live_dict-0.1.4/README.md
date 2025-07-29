# Introduction

This library provides the same experience of builtin `dict`, plus automatical time-to-live (TTL) management.

# How it Works

Different from some other libraries, this one does not require background thread and guarantees that the expired items do not affect results.

Note that technically our `TTLDict` class is a subclass of `MutableMapping` instead of `dict`.

Internally, it utilizes a `dict` to manage expiries. Because every item has the same TTL, the insert order of the `dict` matches the expiry order.

# How to Install

Simply run `pip install time-to-live-dict`.

# How to Use

It works just like builtin `dict`:
``` python
In [1]: from ttl_dict import TTLDict

In [2]: from datetime import timedelta

In [3]: from time import sleep

In [4]: ttl = timedelta(seconds=2)
   ...:
   ...: d = TTLDict(ttl, {"a": 1})
   ...: print(d)
   ...:
   ...: sleep(1)
   ...: print(d)
   ...:
   ...: sleep(1)
   ...: print(d)
{'a': 1}
{'a': 1}
{}

In [5]: ttl1 = timedelta(seconds=2)
   ...: ttl2 = timedelta(seconds=4)
   ...:
   ...: d1 = TTLDict(ttl1, {"a": 1})
   ...: d2 = TTLDict(ttl2, {"b": 2})
   ...:
   ...: d = d1 | d2
   ...: print(d)
   ...:
   ...: sleep(2)
   ...: print(d)
   ...:
   ...: sleep(2)
   ...: print(d)
{'a': 1, 'b': 2}
{'b': 2}
{}
```

In additional, it offers a few new methods:

- `cleanup()` cleans up all expired items. Note that this method is called automatically.
- `cleanup_by_key(key)` cleans up item with specified key if it is expired. Note that this method is called automatically.
- `get_expiry(key)` gets the expiry of specified key if it is not expired yet
- `renew_expiry(key)` renews the expiry of specified key (as if it was just inserted into)
