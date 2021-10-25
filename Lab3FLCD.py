import string
from Lab2FLCD import *

letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPRSTUVWXYZ'
digits = '0123456789'
nonzerodigits = '123456789'

TOKEN_PATH = 'token.in'
TOKENS = {}
simple_separators = [':', ';', ',', '(', ')', '[', ']', '+', '-', '*', '/', '=', '<', '>']
composed_separators = [':=', '==', '!=', '<=', '>=']
keywords = ['var', 'read', 'write', 'if', 'then','while', 'do', 'begin', 'end']

class Handler:
    def __init__(self, filename):
        self.__filename = filename

    def readTokens(self):
        f = open(self.__filename, 'r')
        f.readline()
        i = 1
        for x in f:
            if "\n" in x:
                token = x[0:len(x) - 1]
                TOKENS[token] = i
            else:
                TOKENS[x] = i
            i += 1
        f.close()

    def updatePIF(self, firstTable, secondTable: list):
        result = [ ]
        for elem in secondTable:
            ok = True
            for key in firstTable:
                if key.token == elem.token:
                    ok = False
                    newElem = PIFElement(elem.token, elem.valueInTokens, key.position)
                    result.append(newElem)
            if ok == True:
                result.append(elem)
        return result

    def parse(self, line:string):
        line = line.strip()
        list = [ ]
        list.extend(keywords)
        list.extend(simple_separators)
        for elem in list:
            position = 0
            while (line.find(elem, position) > -1):
                i = line.find(elem, position)
                line = line[: i] + " " + line[i :]
                i += 1
                line = line[: (i + len(elem))] + " " + line[(i + len(elem)) :]
                position = i + 1
        tokens = line.split()
        i = 0
        while i < len(tokens) - 1:
            operator = tokens[i] + tokens[i+1]
            if operator in composed_separators:
                tokens[i] = tokens[i] + tokens[i+1]
                tokens.pop(i + 1)
            i += 1
        return tokens

    def isValidIdentifier(self, identifier):
        if (identifier[0] != '_' and letters.find(identifier[0]) < 0):
            return False
        i = 1
        while (i < len(identifier)):
            if (identifier[i] != '_' and letters.find(identifier[i]) < 0 and digits.find(identifier[i]) < 0):
                return False
            i += 1
        return True

class Error:
    def __init__(self, message):
        self.__message = message

    @property
    def message(self):
        return self.__message
    @message.setter
    def message(self, value):
        self.__message = value



class PIFElement:
    def __init__(self, token, valueInTokens, valueInST):
        self.__token = token
        self.__valueInTokens = valueInTokens
        self.__valueInSymbolTable = valueInST

    @property
    def token(self):
        return self.__token
    @token.setter
    def token(self, value):
        self.__token = value

    @property
    def valueInTokens(self):
        return self.__valueInTokens
    @valueInTokens.setter
    def valueInTokens(self, value):
        self.__valueInTokens = value

    @property
    def valueInSymbolTable(self):
        return self.__valueInSymbolTable
    @valueInSymbolTable.setter
    def valueInSymbolTable(self, value):
        self.__valueInSymbolTable = value

    def __str__(self):
        return "Token: " + str(self.__token) + " | Value in Tokens: " + str(self.__valueInTokens) + " | Value in Symbol Table: " + str(self.__valueInSymbolTable)


class ProgramInternalForm:

    def __init__(self):
        self.__list:[PIFElement] = [ ]

    @property
    def list(self):
        return self.__list
    @list.setter
    def list(self, value):
        self.__list = value;

    def __str__(self):
        result = ''
        for elem in self.__list:
            result += elem.__str__() +"\n"
        return result

    def addElement(self, element):
        self.__list.append(element)

class Scanner:
    def __init__(self, FILE_PATH):
        self.__path = FILE_PATH
        self.__handler = Handler(TOKEN_PATH)
        self.__symbolTable = SortedTable()
        self.__ProgramInternalForm = ProgramInternalForm()

    def execute(self):
        self.__handler.readTokens()
        file = open(self.__path, 'r')
        for line in file:
            tokens = self.__handler.parse(line)
            for token in tokens:
                added = False
                if token in TOKENS and added == False:
                    element = PIFElement(token, TOKENS[token], -1)
                    self.__ProgramInternalForm.addElement(element)
                    added = True
                if self.__symbolTable.isUniqueToken(token) == True and added == False:
                    if self.__handler.isValidIdentifier(token) == True:
                        self.__symbolTable.addElement(token)
                        element = PIFElement(token, 0, self.__symbolTable.searchByToken(token))
                        self.__ProgramInternalForm.addElement(element)
                        self.__ProgramInternalForm.list = self.__handler.updatePIF(self.__symbolTable.table, self.__ProgramInternalForm.list)
                        added = True
                if self.__symbolTable.isUniqueToken(token) == False and added == False:
                    element = PIFElement(token, 0, self.__symbolTable.searchByToken(token))
                    self.__ProgramInternalForm.addElement(element)
                    added = True

        file.close()

    @property
    def symbolTable(self):
        return self.__symbolTable
    @property
    def ProgramInternalForm(self):
        return self.__ProgramInternalForm




if __name__ == "__main__":
    scanner = Scanner('Program1.txt')
    scanner.execute()

    print("-------------------------------------PIF-------------------------------")
    #for i in scanner.PIF:
        #print(i)
    print(scanner.ProgramInternalForm.__str__())
    print("---------------------------------Symbol Table--------------------------")
    print(scanner.symbolTable.__str__())

