from datetime import timedelta
from time import sleep

from ttl_dict import TTLDict


def test_ttl_dict_expiry() -> None:
    ttl = timedelta(seconds=2)

    d = TTLDict[str, int](ttl, {"a": 1})
    assert "a" in d

    sleep(1)
    assert "a" in d

    sleep(1)
    assert "a" not in d


def test_ttl_dict_union() -> None:
    ttl1 = timedelta(seconds=2)
    ttl2 = timedelta(seconds=4)

    d1 = TTLDict[str, int](ttl1, {"a": 1})
    d2 = TTLDict[str, int](ttl2, {"b": 2})

    d = d1 | d2
    assert "a" in d
    assert "b" in d

    sleep(2)
    assert "a" not in d
    assert "b" in d

    sleep(2)
    assert "a" not in d
    assert "b" not in d
