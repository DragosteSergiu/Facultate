import copy


class Rule:
    def __init__(self, leftSide='', rightSide=[]):
        self.__left_side = leftSide
        self.__right_side = rightSide

    def get_left_side(self):
        return self.__left_side

    def set_left_side(self, value):
        self.__left_side = value

    def get_right_side(self):
        return self.__right_side

    def set_right_side(self, value):
        self.__right_side = value

    def add_to_right_side(self, element):
        self.__right_side.append(element)

    def __str__(self):
        result = self.__left_side + " -> "
        for element in self.__right_side:
            result = result + element
        return result

    def __eq__(self, other):
        if other is self:
            return True

        if type(other) is not type(self):
            # delegate to superclass
            return NotImplemented
        valid = True
        other_rightSide = other.get_right_side()
        for rule in self.__right_side:
            if rule not in other_rightSide:
                valid = False
        for rule in other_rightSide:
            if rule not in self.__right_side:
                valid = False
        return self.get_left_side() == other.get_left_side() and valid

    def reset(self):
        self.__left_side = ''
        self.__right_side = []


class Grammar:

    def __init__(self):
        self.__non_terminals = set()
        self.__terminals = set()
        self.__productions: [Rule] = []
        self.__start_symbol = None

    def is_valid_rule(self, rule):
        for i in range(0, len(rule)):
            if rule[i] not in self.__terminals and rule[i] not in self.__non_terminals:
                return False
        return True

    def get_non_terminals(self):
        return self.__non_terminals

    def get_terminals(self):
        return self.__terminals

    def get_productions(self):
        return self.__productions

    def get_start_symbol(self):
        return self.__start_symbol

    def set_non_terminals(self, value):
        self.__non_terminals = value

    def set_terminals(self, value):
        self.__terminals = value

    def set_productions(self, value):
        self.__productions = value

    def set_start_symbol(self, value):
        self.__start_symbol = value

    def get_production_for_specific_left_side(self, value):
        result = []
        for prod in self.__productions:
            if prod.get_left_side() == value:
                result.append(prod)
        return result

    def get_position_of_a_rule(self, left_side, right_side):
        position = 0
        for rule in self.__productions:
            if rule.get_left_side() == left_side and rule.get_right_side() == right_side:
                return position
            position += 1
        return -1

    def insert_rule(self, position, rule):
        self.__productions.insert(position, rule)

    def create_sets(self, line, file):
        line = line[line.find('{') + 1: line.find('}')]
        result = set()
        tokens = line.split(", ")
        for token in tokens:
            if token not in result:
                result.add(token.strip())
        return result

    def create_productions(self, line, file):
        result = []
        while line.find('}') < 0:
            if line != '{':
                position = line.find('->')
                startSymbol = line[: position]
                tokens = line[position + 2:]
                elements = tokens.split('|')
                for elem in elements:
                    rule = Rule(startSymbol.strip(), [])
                    modifiedRule = elem.strip()
                    if self.is_valid_rule(modifiedRule):
                        for i in range(0, len(modifiedRule)):
                            rule.add_to_right_side(modifiedRule[i])
                    if len(rule.get_right_side()) > 0:
                        result.append(copy.deepcopy(rule))
                    # rule.reset()

            line = file.readline()
        return result

    def create_start_symbol(self, line, file):
        return line.strip()

    def is_context_free_grammar(self):
        for production in self.__productions:
            if production.get_left_side() not in self.__non_terminals:
                return False
        return True

    def __str__(self):
        result = 'non-terminals = {'
        toList = list(self.__non_terminals)
        for i in range(0, len(toList)):
            if i != len(toList) - 1:
                result = result + str(toList[i]) + ","
            else:
                result = result + str(toList[i]) + "}\n"
        result = result + "terminals = {"
        toList = list(self.__terminals)
        for i in range(0, len(toList)):
            if i != len(toList) - 1:
                result = result + str(toList[i]) + ","
            else:
                result = result + str(toList[i]) + "}\n"
        result = result + "start symbol = {" + str(self.__start_symbol) + "}\n"
        result = result + "productions = {"
        toList = list(self.__productions)
        for i in range(0, len(toList)):
            if i != len(toList) - 1:
                result = result + toList[i].__str__() + ";\n"
            else:
                result = result + toList[i].__str__() + "}\n"
        return result

    def read_grammar(self, filename):
        file = open(filename, 'r')
        map = {
            "nonTerminals": [self.create_sets, self.set_non_terminals],
            "terminals": [self.create_sets, self.set_terminals],
            "startSymbol": [self.create_start_symbol, self.set_start_symbol],
            "productions": [self.create_productions, self.set_productions]
        }
        for i in range(0, 4):
            line = file.readline().split('=')
            result = map[line[0].strip()][0](line[1].strip(), file)
            map[line[0].strip()][1](result)
        if not self.is_context_free_grammar():
            print('It is not a context free grammar')
        # print(self.__str__())


if __name__ == '__main__':
    grammar = Grammar()
    grammar.read_grammar("g1.txt")
