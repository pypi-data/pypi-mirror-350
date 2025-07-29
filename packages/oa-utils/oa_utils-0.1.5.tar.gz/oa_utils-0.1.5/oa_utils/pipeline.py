from __future__ import annotations
import functools
import itertools
import more_itertools
from pprint import pprint
from typing import IO, Callable, Iterable, Literal, TypeVar, Any

T_co = TypeVar("T_co", covariant=True)
T = TypeVar("T")
U = TypeVar("U")
V = TypeVar("V")
K = TypeVar("K")


class Pipeline(tuple[T_co, ...]):
    """Fluent wrapper around a homogenous variadic tuple.
    
    >>> (Pipeline(range(10))
    ... .filter(lambda x: x % 2 == 0)
    ... .map(lambda x: x * x)
    ... .sum())                      
    120
    """

    def map(self, fn: Callable[[T_co], U]) -> Pipeline[U]:
        """
        >>> Pipeline([1, 2, 3]).map(lambda x: x * 2)
        (2, 4, 6)
        """
        return Pipeline(map(fn, self))

    def filter(self, pred: Callable[[T_co], bool]) -> Pipeline[T_co]:
        """
        >>> Pipeline([1, 2, 3, 4]).filter(lambda x: x % 2 == 0)
        (2, 4)
        """
        return Pipeline(filter(pred, self))

    def zip(self, other: Iterable[U], strict: bool = False) -> Pipeline[tuple[T_co, U]]:
        """
        >>> Pipeline([1, 2]).zip([10, 20])
        ((1, 10), (2, 20))
        """
        return Pipeline(zip(self, other, strict=strict))

    def zip_longest(self, other: Iterable[U], fillvalue: V) -> Pipeline[tuple[T_co | V, U | V]]:
        """
        >>> Pipeline([1, 2]).zip_longest([10, 20, 30], fillvalue=None)
        ((1, 10), (2, 20), (None, 30))
        
        >>> Pipeline([1, 2, 3]).zip_longest([10, 20], fillvalue=0)
        ((1, 10), (2, 20), (3, 0))
        """
        return Pipeline(itertools.zip_longest(self, other, fillvalue=fillvalue))

    def zip_with(self, fn: Callable[[T_co, U], V], other: Iterable[U], strict: bool = False) -> Pipeline[V]:
        """
        >>> Pipeline([1, 2]).zip_with(lambda a, b: a + b, [10, 20])
        (11, 22)
        """
        return Pipeline(fn(a, b) for a, b in zip(self, other, strict=strict))

    def starmap(self: Pipeline[tuple[T, U]], fn: Callable[[T, U], V]) -> Pipeline[V]:
        """
        >>> Pipeline([(1, 2), (3, 4)]).starmap(lambda a, b: a + b)
        (3, 7)
        """
        if not all(isinstance(item, tuple) and len(item) == 2 for item in self):
            raise ValueError("starmap requires a Pipeline of tuples with 2 elements")
        return Pipeline(fn(a, b) for a, b in self) 

    def cartesian_product(self, other: Iterable[U]) -> Pipeline[tuple[T_co, U]]:
        """
        >>> Pipeline([1, 2]).cartesian_product([10, 20])
        ((1, 10), (1, 20), (2, 10), (2, 20))
        """
        return Pipeline(itertools.product(self, other))

    def sort(self, key: Callable[[T_co], Any] | None = None, reverse: bool = False) -> Pipeline[T_co]:
        """
        >>> Pipeline([3, 1, 2]).sort()
        (1, 2, 3)
        
        >>> Pipeline([3, 1, 2]).sort(reverse=True)
        (3, 2, 1)
        """
        return Pipeline(sorted(self, key=key, reverse=reverse)) # type: ignore

    def unique(self) -> Pipeline[T_co]:
        """
        >>> Pipeline([1, 2, 2, 3]).unique()
        (1, 2, 3)
        """
        return Pipeline(dict.fromkeys(self))
    
    def slice(self, start: int = 0, end: int | None = None, step: int = 1) -> Pipeline[T_co]:
        """
        >>> Pipeline([1, 2, 3, 4, 5]).slice(1, 4)
        (2, 3, 4)
        """
        if end is None:
            end = len(self)
        return Pipeline(self[start:end:step])

    def take(self, n: int) -> Pipeline[T_co]:
        """
        >>> Pipeline([1, 2, 3, 4]).take(2)
        (1, 2)
        """
        return Pipeline(self[:n])
    
    def drop(self, n: int) -> Pipeline[T_co]:
        """
        >>> Pipeline([1, 2, 3, 4]).drop(2)
        (3, 4)
        """
        return Pipeline(self[n:])

    def enumerate(self, start: int = 0) -> Pipeline[tuple[int, T_co]]:
        """
        >>> Pipeline(['a', 'b']).enumerate()
        ((0, 'a'), (1, 'b'))
        """
        return Pipeline(enumerate(self, start))

    def batch(self, n: int, strict: bool = False) -> Pipeline[Pipeline[T_co]]:
        """
        >>> Pipeline(range(1, 6)).batch(2)
        ((1, 2), (3, 4), (5,))
        """
        return Pipeline([Pipeline(batch) for batch 
                         in more_itertools.chunked(self, n, strict=strict)])
    
    def batch_fill(self, n: int, 
                   fillvalue: U,
                   incomplete: Literal['fill', 'ignore', 'strict'] = 'fill') -> Pipeline[Pipeline[T_co | U]]:
        """
        >>> Pipeline(range(1, 6)).batch_fill(2, fillvalue=0)
        ((1, 2), (3, 4), (5, 0))
        """
        return Pipeline([Pipeline(row) for row in more_itertools.grouper(
                        self, n, incomplete=incomplete, fillvalue=fillvalue)])

    def flatten(self: Pipeline[Iterable[T]]) -> Pipeline[T]:
        """
        >>> Pipeline([[1, 2], [3, 4]]).flatten()
        (1, 2, 3, 4)
        """
        if not all(isinstance(item, Iterable) for item in self):
            raise ValueError("flatten requires a Pipeline of Iterables")
        return Pipeline(itertools.chain.from_iterable(self))

    def for_each(self, fn: Callable[[T_co], None]) -> Pipeline[T_co]:
        """
        >>> Pipeline([1, 2, 3]).for_each(print)
        1
        2
        3
        (1, 2, 3)
        """
        for item in self:
            fn(item)
        return self

    def for_self(self, fn: Callable[[Pipeline[T_co]], None]) -> Pipeline[T_co]:
        """
        >>> Pipeline([1, 2, 3]).for_self(lambda p: print(p.len()))
        3
        (1, 2, 3)
        """
        fn(self)
        return self

    def print(self, label: str = "", 
              label_only: bool = False,
              end: str | None = "\n",
              file: IO[str] | None = None,
              flush: bool = False) -> Pipeline[T_co]:
        """
        >>> Pipeline([1, 2, 3]).print("Numbers: ", end="\\n\\n")
        Numbers: (1, 2, 3)
        <BLANKLINE>
        (1, 2, 3)
        
        >>> Pipeline([1, 2, 3]).print("Numbers:", label_only=True)
        Numbers:
        (1, 2, 3)
        """
        if label_only:
            print(label, end=end, file=file, flush=flush)
        else:
            print(f"{label}{self}", end=end, file=file, flush=flush)
        return self

    def pprint(self, label: str = "", end: str = "",
               stream: IO[str] | None = None, 
               indent: int = 1, width: int = 80, 
               depth: int | None = None, 
               compact: bool = False, 
               sort_dicts: bool = True, 
               underscore_numbers: bool = False) -> Pipeline[T_co]:
        """
        >>> Pipeline([1, 2, 3]).pprint("Numbers:" , end="\\n")
        Numbers:
        (1, 2, 3)
        <BLANKLINE>
        (1, 2, 3)
        """
        if label:
            print(label, file=stream)
        pprint(self, stream=stream, indent=indent, width=width,
               depth=depth, compact=compact, sort_dicts=sort_dicts,
               underscore_numbers=underscore_numbers)
        if end:
            print(end, file=stream, end="")
        return self

    def append(self, item: T) -> Pipeline[T_co | T]:
        """
        >>> Pipeline([1, 2]).append(3)
        (1, 2, 3)
        """
        return Pipeline(self + (item,))

    def prepend(self, item: T) -> Pipeline[T_co | T]:
        """
        >>> Pipeline([2, 3]).prepend(1)
        (1, 2, 3)
        """
        return Pipeline((item,) + self)

    def extend(self, items: Iterable[T_co]) -> Pipeline[T_co]:
        """
        >>> Pipeline([1, 2]).extend([3, 4])
        (1, 2, 3, 4)
        """
        return Pipeline(self + tuple(items))
    
    def insert(self, index: int, item: T) -> Pipeline[T_co | T]:
        """
        >>> Pipeline([1, 2, 4]).insert(2, 3)
        (1, 2, 3, 4)
        """
        return Pipeline(self[:index] + (item,) + self[index:])
    
    def reverse(self) -> Pipeline[T_co]:
        """
        >>> Pipeline([1, 2, 3]).reverse()
        (3, 2, 1)
        """
        return Pipeline(reversed(self))

    # === Terminal methods ===

    def to_list(self) -> list[T_co]:
        """
        >>> Pipeline([1, 2, 3]).to_list()
        [1, 2, 3]
        """
        return list(self)

    def to_set(self) -> set[T_co]:
        """
        >>> Pipeline([1, 2, 3, 3]).to_set()
        {1, 2, 3}
        """
        return set(self)

    def to_dict(self: Pipeline[tuple[K, V]]) -> dict[K, V]:
        """
        >>> Pipeline([("a", 1), ("b", 2)]).to_dict()
        {'a': 1, 'b': 2}
        """
        return dict(self)

    def first(self) -> T_co:
        """
        >>> Pipeline([1, 2, 3]).first()
        1
        """
        if not self:
            raise IndexError("Pipeline is empty")
        return self[0]
    
    def last(self) -> T_co:
        """
        >>> Pipeline([1, 2, 3]).last()
        3
        """
        if not self:
            raise IndexError("Pipeline is empty")
        return self[-1]

    def reduce(self, fn: Callable[[V, T_co], V], initial: V) -> V:
        """
        >>> Pipeline([104, 101, 108, 108, 111]).reduce(lambda acc, x: acc + chr(x), "")     
        'hello'
        """
        return functools.reduce(fn, self, initial)

    def reduce_non_empty(self, fn: Callable[[T_co, T_co], T_co]) -> T_co:
        """
        >>> Pipeline([1, 2, 3]).reduce_non_empty(lambda acc, x: acc + x)
        6
        """
        if not self:
            raise ValueError("Pipeline is empty")
        return functools.reduce(fn, self)

    def len(self) -> int:
        """
        >>> Pipeline([1, 2, 3]).len()
        3
        """
        return len(self)
    
    def min(self) -> T_co:
        """
        >>> Pipeline([3, 1, 2]).min()
        1
        """
        return min(self) # type: ignore 
    
    def max(self) -> T_co:
        """
        >>> Pipeline([3, 1, 2]).max()
        3
        """
        return max(self) # type: ignore
    
    def sum(self) -> T_co:
        """
        >>> Pipeline([1, 2, 3]).sum()
        6
        """
        return sum(self) # type: ignore
    
    def avg(self) -> float:
        """
        >>> Pipeline([1, 2, 3]).avg()
        2.0
        """
        if not self:
            raise ValueError("Pipeline is empty")
        return sum(self) / len(self) # type: ignore
    
    def any(self) -> bool:
        """
        >>> Pipeline([False, False, True]).any()
        True
        
        >>> Pipeline([False, False, False]).any()
        False
        """
        return any(self)
    
    def all(self) -> bool:
        """
        >>> Pipeline([True, True, True]).all()
        True
        
        >>> Pipeline([True, False, True]).all()
        False
        """
        return all(self)
    
    def contains(self, item: T) -> bool:
        """
        >>> Pipeline([1, 2, 3]).contains(2)
        True
        
        >>> Pipeline([1, 2, 3]).contains(4)
        False
        """
        return item in self

if __name__ == "__main__":
    # Interpreter usage: 
    # from importlib import reload; import oa_utils.pipeline; reload(oa_utils.pipeline); from oa_utils.pipeline import Pipeline
    import doctest
    doctest.testmod()
    