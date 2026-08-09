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
        return f"Unknown spell type: {type(spell).__name__}"

    @cast.register
    def _cast_int(spell: int) -> str:
        return f"Damage spell dealing {spell} damage"

    @cast.register
    def _cast_str(spell: str) -> str:
        return f"Enchantment cast: {spell}"

    @cast.register
    def _cast_list(spell: list) -> str:
        return "Multi-cast: " + " | ".join(cast(item) for item in spell)

    return cast
