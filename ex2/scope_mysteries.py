from typing import Callable


def mage_counter() -> Callable:
    count = 0

    def counter() -> int:
        nonlocal count
        count += 1
        return count

    return counter


def spell_accumulator(initial_power: int) -> Callable:
    total = initial_power

    def accumulate(amount: int) -> int:
        nonlocal total
        total += amount
        return total

    return accumulate


def enchantment_factory(enchantment_type: str) -> Callable:
    def enchant(item_name: str) -> str:
        return f"{enchantment_type} {item_name}"

    return enchant


def memory_vault() -> dict[str, Callable]:
    memory: dict = {}

    def store(key, value) -> None:
        memory[key] = value

    def recall(key):
        return memory.get(key, "Memory not found")

    return {"store": store, "recall": recall}


if __name__ == "__main__":
    import os
    import random
    import sys

    sys.path.insert(
        0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from data_generator import FuncMageDataGenerator

    base, add1, add2 = FuncMageDataGenerator.generate_spell_powers(3)
    types = random.sample(FuncMageDataGenerator.ENCHANTMENT_TYPES, 2)
    items = FuncMageDataGenerator.generate_enchantment_items(2)
    mage = FuncMageDataGenerator.generate_mages(1)[0]

    print("Testing mage counter...")
    counter_a = mage_counter()
    counter_b = mage_counter()
    print(f"counter_a call 1: {counter_a()}")
    print(f"counter_a call 2: {counter_a()}")
    print(f"counter_b call 1: {counter_b()}")

    print("Testing spell accumulator...")
    accumulate = spell_accumulator(base)
    print(f"Base {base}, add {add1}: {accumulate(add1)}")
    print(f"Base {base}, add {add2}: {accumulate(add2)}")

    print("Testing enchantment factory...")
    for enchantment, item in zip(types, items):
        print(enchantment_factory(enchantment)(item))

    print("Testing memory vault...")
    vault = memory_vault()
    vault["store"](mage["name"], mage["power"])
    print(f"Store '{mage['name']}' = {mage['power']}")
    print(f"Recall '{mage['name']}': {vault['recall'](mage['name'])}")
    print(f"Recall 'unknown': {vault['recall']('unknown')}")
