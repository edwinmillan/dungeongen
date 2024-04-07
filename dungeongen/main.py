import random
from gate import ERankGate, DRankGate, CRankGate, BRankGate, ARankGate, SRankGate
from chat import send_prompt
from tqdm import tqdm


def display_menu():

    print("Please select a gate to generate an encounter:")
    print("E - E Rank Gate")
    print("D - D Rank Gate")
    print("C - C Rank Gate")
    print("B - B Rank Gate")
    print("A - A Rank Gate")
    print("S - S Rank Gate")
    print("---")
    print("R - Random Gate")
    print("H - Display these options again")
    print("Q - Quit the Dungeon Generator")


def display_encounter(encounter: dict):
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


def menu_loop():
    gates = {
        "E": ERankGate(),
        "D": DRankGate(),
        "C": CRankGate(),
        "B": BRankGate(),
        "A": ARankGate(),
        "S": SRankGate(),
    }
    while True:
        # Get user input
        gate_choice = input("Enter your choice: ").strip().upper()

        # Generate encounter based on user's choice
        match gate_choice:
            case "E" | "D" | "C" | "B" | "A" | "S":
                gate = gates[gate_choice]
            case "R":
                gate = random.choice(list(gates.values()))
            case "Q":
                print("Goodbye!")
                break
            case "H":
                display_menu()
                continue
            case _:
                print("Invalid choice. Please try again.")
                continue

        encounter = gate.generate_encounters()
        # print("Encounter generated:", encounter)
        # display_encounter(encounter)

        chat_response = send_prompt(
            f"Describe the environment without giving your own commentary of a Solo Leveling gate based on the following encounter data: {encounter}"
        )
        print(chat_response)


def main():
    print("Welcome to the Dungeon Generator!")
    display_menu()
    menu_loop()
    print("Exiting...")


if __name__ == "__main__":
    main()
