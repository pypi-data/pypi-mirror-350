from ..matching import validate_is_equivalent_type
from type_less.inference import guess_return_type
from typing import Awaitable, Literal, TypedDict, Type, TypeVar, Union


def test_guess_return_type_dict():
    def func():
        return {"key": "value"}
    
    assert guess_return_type(func) == dict


def test_guess_return_type_list():
    def func():
        return [1, 2, 3]
    
    assert guess_return_type(func, use_literals=False) == list[int]


def test_guess_return_type_list_literals():
    def func():
        return [1, 2, 3]
    
    assert guess_return_type(func) == list[Union[Literal[1], Literal[2], Literal[3]]]


def test_guess_return_type_string():
    def func():
        return "hello world"
    
    assert guess_return_type(func, use_literals=False) == str


def test_guess_return_type_int():
    def func():
        return 42
    
    assert guess_return_type(func, use_literals=False) == int


def test_guess_return_type_float():
    def func():
        return 3.14
    
    assert guess_return_type(func, use_literals=False) == float


def test_guess_return_type_bool():
    def func():
        return True
    
    assert guess_return_type(func, use_literals=False) == bool


def test_guess_return_type_none():
    def func():
        return None
    
    assert guess_return_type(func, use_literals=False) == type(None)


TestLiteralType = Literal["test1", "test2"]
def test_guess_return_type_root_literal():
    def func():
        literally_something: TestLiteralType = "test1"
        return literally_something
    
    assert guess_return_type(func, use_literals=False) == TestLiteralType


def test_guess_return_type_inline_literal():
    def func():
        literally_something: Literal["test1", "test2"] = "test1"
        return literally_something
    
    assert guess_return_type(func, use_literals=False) == Literal["test1", "test2"]


def test_guess_return_type_multiple_returns():
    def func(x):
        if x > 0:
            return "positive"
        else:
            return "negative"

    assert guess_return_type(func) == Literal["positive"] | Literal["negative"]

def test_guess_return_type_dict():
    def func(x):
        return {
            "name": "tester",
            "age": 123,
        }
    
    class FuncReturn(TypedDict):
        name: str
        age: int

    assert validate_is_equivalent_type(guess_return_type(func, use_literals=False), FuncReturn)


def test_guess_return_type_complex_fuzzy():
    def func(x):
        if x > 10:
            return {"result": "large"}
        elif x > 0:
            return {"result": "small"}
        else:
            return {"result": "negative"}
    
    class FuncReturn1(TypedDict):
        result: str
    class FuncReturn2(TypedDict):
        result: str
    class FuncReturn3(TypedDict):
        result: str

    assert validate_is_equivalent_type(guess_return_type(func, use_literals=False), Union[FuncReturn1, FuncReturn2, FuncReturn3])


def test_guess_return_type_complex_literals():
    def func(x):
        if x > 10:
            return {"result": "large"}
        elif x > 0:
            return {"result": "small"}
        else:
            return {"result": "negative"}
    
    class FuncReturn1(TypedDict):
        result: Literal["large"]
    class FuncReturn2(TypedDict):
        result: Literal["small"]
    class FuncReturn3(TypedDict):
        result: Literal["negative"]

    assert validate_is_equivalent_type(guess_return_type(func), Union[FuncReturn1, FuncReturn2, FuncReturn3])


class TestCat:
    color: Literal["black", "orange"]
    has_ears: bool

def test_guess_return_type_follow_class_members():
    class TheCatReturns(TypedDict):
        color: Literal["black", "orange"]
        has_ears: bool

    def func(cat: TestCat):
        return {
            "color": cat.color,
            "has_ears": cat.has_ears,
        }
    
    assert validate_is_equivalent_type(guess_return_type(func), TheCatReturns)


def it_makes_two() -> tuple[int, str]:
    return 1, "hello"

def test_guess_tuple_return():
    class ExpectedTwo(TypedDict):
        a: int
        b: str

    def func(cat: TestCat):
        a, b = it_makes_two()
        return {
            "a": a,
            "b": b,
        }
    
    assert validate_is_equivalent_type(guess_return_type(func), ExpectedTwo)