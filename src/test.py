from .fsm import FixedShapeMachine
from .validators import NameValidator, NumberValidator, StringValidator


def main():
    machine = FixedShapeMachine('{"name": "', '"}')
    print(machine.is_complete('{"name": "fn_greet"}'))
    print(machine.is_complete('{"name": "fn_g'))
    print(machine.is_complete('{"name": ""}'))
    print(machine.is_complete('{"name": "x"}'))
    print("hello".startswith(""))

    names = ["test", "hello", "123"]
    name_valid = NameValidator(names)
    numb_valid = NumberValidator()
    str_valid = StringValidator()
    print(name_valid.accept("te"))
    print(name_valid.accept("xd"))
    print(name_valid.is_complete("te"))
    print(name_valid.is_complete("test"))
    print(numb_valid.accept("1230"))
    print(numb_valid.accept("  123  "))
    print(numb_valid.accept(".123"))
    print(str_valid.accept("coiff"))
    print(str_valid.accept('coi"ff'))
    print(str_valid.is_complete("coiff"))
    print(str_valid.accept('"coiff"'))


if __name__ == "__main__":
    main()
