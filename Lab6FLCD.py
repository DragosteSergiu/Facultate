from Lab5FLCD import *

class LR0Item(Production):
    def __init__(self, start, rules, dot):
        super(start, rules)
        if dot > 0 and dot < len(rules) - 1:
            self.__dot = dot


if __name__ == "__main__":
    pass