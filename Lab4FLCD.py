import string


class Transition:

    def __init__(self, state, value, resultedState):
        self.__state = state
        self.__value = value
        self.__resultedState = resultedState

    @property
    def state(self):
        return self.__state
    @state.setter
    def state(self, value):
        self.__state = value

    @property
    def value(self):
        return self.__value
    @value.setter
    def value(self, val):
        self.__value = val

    @property
    def resultedState(self):
        return self.__resultedState
    @resultedState.setter
    def resultedState(self, value):
        self.__resultedState = value

    def __str__(self):
        return '(' + self.__state.__str__() + ", " + self.__value.__str__() + ") -> " + self.__resultedState.__str__()


class FiniteAutomata():

    def __init__(self):
        self.__initialState = 0
        self.__setOfStates = set()
        self.__alphabet = set()
        self.__transitions:[Transition] = [ ]
        self.__setOfFinalStates = set()

    @property
    def initialState(self):
        return self.__initialState
    @property
    def setOfStates(self):
        return self.__setOfStates
    @property
    def alphabet(self):
        return self.__alphabet
    @property
    def transitions(self):
        return self.__transitions
    @property
    def setOfFinalStates(self):
        return self.__setOfFinalStates

    def setStates(self, value):
        self.__setOfStates = value
    def setAlphabet(self, value):
        self.__alphabet = value
    def setInitialState(self, value):
        self.__initialState = value
    def setFinalStates(self, value):
        self.__setOfFinalStates = value
    def setTransitions(self, value):
        self.__transitions = value

    def __str__(self):
        result = ''
        result = result + 'Q = ' + self.__setOfStates.__str__() + "\n"
        result = result + 'sigma = ' + self.__alphabet.__str__() + "\n"
        result = result + 'q0 = ' + self.__initialState.__str__() + "\n"
        result = result + 'F = ' + self.__setOfFinalStates.__str__() + "\n"
        result = result + 'transitions = {'
        for i in range(0, len(self.__transitions)):
            if i != len(self.__transitions) - 1:
                result = result + self.__transitions[i].__str__() + ";\n"
            else:
                result = result + self.__transitions[i].__str__() + ";}"
        return result

    def getTransitionsOfSpecifiedStateAndValue(self, state, value):
        result = [ ]
        for transition in self.__transitions:
            if transition.state == state and str(transition.value) == str(value):
                result.append(transition.resultedState)
        return result

    def verifySequence(self, sequence):
        position = 0
        queue = [[self.__initialState, position]]
        while position < len(sequence) and len(queue) > 0:
            currentState, position = queue.pop(0)
            if position == len(sequence)  and currentState in self.__setOfFinalStates:
                return True
            if position == len(sequence) and len(queue) == 0:
                return False
            result = self.getTransitionsOfSpecifiedStateAndValue(currentState, sequence[position])
            if result != None:
                for i in result:
                    queue.append([i, position + 1])
        return False

class Handler:

    def __init__(self, filename):
        self.__filename = filename

    def printMenu(self):
        print('Menu:')
        print('1 -> Display the set of states !')
        print('2 -> Display the alphabet !')
        print('3 -> Display the initial state !')
        print('4 -> Display the final states !')
        print('5 -> Display the list of transitions !')
        print('6 -> Verify if is a valid sequence !')

    def createSet(self, line : string, f):
        line = line[ line.find('{') + 1: line.find('}')]
        line = line.strip()
        elements = line.split(', ')
        return set(elements)

    def createElement(self, line : string, f):
        return line.strip()

    def createTransitions(self, line : string, f):
        result = [ ]
        while (line.find('}') < 0):
            if line != '{':
                line = line[ line.find('{') + 1 : line.find(';')]
                resultedState = line[line.find('->') + 2: ].strip()
                state, value = line[line.find('(') + 1 : line.find(')')].split(', ')
                transition = Transition(state, value, resultedState)
                result.append(transition)
            line = f.readline()
        return result

    def createFiniteAutomata(self):
        finiteAutomata = FiniteAutomata()
        symbols = { 'Q' : [self.createSet, getattr(finiteAutomata, 'setStates')],
                    'sigma' : [self.createSet, getattr(finiteAutomata, 'setAlphabet')],
                    'q0' : [self.createElement, getattr(finiteAutomata, 'setInitialState')],
                    'F' : [self.createSet, getattr(finiteAutomata, 'setFinalStates')],
                    'transitions' : [self.createTransitions, getattr(finiteAutomata, 'setTransitions')]}
        file = open(self.__filename, 'r')
        for i in range(0, 5):
            line = file.readline().split('=')
            result = symbols[line[0].strip()][0](line[1].strip(), file)
            function = symbols[line[0].strip()][1]
            function(result)
        return finiteAutomata

    def run(self):
        finiteAutomata = self.createFiniteAutomata()
        self.printMenu()
        while True:
            command = input("Give a command, please: ")
            if command == 'x':
                print('exit')
                break
            if command not in ['1', '2', '3', '4', '5', '6']:
                print('Invalid command !')
                continue
            if command == '1':
                print('Set of states: ' + finiteAutomata.setOfStates.__str__())
            if command == '2':
                print('Alphabet: ' + finiteAutomata.alphabet.__str__())
            if command == '3':
                print('Initial state: ' + finiteAutomata.initialState.__str__())
            if command == '4':
                print('Set of final states: ' + finiteAutomata.initialState.__str__())
            if command == '5':
                result = 'Transitions: {'
                transitions = finiteAutomata.transitions
                for i in range(0, len(transitions)):
                    if i != len(transitions) - 1:
                        result = result + transitions[i].__str__() + ";\n"
                    else:
                        result = result + transitions[i].__str__() + ";}"
                print(result)
            if command == '6':
                sequence = input('Give the sequence: ')
                print(finiteAutomata.verifySequence(sequence))





if __name__ == "__main__":
    handler = Handler("fa.txt")
    handler.run()
