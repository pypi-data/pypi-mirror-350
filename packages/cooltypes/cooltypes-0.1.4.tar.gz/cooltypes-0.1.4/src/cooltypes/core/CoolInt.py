import operator
from types import NotImplementedType
from typing import *

__all__ = ["CoolInt"]

OP2 = Self | NotImplementedType


class CoolInt(int):
    "This subclass of int reimplements all the mathematical operators with the return type Self."

    # private methods
    def __op1(self: Self, /, operation: Callable) -> Self:
        "This private method implements unary operators."
        return type(self)(operation(operator.index(self)))

    @classmethod
    def __op2(
        cls: type,
        /,
        operation: Callable,
        left: Any,
        right: Any,
    ) -> OP2:
        "This private classmethod implements binary operators."
        try:
            l: int = operator.index(left)
            r: int = operator.index(right)
        except:
            return NotImplemented
        else:
            return cls(operation(l, r))

    # internal magic

    def __new__(cls: type, value: SupportsInt, /, **kwargs: Any) -> Self:
        "This magic method returns a new instance."
        return super().__new__(cls, value, **kwargs)

    # unary operators

    def __abs__(self: Self, /) -> Self:
        "This magic method implements abs(self)."
        return self.__op1(operator.abs)

    def __invert__(self: Self, /) -> Self:
        "This magic method implements ~self."
        return self.__op1(operator.invert)

    def __neg__(self: Self, /) -> Self:
        "This magic method implements -self."
        return self.__op1(operator.neg)

    def __pos__(self: Self, /) -> Self:
        "This magic method implements +self."
        return self.__op1(operator.pos)

    # normal binary operators
    def __add__(self: Self, other: Any, /) -> OP2:
        "This magic method implements self+other."
        return self.__op2(operator.add, self, other)

    def __and__(self: Self, other: Any, /) -> OP2:
        "This magic method implements self&other."
        return self.__op2(operator.and_, self, other)

    def __divmod__(self: Self, other: Any, /) -> OP2:
        "This magic method implements divmod(self, other)."
        return (self // other), (self % other)

    def __floordiv__(self: Self, other: Any, /) -> OP2:
        "This magic method implements self//other."
        return self.__op2(operator.floordiv, self, other)

    def __lshift__(self: Self, other: Any, /) -> OP2:
        "This magic method implements self<<other."
        return self.__op2(operator.lshift, self, other)

    def __mod__(self: Self, other: Any, /) -> OP2:
        "This magic method implements self%other."
        return self.__op2(operator.mod, self, other)

    def __mul__(self: Self, other: Any, /) -> OP2:
        "This magic method implements self*other."
        return self.__op2(operator.mul, self, other)

    def __or__(self: Self, other: Any, /) -> OP2:
        "This magic method implements self|other."
        return self.__op2(operator.or_, self, other)

    def __pow__(self: Self, other: Any, /) -> OP2:
        "This magic method implements self**other."
        return self.__op2(operator.pow, self, other)

    def __rshift__(self: Self, other: Any, /) -> OP2:
        "This magic method implements self>>other."
        return self.__op2(operator.rshift, self, other)

    def __sub__(self: Self, other: Any, /) -> OP2:
        "This magic method implements self-other."
        return self.__op2(operator.sub, self, other)

    def __xor__(self: Self, other: Any, /) -> OP2:
        "This magic method implements self^other."
        return self.__op2(operator.xor, self, other)

    # reverse binary operators
    def __radd__(self: Self, other: Any, /) -> OP2:
        "This magic method implements other+self."
        return self.__op2(operator.add, other, self)

    def __rand__(self: Self, other: Any, /) -> OP2:
        "This magic method implements other&self."
        return self.__op2(operator.and_, other, self)

    def __rdivmod__(self: Self, other: Any, /) -> OP2:
        "This magic method implements divmod(other, self)."
        return (other // self), (other % self)

    def __rfloordiv__(self: Self, other: Any, /) -> OP2:
        "This magic method implements other//self."
        return self.__op2(operator.floordiv, other, self)

    def __rlshift__(self: Self, other: Any, /) -> OP2:
        "This magic method implements other<<self."
        return self.__op2(operator.lshift, other, self)

    def __rmod__(self: Self, other: Any, /) -> OP2:
        "This magic method implements other%self."
        return self.__op2(operator.mod, other, self)

    def __rmul__(self: Self, other: Any, /) -> OP2:
        "This magic method implements other*self."
        return self.__op2(operator.mul, other, self)

    def __ror__(self: Self, other: Any, /) -> OP2:
        "This magic method implements other|self."
        return self.__op2(operator.or_, other, self)

    def __rpow__(self: Self, other: Any, /) -> OP2:
        "This magic method implements other**self."
        return self.__op2(operator.pow, other, self)

    def __rrshift__(self: Self, other: Any, /) -> OP2:
        "This magic method implements other>>self."
        return self.__op2(operator.rshift, other, self)

    def __rsub__(self: Self, other: Any, /) -> OP2:
        "This magic method implements other-self."
        return self.__op2(operator.sub, other, self)

    def __rxor__(self: Self, other: Any, /) -> OP2:
        "This magic method implements other^self."
        return self.__op2(operator.xor, other, self)
