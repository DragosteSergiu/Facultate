#Some constants used in program
letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPRSTUVWXYZ'
digits = '0123456789'
nonzerodigits = '123456789'
variableDeclaration = 'var[ ]*([a-zA-Z_][a-zA-Z_0-9]*)+([ ]*,[ ]*[a-zA-Z_][a-zA-Z_0-9]*)*[ ]*:[ ]*type[ ]*;'
variableDeclarationWithoutVar = '[ ]*([a-zA-Z_][a-zA-Z_0-9]*)+([ ]*,[ ]*[a-zA-Z_][a-zA-Z_0-9]*)*[ ]*:[ ]*type[ ]*;'
TOKEN_PATH = 'token.in'
TOKENS = {}
simple_separators = [':', ';', ',', '(', ')', '[', ']', '+', '-', '*', '/', '=', '<', '>']
composed_separators = [':=', '==', '!=', '<=', '>=']
keywords = ['var', 'read', 'write', 'if', 'then', 'else','while', 'do', 'begin', 'end']
types = ['integer', 'string', 'array']
operators = ['+', '-']

#Imports
import string
import re
from Lab2FLCD import *


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

    def writeInFile(self, filename, string):
        file = open(filename, 'w')
        file.write(string)
        file.close()

    def updateProgramInternalForm(self, firstTable, secondTable: list):
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

    def parse(self, line:string, number, identifiers):
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
        tokens = self.parseComposedSeparators(tokens)
        tokens = self.parseOperatos(tokens)
        listOfErrors = self.verifyErrors(tokens, number, identifiers)
        return tokens, listOfErrors

    def verifyErrors(self, tokens, number, identifiers):
        listOfErrors = ErrorsList()
        error = self.verifyIdentifiers(tokens)
        if error != None:
            error.line = number
            listOfErrors.addError(error)
        error = self.verifyNumberOfParenthesis(tokens)
        if error != None:
            error.line = number
            listOfErrors.addError(error)
        error = self.verifyVariableDeclaration(tokens)
        if error != None:
            error.line = number
            listOfErrors.addError(error)
        error = self.verifyAssign(tokens, identifiers)
        if error != None:
            error.line = number
            listOfErrors.addError(error)
        return listOfErrors

    def verifyAssign(self, tokens, identifiers):
        if ':=' in tokens:
            for token in tokens:
                if token not in identifiers and token not in TOKENS and \
                         self.isValidNumericConstant(token) == False and self.isValidStringConstant(token) == False:
                    return Error('There was an error scanning token: ' + token)

    def parseComposedSeparators(self, tokens: list):
        i = 0
        while i < len(tokens) - 1:
            operator = tokens[i] + tokens[i+1]
            if operator in composed_separators:
                tokens[i] = tokens[i] + tokens[i+1]
                tokens.pop(i + 1)
            i += 1
        return tokens

    def parseOperatos(self, tokens: list):
        i = 1
        while i < len(tokens) - 1:
            if tokens[i] in operators and tokens[i-1] == ':=':
                result = tokens[i] + tokens[i+1]
                tokens[i+1] = result
                tokens.pop(i)
            else:
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

    def isValidNumericConstant(self, constant):
        if constant[0] in operators and len(constant) == 1:
            return False
        if constant[0] in operators:
            position = 1
            if constant[position] == '0':
                return False
            if len(constant) == 2:
                if nonzerodigits.find(constant[position]) > -1:
                    return True
            while position < len(constant):
                if position == 1 and nonzerodigits.find(constant[position]) == -1:
                    return False
                if position > 1 and digits.find(constant[position]) == -1:
                    return False
                position += 1
            return True
        if constant[0] not in operators:
            position = 0
            if len(constant) == 1:
                if digits.find(constant[position]) > -1:
                    return True
            while position < len(constant):
                if position == 0 and nonzerodigits.find(constant[position]) == -1:
                    return False
                if position > 0 and digits.find(constant[position]) == -1:
                    return False
                position += 1
            return True
    def isValidStringConstant(self, constant):
        if constant[0] != '"' or constant[-1] != '"':
            return False
        if constant.find(' ') > -1:
            return False
        return True

    def verifyIdentifiers(self, tokens):
        error = None
        position = 0
        while position < len(tokens) - 1:
            if (tokens[position + 1] == ':' or tokens[position + 1] == ':=') and self.isValidIdentifier(
                    tokens[position]) == False:
                error = Error("Token '" + tokens[position] + "' is not a valid identifier !")
            position += 1
        return error

    def verifyNumberOfParenthesis(self, tokens):
        position = 0
        stack = [ ]
        while position < len(tokens) - 1:
            if tokens[position] == '(' or tokens[position] == '[':
                stack.append(tokens[position])
            if tokens[position] == ')' or tokens[position] == ']':
                if len(stack) == 0:
                    return Error('Invalid number of parenthesis !')
                if tokens[position] == ')' and stack[len(stack) - 1] != '(':
                    return Error('The parenthesis are closed in an incorrect order !')
                if tokens[position] == ']' and stack[len(stack) -1] != '[':
                    return Error('The parenthesis are closed in an incorrect order !')
                stack.pop(len(stack) - 1)
            position += 1
        if len(stack) > 0:
            return Error('Invalid number of parenthesis')
    def verifyVariableDeclaration(self, tokens):
        result = ''
        for token in tokens:
            result += token
        if result.find('var') == 0:
            integerDecl = variableDeclaration.replace('type', 'integer')
            stringDecl = variableDeclaration.replace('type', 'string')
            if re.search(integerDecl, result) == None and re.search(stringDecl, result):
                return Error('Variable declaration is incorrect !')
        else:
            integerDecl = variableDeclarationWithoutVar.replace('type', 'integer')
            stringDecl = variableDeclarationWithoutVar.replace('type', 'string')
            if re.search(integerDecl, result) != None or re.search(stringDecl, result) != None:
                return Error('Illegal variable declaration !')


