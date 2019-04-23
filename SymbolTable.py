#!/usr/bin/python


class Symbol:
    pass


class VariableSymbol(Symbol):
    def __init__(self, name, type):
        self.name = name
        self.type = type
    #


class FunctionSymbol(Symbol):
    def __init__(self, name, type, table):
        self.name = name
        self.type = type
        self.params = []
        self.table = table

    def extractParams(self):
        self.params = [x.type for x in self.table.symbols.values()]


class SymbolTable(object):

    def __init__(self, parent, name): # parent scope and symbol table name
        self.symbols = {}
        self.name = name
        self.parent = parent
    #

    def put(self, name, symbol): # put variable symbol or fundef under <name> entry
        self.symbols[name] = symbol
    #

    def get(self, name): # get variable symbol or fundef from <name> entry
        try:
            ret = self.symbols[name]
            return ret
        except:
            return None
    #

    def getGlobal(self, name):
        if self.get(name) is None:
            if self.parent is not None:
                return self.parent.getGlobal(name)
            else:
                return None
        else:
            return self.get(name)

    def getParentScope(self):
        return self.parent
    #

    def pushScope(self, name):
        self.name = name
    #

    def popScope(self):
        return self.name
    #
