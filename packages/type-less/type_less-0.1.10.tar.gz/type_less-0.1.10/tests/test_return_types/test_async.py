import pytest
from ..matching import validate_is_equivalent_type
from type_less.inference import guess_return_type
from typing import Awaitable, Literal, TypedDict, Type, TypeVar, Union


MODEL = TypeVar("MODEL", bound="Animal")
class Animal:
    @classmethod
    async def create(cls: Type[MODEL]) -> MODEL:
        return cls()
    

class Cat(Animal):
    color: Literal["black", "orange"]
    has_ears: bool
    

class Collar:
    cat: Awaitable[Cat]



# Async

async def get_cat_async() -> Cat:
    return Cat(color="black", has_ears=True)

@pytest.mark.asyncio
async def test_guess_return_type_follow_function_return_async():
    class TheCatReturns(TypedDict):
        color: Literal["black", "orange"]
        has_ears: bool

    async def func():
        cat = await get_cat_async()
        return {
            "color": cat.color,
            "has_ears": cat.has_ears,
        }
    
    assert validate_is_equivalent_type(guess_return_type(func), TheCatReturns)

# Static method

class FeatureA:
    thingo: int

    @staticmethod
    async def run_me() -> tuple["FeatureA", "FeatureB"]:
        return FeatureA(), FeatureB()


class FeatureB:
    thingo: bool


@pytest.mark.asyncio
async def test_guess_return_type_follow_function_return_async():
    async def func():
        fa, fb = await FeatureA.run_me()
        return fb, fa
    
    assert validate_is_equivalent_type(guess_return_type(func), tuple[FeatureB, FeatureA])

# Inherited


@pytest.mark.asyncio
async def test_inherited_typevar_async_method():
    async def func():
        cat = await Cat.create()
        return cat
    
    assert validate_is_equivalent_type(guess_return_type(func), Cat)

@pytest.mark.asyncio
async def test_awaitable_member_variable():
    async def func():
        collar = Collar()
        cat = await collar.cat
        return cat
    
    assert validate_is_equivalent_type(guess_return_type(func), Cat)

