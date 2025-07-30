from ..matching import validate_is_equivalent_type
from type_less.inference import guess_return_type
from typing import Literal, TypedDict


class TestCat:
    color: Literal["black", "orange"]
    has_ears: bool


# Subscript

def get_cats_list() -> list[TestCat]:
    return [TestCat(color="black", has_ears=True)]

def test_guess_return_type_follow_function_return_list_item():
    class TheCatReturns(TypedDict):
        color: Literal["black", "orange"]
        has_ears: bool

    def func():
        cat = get_cats_list()[0]
        return {
            "color": cat.color,
            "has_ears": cat.has_ears,
        }
    
    assert validate_is_equivalent_type(guess_return_type(func), TheCatReturns)



def get_cats_dict() -> dict[str, TestCat]:
    return {"base": TestCat(color="black", has_ears=True)}

def test_guess_return_type_follow_function_return_dict_item():
    class TheCatReturns(TypedDict):
        color: Literal["black", "orange"]
        has_ears: bool

    def func():
        cat = get_cats_dict()["base"]
        return {
            "color": cat.color,
            "has_ears": cat.has_ears,
        }
    
    assert validate_is_equivalent_type(guess_return_type(func), TheCatReturns)



def get_cats_dict_list() -> dict[str, list[TestCat]]:
    return {"base": [TestCat(color="black", has_ears=True)]}

def test_guess_return_type_follow_function_return_dict_list_item():
    class TheCatReturns(TypedDict):
        color: Literal["black", "orange"]
        has_ears: bool

    def func():
        cat = get_cats_dict_list()["base"][0]
        return {
            "color": cat.color,
            "has_ears": cat.has_ears,
        }
    
    assert validate_is_equivalent_type(guess_return_type(func), TheCatReturns)