class Error:
    def __init__(self, message):
        self.__message = message
        self.__line = 0

    @property
    def message(self):
        return self.__message
    @message.setter
    def message(self, value):
        self.__message = value
    @property
    def line(self):
        return self.__line
    @line.setter
    def line(self, value):
        self.__line = value
    def __str__(self):
        return "ERROR ON LINE: " + self.__line.__str__() + " WITH MESSAGE: " + self.__message

class ErrorsList:
    def __init__(self):
        self.__list:[Error] = []

    @property
    def list(self):
        return self.__list
    @list.setter
    def list(self, value):
        self.__list = value

    def addError(self, error):
        self.__list.append(error)

    def len(self):
        return len(self.__list)

    def extend(self, anotherList:[Error]):
        for error in anotherList:
            self.__list.append(error)

    def __str__(self):
        result = '--------------------List of errors---------------\n'
        for error in self.__list:
            result += error.__str__() + "\n"
        return result

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
        self.__list = value

    def __str__(self):
        result = '-----------------------Program Internal Form-------------------------------\n'
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
        self.__errors = ErrorsList()

    def execute(self):
        self.__handler.readTokens()
        file = open(self.__path, 'r')
        identifiers = [ ]
        numberOfLine = 1
        for line in file:
            tokens, errors = self.__handler.parse(line, numberOfLine, identifiers)
            if errors.len() > 0:
                self.__errors.extend(errors.list)
                break
            for token in tokens:
                added = False
                if token in TOKENS and added == False:
                    element = PIFElement(token, TOKENS[token], -1)
                    self.__ProgramInternalForm.addElement(element)
                    added = True
                if self.__symbolTable.isUniqueToken(token) == True and added == False:
                    if self.__handler.isValidIdentifier(token) == True or self.__handler.isValidNumericConstant(token) == True or self.__handler.isValidStringConstant(token):
                        if self.__handler.isValidStringConstant(token) == False and self.__handler.isValidNumericConstant(token) == False:
                            identifiers.append(token)
                        self.__symbolTable.addElement(token)
                        element = PIFElement(token, 0, self.__symbolTable.searchByToken(token))
                        self.__ProgramInternalForm.addElement(element)
                        self.__ProgramInternalForm.list = self.__handler.updateProgramInternalForm(self.__symbolTable.table, self.__ProgramInternalForm.list)
                        added = True
                if self.__symbolTable.isUniqueToken(token) == False and added == False:
                    element = PIFElement(token, 0, self.__symbolTable.searchByToken(token))
                    self.__ProgramInternalForm.addElement(element)
                    added = True
                if added == False:
                    element = Error('There was an error scanning token: ' + token)
                    element.line = numberOfLine
                    self.__errors.addError(element)
                    break
            numberOfLine += 1

        if self.__errors.len() == 0:
            self.__handler.writeInFile('ST.out', self.__symbolTable.__str__())
            self.__handler.writeInFile('PIF.out', self.__ProgramInternalForm.__str__())
            self.__handler.writeInFile('error.out', 'No errors')
        else:
            self.__handler.writeInFile('ST.out', self.__errors.__str__())
            self.__handler.writeInFile('PIF.out', self.__errors.__str__())
            self.__handler.writeInFile('error.out', self.__errors.__str__())
        file.close()

    @property
    def symbolTable(self):
        return self.__symbolTable
    @property
    def ProgramInternalForm(self):
        return self.__ProgramInternalForm




if __name__ == "__main__":
    scanner = Scanner('Problem1.txt')
    scanner.execute()
