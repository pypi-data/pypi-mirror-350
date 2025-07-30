from ..matching import validate_is_equivalent_type
from type_less.inference import guess_return_type
from typing import TypeVar, Generic, Type

T = TypeVar("T")
def get_item(item: T) -> T:
    return item

class Base:
    @classmethod
    def create(cls: Type[T]) -> T:
        return cls()
    
class Child(Base):
    pass

def test_typevar_int():
    def func():
        value = get_item(42)
        return value
    
    assert guess_return_type(func, use_literals=False) == int

def test_typevar_inherited_class():

    def func():
        value = Child.create()
        return value
    
    assert guess_return_type(func, use_literals=False) == Child