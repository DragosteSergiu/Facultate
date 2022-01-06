class Element:
    def __init__(self, position, token):
        self.__position = position
        self.__token = token

    def getPosition(self):
        return self.__position

    def setPosition(self, position):
        self.__position = position

    def getToken(self):
        return self.__token

    def setToken(self, token):
        self.__token = token


class SortedTable:
    def __init__(self):
        self.__table = []
    
    def isUniqueToken(self, token):
        exists = True
        for element in self.__table: 
            if element.getToken() == token:
                exists = False
        return exists

    def addElement(self, token):
        if len(self.__table) == 0:
            element = Element(1, token)
            self.__table.append(element)
        else:
            if self.isUniqueToken(token) == True:
                self.insertElement(token)

    def determinePosition(self, token):
        position = 0
        while True:
            if self.__table[position].getToken() > token:
                return position
            position = position + 1

    def insertElement(self, token):
        position = self.determinePosition(token)
        element = Element(position + 1, token)
        for elem in self.__table:
            if elem.getToken() > token:
                pos = elem.getPosition()
                elem.setPosition(pos + 1)
        self.__table.insert(position, element)

    def searchByToken(self, token):
        exists = False
        for element in self.__table:
            if element.getToken() == token:
                exists = True
                return element
        if exists == False:
            return None

    def toString(self):
        toStr = ""
        for element in self.__table:
            toStr = toStr + "Position: " + str(element.getPosition()) + ", Identifier; " + element.getToken() + "\n"
        return toStr


def main():
    st = SortedTable()
    st.addElement("zzz")
    st.addElement("d")
    st.addElement("abc")
    st.addElement("aaa")
    print(st.toString())
    element = st.searchByToken("d")
    print('SEARCH RESULT: ' + str(element.getPosition()) + ", " + element.getToken())


if __name__ == "__main__":
    main()


