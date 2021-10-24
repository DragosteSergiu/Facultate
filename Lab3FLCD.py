from Lab2FLCD import *
import re

TOKEN_PATH = 'token.in'
TOKENS = {}
SEPARATORS = []
keywords = ['var', 'read', 'write', 'if', 'while', 'begin', 'end']

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
        for key in TOKENS:
            if len(key) == 1:
                SEPARATORS.append(key)
        f.close()

    def updatePIF(self, firstTable: SortedTable, secondTable: list):
        result = [ ]
        for elem in secondTable:
            ok = True
            for key in firstTable:
                if key.token == elem.token:
                    ok = False
                    newElem = PElement(elem.token, elem.valueInTokens, key.position)
                    result.append(newElem)
            if ok == True:
                result.append(elem)
        return result
                    #print(elem.positionInTokens)
        #print("-----------------------------------------------")


class Error:
    def __init__(self, message):
        self.__message = message

    @property
    def message(self):
        return self.__message
    @message.setter
    def message(self, value):
        self.__message = value



class PElement:
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




class Scanner:
    def __init__(self, FILE_PATH):
        self.__path = FILE_PATH
        self.__handler = Handler(TOKEN_PATH)
        self.__symbolTable = SortedTable()
        self.__PIF = []

    def execute(self):
        self.__handler.readTokens()
        file = open(self.__path, 'r')
        previous = ''
        token = ''
        character = ''
        while True:
            if character != '':
                prevCharacter = character
            character = file.read(1)

            if character in SEPARATORS or character == ' ':
                if token.find('\n') > -1:
                    new = token.strip()
                    token = new
                if previous == 'var' and len(token) > 0 and character in [':']:
                    self.__symbolTable.addElement(token)
                    elem = PElement(token, 0, self.__symbolTable.searchByToken(token))
                    self.__PIF.append(elem)
                    self.__PIF = self.__handler.updatePIF(self.__symbolTable.table, self.__PIF)
                    elem = PElement(character, TOKENS[character], -1)
                    self.__PIF.append(elem)
                    token = ''
                    continue
                if (token == 'read' or token == 'write') and character == '(':
                    elem = PElement(token, TOKENS[token], -1)
                    self.__PIF.append(elem)
                    elem = PElement(character, TOKENS[character], 0)
                    self.__PIF.append(elem)
                    token = ''
                    while 1:
                        prevCharacter = character
                        character = file.read(1)
                        if not character:
                            break
                        if character == ')':
                            if (self.__symbolTable.searchByToken(token) > -1):
                                elem = PElement(token, 0, self.__symbolTable.searchByToken(token))
                                self.__PIF.append(elem)
                                token = ''
                                elem = PElement(character, TOKENS[character], -1)
                                self.__PIF.append(elem)
                                break
                        if character != ' ':
                            token = token + character
                    while 1:
                        prevCharacter = character
                        character = file.read(1)
                        if (character != ' ') and (character != ';'):
                            break
                        if (character == ';'):
                            elem = PElement(character, TOKENS[character], -1)
                            self.__PIF.append(elem)
                            break

                if self.__symbolTable.searchByToken(token) > -1:
                    elem = PElement(token, 0, self.__symbolTable.searchByToken(token))
                    self.__PIF.append(elem)
                    while character == ' ':
                        character = file.read(1)
                    token = character
                    prevCharacter = token
                if (token in TOKENS and token != 'read' and token != 'write') or (prevCharacter+character in TOKENS):
                    if len(token) > 0:
                        elem = PElement(token, TOKENS[token], -1)
                        self.__PIF.append(elem)
                    if token in keywords:
                        previous = token
                    if character != ' ':
                        elem = PElement(character, TOKENS[character], -1)
                        self.__PIF.append(elem)
                    token = ''
            else:
                token = token + character
            if not character:
                break
        file.close()

    @property
    def PIF(self):
        result = [ ]
        for elem in self.__PIF:
            result.append(elem.__str__())
        return result

    def SymbolTableToString(self):
        return self.__symbolTable.toString()




if __name__ == "__main__":
    scanner = Scanner('Program1.txt')
    scanner.execute()
    print("-------------------------------------PIF-------------------------------")
    for i in scanner.PIF:
        print(i)
    print("---------------------------------Symbol Table--------------------------")
    print(scanner.SymbolTableToString())

