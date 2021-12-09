import string

from Lab5FLCD import *


class Action:

    def __init__(self, name, operand):
        self.__name = name
        self.__operand = operand

    def get_name(self):
        return self.__name

    def set_name(self, value):
        self.__name = value

    def get_operand(self):
        return self.__operand

    def set_operand(self, value):
        self.__operand = value

    def __str__(self):
        return "action " + str(self.__name) + ", operand " + str(self.__operand)


class LR0Item(Rule):

    def __init__(self, left_side, right_side, position):
        super().__init__(left_side, right_side)
        if position <= len(right_side):
            self.__dot_position = position

    def get_left_side(self):
        return super().get_left_side()

    def set_left_side(self, value):
        super().set_left_side(value)

    def get_right_side(self):
        return super().get_right_side()

    def set_right_side(self, value):
        super().set_right_side(value)

    def get_dot_position(self):
        return self.__dot_position

    def set_dot_position(self, value):
        self.__dot_position = value

    def add_to_right_side(self, element):
        super().add_to_right_side(element)

    def get_current_symbol(self):
        if self.__dot_position < len(super().get_right_side()):
            return super().get_right_side()[self.__dot_position]
        return None

    def __str__(self):
        result = super().get_left_side() + " -> "
        for i in range(0, len(super().get_right_side())):
            if i == self.__dot_position:
                result = result + "."
            result = result + str(super().get_right_side()[i])
        if self.__dot_position == len(super().get_right_side()):
            result = result + "."
        return result

    def __eq__(self, other):
        if other is self:
            return True

        if type(other) is not type(self):
            # delegate to superclass
            return NotImplemented
        valid = super().__eq__(other)
        return self.get_dot_position() == other.get_dot_position() and valid

    def __hash__(self):
        return hash(str(self))


class LR0State:

    def __init__(self, state_number, items: [LR0Item]):
        self.__number = state_number
        self.__items: [LR0Item] = items
        self.__transitions: {(LR0Item, string): LR0State} = {}

    def get_state_number(self):
        return self.__number

    def get_items(self):
        return self.__items

    def set_items(self, value: [LR0Item]):
        self.__items = value

    def add_item(self, item: LR0Item):
        self.__items.append(item)

    def get_transitions(self):
        return self.__transitions

    def set_transitions(self, value):
        self.__transitions = value

    def add_transition(self, item, through, state):
        if through is not None and item in self.__items and \
                ((item, through) not in self.__transitions or self.__transitions[(item, through) is None]):
            self.__transitions[(item, through)] = state

    def update_transition(self, item, through, state):
        self.__transitions[(item, through)] = state

    def __str__(self):
        result = "State " + str(self.__number) + "\n"
        result = result + "Items: \n"
        for item in self.__items:
            result = result + item.__str__() + "\n"
        if len(self.__transitions) > 0:
            result = result + "Transitions: \n"
            for transition in self.__transitions:
                if transition[1] is not None and self.__transitions[transition] is not None:
                    result = result + "(" + transition[0].__str__() + ", " + transition[1] + ") -> State " + str(
                        self.__transitions[transition].get_state_number()) + "\n"
        return result

    def __eq__(self, other):
        if other is self:
            return True

        if type(other) is not type(self):
            # delegate to superclass
            return NotImplemented
        valid_items = True
        other_items = other.get_items()
        for item in self.__items:
            if item not in other_items:
                valid_items = False
        for item in other_items:
            if item not in self.__items:
                valid_items = False
        valid_transitions = True
        other_transition = other.get_transitions()
        for key in self.__transitions:
            if key not in other_transition or other_transition[key] != self.__transitions[key]:
                valid_transitions = False
        for key in other_transition:
            if key not in self.__transitions or other_transition[key] != self.__transitions[key]:
                valid_transitions = False
        return valid_items and valid_transitions

    def compare_items(self, items: [LR0Item]):
        for item in self.__items:
            if item not in items:
                return False
        for item in items:
            if item not in self.__items:
                return False
        return True


