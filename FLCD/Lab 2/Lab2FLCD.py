class Node:
    def __init__(self, position, token, father, sibling):
        self.__position = position
        self.__token = token
        self.__father = father
        self.__sibling = sibling

    def getPosition():
        return self.__position
    def setPosition(position):
        self.__position = position

    def getToken():
        return self.__token
    def setToken(token):
        self.__token = token

    def getFather():
        return self.__father
    def setFather(father):
        self.__father = father

    def getSibling():
        return self.__sibling
    def setSibling(sibling):
        self.__sibling = sibling


class BinaryTree:
    def __init__(self):
        self.__tree = [ ]

    def getChildrenWithSpecifiedFather(father):
        result = -1
        for node in self.__tree:
            if node.getFather() == father.getPosition():
                result = node.getPosition()
        return result

    def computeAttributes(token):
        currentNode = self.__tree[0]
        position = -1
        father = -1
        sibling = -1
        while True:
            if 

    def addNode(token):
        if len(self.__tree) == 0:
            node = Node(1, token, -1, -1)
            self.__tree.append(node)
        else:

