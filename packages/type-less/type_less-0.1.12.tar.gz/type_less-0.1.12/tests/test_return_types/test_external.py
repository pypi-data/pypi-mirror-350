from ..external import Dog, Donkey as Dinkey, get_dog, get_dog_with_input, LiteralType
from .. import external
from ..matching import validate_is_equivalent_type
from type_less.inference import guess_return_type
from typing import TypedDict


# Imported


def test_guess_return_type_imported_function():
    assert validate_is_equivalent_type(guess_return_type(get_dog), Dog)

def test_guess_return_type_called_imported_function():
    class TheDogReturns(TypedDict):
        dog: Dog

    def func():
        dog = get_dog()
        return {
            "dog": dog,
        }
    
    assert validate_is_equivalent_type(guess_return_type(func), TheDogReturns)

def test_guess_return_type_imported_function_args():
    class TheDogReturns(TypedDict):
        input: LiteralType
        dog: Dog

    def func():
        dog = get_dog_with_input("test1")
        return dog
    
    assert validate_is_equivalent_type(guess_return_type(func), TheDogReturns)

def test_guess_return_type_imported_module_function_args():
    class TheDogReturns(TypedDict):
        input: LiteralType
        dog: Dog

    def func():
        dog = external.get_dog_with_input("test1")
        return dog
    
    assert validate_is_equivalent_type(guess_return_type(func), TheDogReturns)


def test_external_static_method_quoted_type_module():
    def func():
        donkey = external.Donkey.get_by_saddle(10)
        return donkey
    
    assert validate_is_equivalent_type(guess_return_type(func), external.Donkey)


def test_external_static_method_quoted_type_renamed():
    def func():
        donkey = Dinkey.get_by_saddle(10)
        return donkey
    
    assert validate_is_equivalent_type(guess_return_type(func), Dinkey)
    