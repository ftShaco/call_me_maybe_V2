from .fsm import FixedShapeMachine


def main():
    machine = FixedShapeMachine('{"name": "', '"}')
    print(machine.is_complete('{"name": "fn_greet"}'))
    print(machine.is_complete('{"name": "fn_g'))
    print(machine.is_complete('{"name": ""}'))
    print(machine.is_complete('{"name": "x"}'))
    print("hello".startswith(""))


if __name__ == "__main__":
    main()
