# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    result.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: dfine <coding@dfine.tech>                  +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/05/23 12:46:18 by dfine             #+#    #+#              #
#    Updated: 2025/05/23 15:38:43 by dfine            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from collections.abc import Callable
from typing import Generic, NoReturn, TypeAlias, TypeVar, final, override

T = TypeVar("T")
U = TypeVar("U")
E = TypeVar("E", default=Exception)
F = TypeVar("F", default=Exception)


@final
class Ok(Generic[T]):
    _value: T
    __match_args__ = ("ok",)
    __slot__ = ("_value",)

    def __init__(self, value: T) -> None:
        self._value = value

    @override
    def __eq__(self, value: object) -> bool:
        if isinstance(value, Ok):
            return self._value == value._value  # pyright: ignore[reportUnknownMemberType,reportUnknownVariableType]
        return False

    @override
    def __hash__(self) -> int:
        return hash(("Ok", self._value))

    @override
    def __repr__(self):
        return f"Ok({self._value!r})"

    @property
    def ok(self) -> T:
        return self._value

    def is_ok(self):
        return True

    def is_err(self):
        return False

    def unwrap(self) -> T:
        return self._value

    def unwrap_or(self, default_value: T) -> T:
        return self._value

    def map(self, func: Callable[[T], U]) -> "Ok[U]":
        return Ok(func(self._value))

    def map_err(self, func: Callable[[E], F]) -> "Ok[T]":
        return self

    def and_then(self, func: Callable[[T], "Ok[U] | Err[F]"]) -> "Ok[U] | Err[F]":
        return func(self._value)

    def or_else(self, func: Callable[[E], "Ok[T] | Err[F]"]) -> "Ok[T]":
        return self

    def unwrap_or_else(self, func: Callable[[E], T]) -> T:
        return self._value

    def inspect(self, func: Callable[[T], None]) -> "Ok[T]":
        func(self._value)
        return self

    def inspect_err(self, func: Callable[[E], None]) -> "Ok[T]":
        return self


class UnwrapError(Exception):
    def __init__(self, msg: str) -> None:
        super().__init__(msg)


@final
class Err(Generic[E]):
    _value: E
    __match_args__ = ("err",)
    __slot__ = ("_value",)

    def __init__(self, error: E) -> None:
        self._value = error

    @override
    def __eq__(self, value: object, /) -> bool:
        if isinstance(value, Err):
            return self._value == value._value
        return False

    @override
    def __hash__(self) -> int:
        return hash(("Err", self._value))

    @override
    def __repr__(self):
        return f"Err({self._value!r})"

    @property
    def err(self) -> E:
        return self._value

    def is_ok(self):
        return False

    def is_err(self):
        return True

    def unwrap(self) -> NoReturn:
        if isinstance(self._value, BaseException):
            raise self._value
        raise UnwrapError(str(self._value))

    def unwrap_or(self, default_value: T) -> T:
        return default_value

    def map(self, func: Callable[[T], U]) -> "Err[E]":
        return self

    def map_err(self, func: Callable[[E], F]) -> "Err[F]":
        return Err(func(self._value))

    def and_then(self, func: Callable[[T], "Ok[U] | Err[F]"]) -> "Err[E]":
        return self

    def or_else(self, func: Callable[[E], "Ok[T] | Err[F]"]) -> "Ok[T] | Err[F]":
        return func(self._value)

    def unwrap_or_else(self, func: Callable[[E], T]) -> T:
        return func(self._value)

    def inspect(self, func: Callable[[T], None]) -> "Err[E]":
        return self

    def inspect_err(self, func: Callable[[E], None]) -> "Err[E]":
        func(self._value)
        return self


Result: TypeAlias = Ok[T] | Err[E]