class LR0Parser:

    def __init__(self, grammar: Grammar):
        self.__grammar = grammar
        self.__canonical_collection: [LR0State] = []
        self.__go_to_table: {(string, string): string} = {}
        self.__action_table: {(string, string): Action} = {}

    def enhance_grammar(self):
        self.__grammar.insert_rule(0, Rule(self.__grammar.get_productions()[0].get_left_side() + "'",
                                           [self.__grammar.get_productions()[0].get_left_side()]))

    def create_canonical_collection(self):
        self.enhance_grammar()
        state_number = 0
        rule = self.__grammar.get_productions()[0]
        queue = [LR0Item(rule.get_left_side(), rule.get_right_side(), 0)]
        while len(queue) > 0:
            currentItem = queue.pop(0)
            items = self.closure(currentItem)
            exists = False
            for i in range(0, len(self.__canonical_collection)):
                if self.__canonical_collection[i].compare_items(items):
                    exists = True
            if not exists:
                state = LR0State(state_number, items)
                state_number += 1
                self.__canonical_collection.append(state)
                for item in items:
                    state.add_transition(item, item.get_current_symbol(), None)
                    modified_item = self.goTo(item)
                    if modified_item is not None:
                        queue.append(modified_item)
        for i in range(0, len(self.__canonical_collection)):
            for j in range(0, len(self.__canonical_collection)):
                i_state = self.__canonical_collection[i]
                j_state = self.__canonical_collection[j]
                i_transitions = i_state.get_transitions()
                for transition in i_transitions:
                    if j_state.compare_items(self.closure(self.goTo(transition[0]))) \
                            and transition[0].get_current_symbol() == transition[1]:
                        self.__canonical_collection[i].update_transition(transition[0], transition[1], j_state)

    def create_go_to_table(self):
        non_terminals = self.__grammar.get_non_terminals()
        for state in self.__canonical_collection:
            transitions = state.get_transitions()
            number = state.get_state_number()
            for transition in transitions:
                if transition[1] in non_terminals:
                    self.__go_to_table[(str(number), transition[1])] = transitions[transition]

    def create_action_table(self):
        terminals = copy.deepcopy(self.__grammar.get_terminals())
        terminals.add("$")
        for state in self.__canonical_collection:
            transitions = state.get_transitions()
            number = state.get_state_number()
            items = state.get_items()
            if len(transitions) == 0:
                if len(items) == 1 and "S'" in items[0].get_left_side():
                    self.__action_table[(str(number), "$")] = Action("ACCEPT", " ")
                elif len(items) == 1 and len(items[0].get_right_side()) == items[0].get_dot_position():
                    for terminal in terminals:
                        self.__action_table[(str(number), terminal)] = Action("REDUCE", str(self.__grammar.get_position_of_a_rule(items[0].get_left_side(), items[0].get_right_side())))
            else:
                for transition in transitions:
                    if transition[1] in terminals:
                        self.__action_table[(str(number), transition[1])] = Action("SHIFT", str(transitions[transition].get_state_number()))

    def closure(self, item: LR0Item):
        result = [item]
        queue = [item]
        while len(queue) > 0:
            currentItem = queue.pop(0)
            symbol = currentItem.get_current_symbol()
            if symbol is not None and symbol in self.__grammar.get_non_terminals():
                new_rules = self.__grammar.get_production_for_specific_left_side(symbol)
                for new_rule in new_rules:
                    new_item = LR0Item(new_rule.get_left_side(), new_rule.get_right_side(), 0)
                    result.append(new_item)
                    queue.append(new_item)
        return result

    def goTo(self, item: LR0Item):
        if item.get_dot_position() == len(item.get_right_side()):
            return None
        return LR0Item(item.get_left_side(), item.get_right_side(), item.get_dot_position() + 1)

    def canonical_collection_to_string(self):
        result = "Canonical collection: \n"
        for state in self.__canonical_collection:
            result = result + state.__str__() + "\n"
        return result

    def go_to_table_to_string(self):
        result = "goTo table: \n"
        non_terminals = list(self.__grammar.get_non_terminals())
        states = self.__canonical_collection
        number_of_states = len(self.__canonical_collection)
        result = self.draw_line(copy.deepcopy(result), len(non_terminals))
        result = result + "|   |"
        for i in range(0, len(non_terminals)):
            result = result + " " + str(non_terminals[i]) + " |"
        result = result + "\n"
        result = self.draw_line(copy.deepcopy(result), len(non_terminals))
        for i in range(0, number_of_states):
            for j in range(0, len(non_terminals) + 1):
                if j == 0:
                    result = result + "| " + str(states[i].get_state_number()) + " |"
                elif j == len(non_terminals):
                    if (str(i), non_terminals[j - 1]) in self.__go_to_table:
                        result = result + " " + str(self.__go_to_table[(str(i), non_terminals[j - 1])].get_state_number()) + " |\n"
                    else:
                        result = result + "   |\n"
                else:
                    if (str(i), non_terminals[j - 1]) in self.__go_to_table:
                        result = result + " " + str(self.__go_to_table[(str(i), non_terminals[j - 1])].get_state_number()) + " |"
                    else:
                        result = result + "   |"
            result = self.draw_line(copy.deepcopy(result), len(non_terminals))
        return result

    def action_table_to_string(self):
        result = "Action table: \n"
        terminals = list(self.__grammar.get_terminals())
        terminals.append("$")
        states = self.__canonical_collection
        number_of_states = len(self.__canonical_collection)
        result = self.draw_line(copy.deepcopy(result), len(terminals))
        result = result + "|   |"
        for i in range(0, len(terminals)):
            result = result + " " + str(terminals[i]) + " |"
        result = result + "\n"
        result = self.draw_line(copy.deepcopy(result), len(terminals))
        for i in range(0, number_of_states):
            for j in range(0, len(terminals) + 1):
                if j == 0:
                    result = result + "| " + str(states[i].get_state_number()) + " |"
                elif j == len(terminals):
                    if (str(i), terminals[j - 1]) in self.__action_table:
                        action = self.__action_table[(str(i), terminals[j - 1])]
                        result = result + " " + str(action.get_name()[0] + action.get_operand()) + "|\n"
                    else:
                        result = result + "   |\n"
                else:
                    if (str(i), terminals[j - 1]) in self.__action_table:
                        action = self.__action_table[(str(i), terminals[j - 1])]
                        result = result + " " + str(action.get_name()[0] + action.get_operand()) + "|"
                    else:
                        result = result + "   |"
            result = self.draw_line(copy.deepcopy(result), len(terminals))
        return result

    def draw_line(self, str, number):
        for i in range(0, number + 1):
            str = str + "----"
        str = str + "-\n"
        return str

if __name__ == "__main__":
    grammar = Grammar()
    grammar.read_grammar("g1.txt")
    parser = LR0Parser(grammar)
    parser.create_canonical_collection()
    parser.create_go_to_table()
    parser.create_action_table()
    #print(parser.canonical_collection_to_string())
    #print(parser.go_to_table_to_string())
    print(parser.action_table_to_string())
