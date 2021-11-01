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
    @resultedState
    def resultedState(self, value):
        self.__resultedState = value


class FiniteAutomata():

    def __init__(self, initialState):
        self.__initialState = initialState
        self.__setOfStates = set()
        self.__alphabet = [ ]
        self.__transitions:[Transition] = [ ]
        self.__setOfFinalStates = set()

    @property
    def initialState(self):
        return self.__initialState
    @initialState.setter
    def initialState(self, value):
        self.__initialState = value

    @property
    def setOfStates(self):
        return self.__setOfStates
    @setOfStates.setter
    def setOfStates(self, value):
        self.__setOfStates = value

    @property
    def alphabet(self):
        return self.__alphabet
    @alphabet.setter
    def alphabet(self, value):
        self.__alphabet = value

    @property
    def transitions(self):
        return self.__transitions
    @transitions.setter
    def transitions(self, value):
        self.__transitions = value

    @property
    def setOfFinalStates(self):
        return self.__setOfFinalStates
    @setOfFinalStates.setter
    def setOfFinalStates(self, value):
        self.__setOfFinalStates = value

class Handler:

    def __init__(self, filename):
        self.__filename = filename

    def readFromFile(self):
        file = open(self.__filename, 'r')
        initialState = ''
