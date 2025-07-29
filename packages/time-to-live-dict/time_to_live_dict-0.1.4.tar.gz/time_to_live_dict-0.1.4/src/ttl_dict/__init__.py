from __future__ import annotations

from collections import UserDict
from collections.abc import ItemsView, Iterable, Iterator, KeysView, Mapping, ValuesView
from datetime import UTC, datetime, timedelta
from typing import Self, cast, overload, override


class TTLDict[_KT, _VT](UserDict[_KT, _VT]):
    def __init__(
        self,
        ttl: timedelta,
        other: Mapping[_KT, _VT] | Iterable[tuple[_KT, _VT]] | None = None,
        /,
        **kwargs: _VT,
    ) -> None:
        self.__ttl: timedelta = ttl

        self.__expiries: dict[_KT, datetime] = {}

        # Must be at the end of __init__ as it calls self.update which needs self.__ttl
        super().__init__(other, **kwargs)

    def cleanup(self) -> None:
        now: datetime = datetime.now(UTC)

        expired_keys: list[_KT] = []
        for key, expiry in self.__expiries.items():
            # As dict is iterated by insert order, the newer ones are iterated later
            if now < expiry:
                break

            expired_keys.append(key)

        for key in expired_keys:
            del self.__expiries[key]
            del self.data[key]

    def cleanup_by_key(self, key: _KT) -> bool:
        now: datetime = datetime.now(UTC)

        if key not in self.__expiries:
            return False

        if self.__expiries[key] <= now:
            del self.__expiries[key]
            del self.data[key]

            return False

        return True

    @override
    def __len__(self) -> int:
        self.cleanup()
        return super().__len__()

    @override
    def __contains__(self, key: _KT) -> bool:
        return self.cleanup_by_key(key)

    @override
    def __getitem__(self, key: _KT) -> _VT:
        self.cleanup_by_key(key)
        return super().__getitem__(key)

    def get_expiry(self, key: _KT) -> datetime | None:
        self.cleanup_by_key(key)
        return self.__expiries.get(key)

    @override
    def __iter__(self) -> Iterator[_KT]:
        self.cleanup()
        return super().__iter__()

    @override
    def clear(self) -> None:
        self.__expiries.clear()
        self.data.clear()

    @override
    def __delitem__(self, key: _KT) -> None:
        del self.__expiries[key]
        super().__delitem__(key)

    @override
    def __setitem__(self, key: _KT, value: _VT) -> None:
        self.__expiries[key] = datetime.now(UTC) + self.__ttl
        super().__setitem__(key, value)

    def renew_expiry(self, key: _KT) -> None:
        del self.__expiries[key]
        self.__expiries[key] = datetime.now(UTC) + self.__ttl

    @overload
    def update(
        self,
        other: Mapping[_KT, _VT],
        /,
        **kwargs: _VT,
    ) -> None: ...
    @overload
    def update(
        self,
        other: Iterable[tuple[_KT, _VT]],
        /,
        **kwargs: _VT,
    ) -> None: ...
    @overload
    def update(
        self,
        other: None = None,
        /,
        **kwargs: _VT,
    ) -> None: ...
    @override
    def update(
        self,
        other=None,
        /,
        **kwargs,
    ) -> None:
        now: datetime = datetime.now(UTC)
        expiry: datetime = now + self.__ttl
        other_ttl_dict: bool = isinstance(other, TTLDict)

        key: _KT
        value: _VT
        if isinstance(other, Mapping):
            for key, value in other.items():
                self.__expiries[key] = (
                    # In rare case, item may have been expired during iteration
                    # Thus, we set expiry to now (which means it is already expired)
                    (other.get_expiry(key) or now) if other_ttl_dict
                    else expiry
                )
                self.data[key] = value
        elif isinstance(other, Iterable):
            for key, value in other:
                self.__expiries[key] = expiry
                self.data[key] = value

        for str_key, value in kwargs.items():
            key = cast("_KT", str_key)
            self.__expiries[key] = expiry
            self.data[key] = value

    @override
    def copy(self) -> TTLDict:
        return TTLDict(self.__ttl, self)

    @override
    def __or__(self, other: Mapping[_KT, _VT]) -> TTLDict:
        d: TTLDict = self.copy()
        d.update(other)

        return d

    @override
    def __ior__(self, other: Mapping[_KT, _VT]) -> Self:
        self.update(other)
        return self

    @override
    def __repr__(self) -> str:
        self.cleanup()
        return super().__repr__()

    @override
    def keys(self) -> KeysView:
        self.cleanup()
        return super().keys()

    @override
    def values(self) -> ValuesView:
        self.cleanup()
        return super().values()

    @override
    def items(self) -> ItemsView:
        self.cleanup()
        return super().items()
