from typing import Literal

LiteralType = Literal["test1", "test2"]

class Dog:
    name: str
    age: int
    barks: bool


def get_dog():
    return Dog(name="Rex", age=3, barks=True)

def get_dog_with_input(input_literal: LiteralType):
    return {
        "input": input_literal,
        "dog": get_dog(),
    }

class Donkey:
    @staticmethod
    def get_by_saddle(size: int) -> "Donkey":
        return Donkey()
    
class AsyncDonkey:
    @staticmethod
    async def get_by_saddle(size: int) -> tuple["AsyncDonkey", "AsyncDonkey"]:
        return AsyncDonkey(), AsyncDonkey()