#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This grammar extracts from an input string or tokenlist the elements that conforms the input grammar definition"""

from pydsl.Memory.Storage.Directory.Grammar import GrammarDirStorage

def function(inputdic, inputgt, outputgt):
    grammarname =  inputdic['grammar']
    gl = GrammarDirStorage()
    grammar = gl.loadGrammar(grammarname)
    thestring = inputdic['string'].string
    result = ""
    tmpstring = ""
    while len(thestring) > 0:
        tmpstring += thestring[0]
        del thestring[0]
        for tmpindex in range(len(tmpstring)):
            tmptmpstring = tmpstring[tmpindex:]
            if grammar.check(tmptmpstring):
                while grammar.check(tmptmpstring + thestring[0]):
                    tmptmpstring += thestring[0]
                    del thestring[0]
                result += tmptmpstring
                result += " " #separator
    return {"output":result}


inputdic = {
          "grammar":"cstring"
        , "cstring":"cstring"}
outputdic = {"output":"list"}
iclass = "PythonTransformer"
