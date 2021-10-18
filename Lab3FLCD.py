from Lab2FLCD import *
import re

TOKEN_PATH = 'token.in'
TOKENS = {}
SEPARATORS = []

def readTokens(TOKEN_PATH):
    f = open(TOKEN_PATH, 'r')
    f.readline()
    i = 1
    for x in f:
        if "\n" in x:
            token = x[0:len(x)-1]
            TOKENS[token] = i
        else:
            TOKENS[x] = i
        i += 1
    for key in TOKENS:
        if len(key) == 1:
            SEPARATORS.append(key)



class PifElement:
    def __init__(self, token, valueInTokens, valueInST):
        self.__token = token
        self.__valueInT = valueInTokens
        self.__valueInST = valueInST

    def getToken(self):
        return self.__token
    def setToken(self, value):
        self.__token = value

    def getValueInT(self):
        return self.__valueInT
    def setValueInT(self, value):
        self.__valueInT = value

    def getValutInST(self):
        return self.__valueInST
    def setValueInST(self, value):
        self.__valueInST = value

    def __str__(self):
        return "token: " + str(self.__token) + ", value in pif: " + str(self.__valueInT) + ", value in st: " + str(self.__valueInST)

def existsInString(key, str):
    position = str.find(key)
    if position < 0:
        return False
    else:
        return True



class Scanner:
    def __init__(self, FILE_PATH):
        self.__filePath = FILE_PATH
        self.__symbolTable = SortedTable()
        self.__pif = []

    def anotherParse(self, character):
        result = [ ]
        f = open(self.__filePath, 'r')
        for x in f:
            parse = re.split(character, x)
            for elem in parse:
                if elem != '':
                    result.append(elem)
        return result

    def parseTable(self, character, table):
        result = [ ]
        for elem in table:
            parse = re.split(character, elem)
            for i in parse:
                result.append(i)
        return result


    def parseFile(self, tokens):
        f = open(self.__filePath, 'r')
        for x in f:
            for key in tokens:
                if existsInString(str(key), x) == True:
                    pifElem = PifElement(key, tokens[key], -1)
                    self.__pif.append(pifElem)

    def getPif(self):
        return self.__pif


if __name__ == "__main__":
    readTokens(TOKEN_PATH)
    scanner = Scanner('Program1.txt')
    result = scanner.anotherParse(' ')
    for separator in SEPARATORS:
        res = scanner.parseTable(separator, result)
        result = res
    print(result)
    #scanner.parseFile(TOKENS)
    #pif = scanner.getPif()
    #for res in pif:
        #print(res.__str__())

