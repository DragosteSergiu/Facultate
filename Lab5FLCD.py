class Rule:

    def __init__(self):
        self.__representation = []

    def getRepresentation(self):
        return self.__representation
    def setRepresentation(self, value):
        self.__representation = value
    def addElement(self, element):
        self.__representation.append(element)

class Production:

    def __init__(self, start):
        self.__start = start
        self.__rules:[Rule] = []

    def getStart(self):
        return self.__start
    def setStart(self, value):
        self.__start = value

    def getRules(self):
        return self.__rules
    def setRules(self, value):
        self.__rules = value

    def addRules(self, rule):
        self.__rules.append(rule)

    def __str__(self):
        result = self.__start + " -> "
        for rule in self.__rules:
            elements = rule.getRepresentation()
            for element in elements:
                result = result + element
            result = result + " | "
        return result[: len(result) - 2]

class Grammar:

    def __init__(self):
        self.__nonTerminals = set()
        self.__terminals = set()
        self.__productions: set(Production) = set()
        self.__startSymbol = None

    def isValidRule(self, rule):
        for i in range(0, len(rule)):
            if rule[i] not in self.__terminals and rule[i] not in self.__nonTerminals:
                return False
        return True

    def setNonTerminals(self, value):
        self.__nonTerminals = value
    def setTerminals(self, value):
        self.__terminals = value
    def setProductions(self, value):
        self.__productions = value
    def setStartSymbol(self, value):
        self.__startSymbol = value

    def createSets(self, line, file):
        line = line[line.find('{') + 1: line.find('}')]
        result = set()
        tokens = line.split(", ")
        for token in tokens:
            if token not in result:
                result.add(token.strip())
        return result

    def createProductions(self, line, file):
        result = set()
        while (line.find('}') < 0):
            if line != '{':
                position = line.find('->')
                startSymbol = line[: position]
                tokens = line[position + 2:]
                rules = tokens.split('|')
                production = Production(startSymbol.strip())
                newRule = None
                for rule in rules:
                    modifiedRule = rule.strip()
                    if self.isValidRule(modifiedRule) == True:
                        newRule = Rule()
                        for i in range(0, len(modifiedRule)):
                            newRule.addElement(modifiedRule[i])
                    if newRule != None:
                        production.addRules(newRule)
                result.add(production)
            line = file.readline()
        return result

    def createStartSymbol(self, line, file):
        return line.strip()

    def __str__(self):
        result = 'non-terminals = {'
        toList = list(self.__nonTerminals)
        for i in range(0, len(toList)):
            if i != len(toList) - 1:
                result = result + str(toList[i]) + ","
            else:
                result = result + str(toList[i]) +"}\n"
        result = result + "terminals = {"
        toList = list(self.__terminals)
        for i in range(0, len(toList)):
            if i != len(toList) - 1:
                result = result + str(toList[i]) + ","
            else:
                result = result + str(toList[i]) +"}\n"
        result = result + "start symbol = {" + str(self.__startSymbol) +"}\n"
        result = result + "productions = {"
        toList = list(self.__productions)
        for i in range(0, len(toList)):
            if i != len(toList) - 1:
                result = result + toList[i].__str__() + ";\n"
            else:
                result = result + toList[i].__str__() +"}\n"
        return result


    def readGrammar(self, filename):
        file = open(filename, 'r')
        map = {
            "nonTerminals": [self.createSets, self.setNonTerminals],
            "terminals": [self.createSets, self.setTerminals],
            "startSymbol": [self.createStartSymbol, self.setStartSymbol],
            "productions": [self.createProductions, self.setProductions]
        }
        for i in range(0, 4):
            line = file.readline().split('=')
            result = map[line[0].strip()][0](line[1].strip(), file)
            map[line[0].strip()][1](result)
        print(self.__str__())


if __name__ == '__main__':
    grammar = Grammar()
    grammar.readGrammar("g1.txt")