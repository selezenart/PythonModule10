from typing import Callable


def spell(target: str, power: int) -> str:
    return f"Spell strikes {target} for {power} damage"


def spell_combiner(spell1: Callable, spell2: Callable) -> Callable:
    return lambda target, power: (spell1(target, power),
                                  spell2(target, power))


def power_amplifier(base_spell: Callable, multiplier: int) -> Callable:
    return lambda target, power: base_spell(target, power*multiplier)


def conditional_caster(condition: Callable, spell: Callable) -> Callable:
    return lambda target, power: (spell(target, power)
                                  if condition(target, power)
                                  else "Spell fizzled")


def spell_sequence(spells: list[Callable]) -> Callable:
    return lambda target, power: [spell(target, power) for spell in spells]


if __name__ == "__main__":
    import os
    import sys

    sys.path.insert(
        0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from data_generator import FuncMageDataGenerator

    mage = FuncMageDataGenerator.generate_mages(1)[0]
    target, power = mage["name"], mage["power"]

    def fireball(target: str, power: int) -> str:
        return f"Fireball hits {target}"

    def heal(target: str, power: int) -> str:
        return f"Heals {target}"

    def probe(target: str, power: int) -> str:
        return str(power)

    print("Testing spell combiner...")
    combined = spell_combiner(fireball, heal)
    print("Combined spell result:", ", ".join(combined(target, power)))

    print("Testing power amplifier...")
    mega_probe = power_amplifier(probe, 3)
    print(f"Original: {probe(target, power)}, "
          f"Amplified: {mega_probe(target, power)}")

    print("Testing conditional caster...")
    strong_only = conditional_caster(lambda t, p: p >= 50, fireball)
    print(f"Power {power}: {strong_only(target, power)}")
    print(f"Power 10: {strong_only(target, 10)}")

    print("Testing spell sequence...")
    for result in spell_sequence([fireball, heal, spell])(target, power):
        print(f"  {result}")
