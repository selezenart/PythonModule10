import operator
from functools import lru_cache, partial, reduce, singledispatch
from typing import Any, Callable

OPERATIONS = {
    "add": operator.add,
    "multiply": operator.mul,
    "max": max,
    "min": min,
}


def spell_reducer(spells: list[int], operation: str) -> int:
    if operation not in OPERATIONS:
        raise ValueError(f"Unknown operation: {operation}")
    if not spells:
        return 0
    return reduce(OPERATIONS[operation], spells)


def partial_enchanter(base_enchantment: Callable) -> dict[str, Callable]:
    return {
        element: partial(base_enchantment, 50, element)
        for element in ("fire", "ice", "lightning")
    }


@lru_cache(maxsize=None)
def memoized_fibonacci(n: int) -> int:
    if n < 2:
        return n
    return memoized_fibonacci(n - 1) + memoized_fibonacci(n - 2)


def spell_dispatcher() -> Callable[[Any], str]:
    @singledispatch
    def cast(spell: Any) -> str:
        return "Unknown spell type"

    @cast.register
    def _cast_int(spell: int) -> str:
        return f"Damage spell: {spell} damage"

    @cast.register
    def _cast_str(spell: str) -> str:
        return f"Enchantment: {spell}"

    @cast.register
    def _cast_list(spell: list) -> str:
        return f"Multi-cast: {len(spell)} spells"

    return cast


if __name__ == "__main__":
    import os
    import sys

    sys.path.insert(
        0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from data_generator import FuncMageDataGenerator

    powers = FuncMageDataGenerator.generate_spell_powers(4)
    spells = FuncMageDataGenerator.generate_spells(3)
    items = FuncMageDataGenerator.generate_enchantment_items(3)

    print("Testing spell reducer...")
    print(f"Sum: {spell_reducer(powers, 'add')}")
    print(f"Product: {spell_reducer(powers, 'multiply')}")
    print(f"Max: {spell_reducer(powers, 'max')}")
    print(f"Min: {spell_reducer(powers, 'min')}")
    print(f"Empty: {spell_reducer([], 'add')}")
    try:
        spell_reducer(powers, "divide")
    except ValueError as error:
        print(f"Unknown operation handled: {error}")

    print("Testing partial enchanter...")

    def base_enchantment(power: int, element: str, target: str) -> str:
        return f"{element.title()} {target} (+{power} power)"

    enchanters = partial_enchanter(base_enchantment)
    for (element, enchant), item in zip(enchanters.items(), items):
        print(f"{element}: {enchant(item)}")

    print("Testing memoized fibonacci...")
    for step in (0, 1, 10, 15):
        print(f"Fib({step}): {memoized_fibonacci(step)}")
    print(f"Cache after warm-up: {memoized_fibonacci.cache_info()}")

    print("Testing spell dispatcher...")
    cast_spell = spell_dispatcher()
    print(cast_spell(powers[0]))
    print(cast_spell(spells[0]))
    print(cast_spell(spells))
    print(cast_spell(3.14))
