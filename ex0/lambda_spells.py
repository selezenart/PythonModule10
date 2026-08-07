from typing import Any


def artifact_sorter(artifacts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(artifacts, key=lambda a: a['power'], reverse=True)


def power_filter(
        mages: list[dict[str, Any]],
        min_power: int) -> list[dict[str, Any]]:
    return list(filter(lambda a: a["power"] >= min_power, mages))


def spell_transformer(spells: list[str]) -> list[str]:
    return list(map(lambda a: f"* {a} *", spells))


def mage_stats(mages: list[dict[str, Any]]) -> dict[str, Any]:
    powers = list(map(lambda m: m['power'], mages))
    return {
        "max_power": max(powers),
        "min_power": min(powers),
        "avg_power": round(sum(powers) / len(powers), 2),
    }


if __name__ == "__main__":
    import os
    import sys

    sys.path.insert(
        0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from data_generator import FuncMageDataGenerator

    artifacts = FuncMageDataGenerator.generate_artifacts(4)
    spells = FuncMageDataGenerator.generate_spells(3)

    print("Testing artifact sorter...")
    ranked = artifact_sorter(artifacts)
    print(f"{ranked[0]['name']} ({ranked[0]['power']} power) comes before "
          f"{ranked[1]['name']} ({ranked[1]['power']} power)")

    print("Testing spell transformer...")
    print(" ".join(spell_transformer(spells)))
