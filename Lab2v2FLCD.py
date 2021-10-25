class Element:
    def __init__(self, position, token):
        self.__position = position
        self.__token = token

    @property
    def position(self):
        return self.__position
    @position.setter
    def position(self, value):
        self.__position = value

    @property
    def token(self):
        return self.__token
    @token.setter
    def token(self, value):
        self.__token = value


class SortedTable:
    def __init__(self):
        self.__table = []

    @property
    def table(self):
        return self.__table

    def isUniqueToken(self, token):
        exists = True
        for element in self.__table:
            if element.token == token:
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
            if position == len(self.__table):
                return position
            if self.__table[position].token > token:
                return position
            position = position + 1

    def insertElement(self, token):
        position = self.determinePosition(token)
        element = Element(position + 1, token)
        for elem in self.__table:
            if elem.token > token:
                pos = elem.position
                elem.position = (pos + 1)
        self.__table.insert(position, element)

    def searchByToken(self, token):
        exists = False
        for element in self.__table:
            if element.token == token:
                exists = True
                return element.position
        if exists == False:
            return -1

    def __str__(self):
        toStr = ""
        for element in self.__table:
            toStr = toStr + "Position: " + str(element.position) + ", Identifier: " + str(element.token) + "\n"
        return toStr


def main():
    st = SortedTable()
    st.addElement("zzz")
    st.addElement("d")
    st.addElement("abc")
    st.addElement("aaa")
    print(st.toString())
    element = st.searchByToken("d")
    print(element)


if __name__ == "__main__":
    main()


