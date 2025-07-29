# Copyright 2023-2025 Geoffrey R. Scheller
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
#### Immutable homogeneous "lists"

- immutable data structure whose elements are all of the same type
- hashable if elements are hashable
  - TODO: not sure if I am enforcing hashability
- declared covariant in its generic datatype
  - hashability should be enforced by LSP tooling
  - hashability will be enforced at runtime
  - ImmutableList addition supported via concatenation
  - ImmutableList integer multiplication supported

"""

from __future__ import annotations

from collections.abc import Callable, Iterable, Iterator, Hashable
from typing import cast, Never, overload, TypeVar
from dtools.iterables import FM, accumulate, concat, exhaust, merge

__all__ = ['ImmutableList', 'immutable_list']

D_co = TypeVar('D_co', covariant=True)


class ImmutableList[D_co](Hashable):
    """Immutable List like data structures

    - immutable "lists" all whose elements are all of the same type
    - A `ImmutableList` is covariant in its generic datatype
      - its method type parameters are also declared covariant
      - hashability will be enforced by LSP tooling
    - supports both indexing and slicing
    - `ImmutableList` addition & `int` multiplication supported
      - addition concatenates results, resulting type a Union type
      - both left and right int multiplication supported

    """

    __slots__ = ('_ds', '_len', '_hash')
    __match_args__ = ('_ds', '_len')

    L_co = TypeVar('L_co', covariant=True)
    R_co = TypeVar('R_co', covariant=True)
    U_co = TypeVar('U_co', covariant=True)

    def __init__(self, *dss: Iterable[D_co]) -> None:
        if (size := len(dss)) > 1:
            msg = f'ImmutableList expects at most 1 iterable argument, got {size}'
            raise ValueError(msg)
        else:
            self._ds: tuple[D_co, ...] = tuple(dss[0]) if size == 1 else tuple()
            self._len = len(self._ds)
            try:
                self._hash = hash((self._len, 42) + self._ds)
            except TypeError as exc:
                msg = f'ImmutableList: {exc}'
                raise TypeError(msg)

    def __hash__(self) -> int:
        return self._hash

    def __iter__(self) -> Iterator[D_co]:
        return iter(self._ds)

    def __reversed__(self) -> Iterator[D_co]:
        return reversed(self._ds)

    def __bool__(self) -> bool:
        return bool(self._ds)

    def __len__(self) -> int:
        return len(self._ds)

    def __repr__(self) -> str:
        return 'immutable_list(' + ', '.join(map(repr, self)) + ')'

    def __str__(self) -> str:
        return '((' + ', '.join(map(repr, self)) + '))'

    def __eq__(self, other: object, /) -> bool:
        if not isinstance(other, ImmutableList):
            return NotImplemented  # magic object
        if self._len != other._len:
            return False
        if self._ds is other._ds:
            return True
        return self._ds == other._ds

    @overload
    def __getitem__(self, idx: int, /) -> D_co: ...
    @overload
    def __getitem__(self, idx: slice, /) -> ImmutableList[D_co]: ...

    def __getitem__(self, idx: slice | int, /) -> ImmutableList[D_co] | D_co:
        if isinstance(idx, slice):
            return ImmutableList(self._ds[idx])
        return self._ds[idx]

    def foldl[L_co](
        self,
        f: Callable[[L_co, D_co], L_co],
        /,
        start: L_co | None = None,
        default: L_co | None = None,
    ) -> L_co | None:
        """Fold Left

        - fold left with an optional starting value
        - first argument of function `f` is for the accumulated value
        - throws `ValueError` when `ImmutableList` empty and a start value not given

        """
        it = iter(self._ds)
        if start is not None:
            acc = start
        elif self:
            acc = cast(L_co, next(it))  # L_co = D_co in this case
        else:
            if default is None:
                msg0 = 'ImmutableList: foldl method requires '
                msg1 = 'either start or default to be defined for '
                msg2 = 'an empty ImmutableList'
                raise ValueError(msg0 + msg1 + msg2)
            acc = default
        for v in it:
            acc = f(acc, v)
        return acc

    def foldr[R_co](
        self,
        f: Callable[[D_co, R_co], R_co],
        /,
        start: R_co | None = None,
        default: R_co | None = None,
    ) -> R_co | None:
        """Fold Right

        - fold right with an optional starting value
        - second argument of function `f` is for the accumulated value
        - throws `ValueError` when `ImmutableList` empty and a start value not given

        """
        it = reversed(self._ds)
        if start is not None:
            acc = start
        elif self:
            acc = cast(R_co, next(it))
        else:
            if default is None:
                msg0 = 'ImmutableList: foldr method requires '
                msg1 = 'either start or default to be defined for '
                msg2 = 'an empty ImmutableList'
                raise ValueError(msg0 + msg1 + msg2)
            acc = default
        for v in it:
            acc = f(v, acc)
        return acc

    def __add__(self, other: ImmutableList[D_co], /) -> ImmutableList[D_co]:
        if not isinstance(other, ImmutableList):
            msg = 'ImmutableList being added to something not a ImmutableList'
            raise ValueError(msg)

        return ImmutableList(concat(self, other))

    def __mul__(self, num: int, /) -> ImmutableList[D_co]:
        return ImmutableList(self._ds.__mul__(num if num > 0 else 0))

    def __rmul__(self, num: int, /) -> ImmutableList[D_co]:
        return ImmutableList(self._ds.__mul__(num if num > 0 else 0))

    def accummulate[L_co](
        self, f: Callable[[L_co, D_co], L_co], s: L_co | None = None, /
    ) -> ImmutableList[L_co]:
        """Accumulate partial folds

        Accumulate partial fold results in an ImmutableList with an optional
        starting value.

        """
        if s is None:
            return ImmutableList(accumulate(self, f))
        return ImmutableList(accumulate(self, f, s))

    def map[U_co](self, f: Callable[[D_co], U_co], /) -> ImmutableList[U_co]:
        return ImmutableList(map(f, self))

    def bind[U_co](
        self, f: Callable[[D_co], ImmutableList[U_co]], type: FM = FM.CONCAT, /
    ) -> ImmutableList[U_co] | Never:
        """Bind function `f` to the `ImmutableList`.

        * FM Enum types
          * CONCAT: sequentially concatenate iterables one after the other
          * MERGE: round-robin merge iterables until one is exhausted
          * EXHAUST: round-robin merge iterables until all are exhausted

        """
        match type:
            case FM.CONCAT:
                return ImmutableList(concat(*map(f, self)))
            case FM.MERGE:
                return ImmutableList(merge(*map(f, self)))
            case FM.EXHAUST:
                return ImmutableList(exhaust(*map(f, self)))

        raise ValueError(f'ImmutableList: Unknown FM type: {type}')


def immutable_list[D_co](*ds: D_co) -> ImmutableList[D_co]:
    return ImmutableList(ds)
