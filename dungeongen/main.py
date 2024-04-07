from gate import ERankGate, DRankGate, CRankGate, BRankGate, ARankGate, SRankGate


def main():
    # egate = ERankGate()
    dgate = DRankGate()
    print(dgate)
    print(dgate.generate_encounters())


if __name__ == "__main__":
    main()
