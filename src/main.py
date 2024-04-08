import asyncio
import itertools
import random
from os import getenv

from dotenv import load_dotenv

from src.chat import send_prompt
from src.compendium import Compendium
from src.gate import ARankGate, BRankGate, CRankGate, DRankGate, ERankGate, SRankGate

load_dotenv()


def display_menu(chat_narration: bool) -> None:

    print("Please select a gate to generate an encounter:")
    print("E - E Rank Gate")
    print("D - D Rank Gate")
    print("C - C Rank Gate")
    print("B - B Rank Gate")
    print("A - A Rank Gate")
    print("S - S Rank Gate")
    print("---")
    print("R - Random Gate")
    print(
        f"N - Toggle chat narration (currently {'enabled' if chat_narration else 'disabled'})"
    )
    print("H - Display these options again")
    print("Q - Quit the Dungeon Generator")


def display_encounter(encounter: dict) -> None:
    print("Encounter generated:")
    print(f"Rank: {encounter.get('rank')}")

    monsters = encounter.get("monsters", [])
    monster_count = sum(map(lambda m: m.get("wave_size"), monsters))
    wave_count = len(monsters)

    print(f"Monsters: Total: {monster_count}, Waves: {wave_count}")

    for monster in monsters:
        print(
            f"  - Wave {monster.get('wave')} {monster.get('monster')} x{monster.get('wave_size')}"
        )
    print(f"Boss: {encounter.get('boss')}")


async def spinner_function(description: str) -> None:
    for char in itertools.cycle(["|", "/", "-", "\\"]):
        if not asyncio.current_task().cancelled():
            print(f"\r{description}: {char}", end="", flush=True)
            await asyncio.sleep(0.1)
        else:
            break


async def send_prompt_with_spinner(prompt: str) -> str:
    spinner = asyncio.create_task(spinner_function("Waiting for Chat response"))
    result = await send_prompt(prompt)
    spinner.cancel()
    print(" Done!")
    return result


def parse_boolean(value: str | bool) -> bool:
    if value is True or value is False:
        return value
    elif value.lower() in ("true", "1", "yes"):
        return True
    elif value.lower() in ("false", "0", "no"):
        return False
    else:
        raise ValueError(f"Cannot convert {value} to boolean")


def menu_loop():
    base_url = getenv("COMPENDIUM_URL")
    chat_narration: bool = parse_boolean(getenv("CHAT_NARRATION", False))

    compendium = Compendium(base_url=base_url)

    gates = {
        "E": ERankGate(compendium=compendium),
        "D": DRankGate(compendium=compendium),
        "C": CRankGate(compendium=compendium),
        "B": BRankGate(compendium=compendium),
        "A": ARankGate(compendium=compendium),
        "S": SRankGate(compendium=compendium),
    }
    display_menu(chat_narration=chat_narration)
    while True:
        # Get user input
        gate_choice = input("Enter your choice: ").strip().upper()

        # Generate encounter based on user's choice
        match gate_choice:
            case "E" | "D" | "C" | "B" | "A" | "S":
                gate = gates[gate_choice]
            case "N":
                chat_narration = not chat_narration
                print(
                    f"Chat narration is now {'enabled' if chat_narration else 'disabled'}"
                )
                continue
            case "R":
                gate = random.choice(list(gates.values()))
            case "Q":
                print("Goodbye!")
                break
            case "H":
                display_menu(chat_narration=chat_narration)
                continue
            case _:
                print("Invalid choice. Please try again.")
                continue

        encounter = gate.generate_encounters()
        # print("Encounter generated:", encounter)
        display_encounter(encounter)

        if chat_narration:
            chat_response = asyncio.run(
                send_prompt_with_spinner(
                    f"Describe the environment without giving your own commentary or analysis. Describe a pocket dimension's environment based on the following encounter data. Don't refer to the pocket dimension in your description. All the following information should be present in the response: {encounter}"
                )
            )

            print(chat_response)


def main():
    print("Welcome to the Dungeon Generator!")
    menu_loop()
    print("Exiting...")


if __name__ == "__main__":
    main()
