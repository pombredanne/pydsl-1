#!/usr/bin/python
# -*- coding: utf-8 -*-
#This file is part of pydsl.
#
#pydsl is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#pydsl is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with pydsl.  If not, see <http://www.gnu.org/licenses/>.

"""loader class"""
from pydsl.Alphabet.Definition import Encoding

__author__ = "Nestor Arocha"
__copyright__ = "Copyright 2008-2013, Nestor Arocha"
__email__ = "nesaro@gmail.com"

def load_checker(grammar):
    from pydsl.Grammar.BNF import BNFGrammar
    from pydsl.Grammar.Definition import PLYGrammar, RegularExpressionDefinition, MongoGrammar
    from pydsl.Alphabet.Definition import AlphabetDictDefinition
    if isinstance(grammar, str):
        grammar = load(grammar)
    if isinstance(grammar, BNFGrammar):
        from pydsl.Checker import BNFChecker
        return BNFChecker(grammar)
    elif isinstance(grammar, RegularExpressionDefinition):
        from pydsl.Checker import RegularExpressionChecker
        return RegularExpressionChecker(grammar)
    elif isinstance(grammar, dict) and "matchFun" in grammar:
        from pydsl.Checker import PythonChecker
        return PythonChecker(grammar)
    elif isinstance(grammar, MongoGrammar):
        from pydsl.Checker import MongoChecker
        return MongoChecker(grammar["spec"])
    elif isinstance(grammar, PLYGrammar):
        from pydsl.Checker import PLYChecker
        return PLYChecker(grammar)
    elif isinstance(grammar, AlphabetDictDefinition):
        from pydsl.Checker import AlphabetDictChecker
        return AlphabetDictChecker(grammar)
    elif isinstance(grammar, Encoding):
        from pydsl.Checker import EncodingChecker
        return EncodingChecker(grammar)
    else:
        raise ValueError(grammar)

def load_grammar_tool(grammar):
    from pydsl.Grammar.BNF import BNFGrammar
    from pydsl.Grammar.Definition import RegularExpressionDefinition
    from pydsl.Grammar.Tool.Python import PythonGrammarTools
    if isinstance(grammar, str):
        grammar = load(grammar)
    if isinstance(grammar, BNFGrammar):
        from pydsl.Grammar.Tool.Symbol import SymbolGrammarTools
        return SymbolGrammarTools(grammar)
    elif isinstance(grammar, RegularExpressionDefinition):
        from pydsl.Grammar.Tool.Regular import RegularExpressionGrammarTools
        return RegularExpressionGrammarTools(grammar)
    elif isinstance(grammar, dict) and "matchFun" in grammar:
        from pydsl.Grammar.Tool.Python import PythonGrammarTools
        return PythonGrammarTools(grammar)
    else:
        raise ValueError(grammar)

def load_lexer(alphabet):
    from pydsl.Alphabet.Definition import AlphabetDictDefinition
    from pydsl.Grammar.BNF import BNFGrammar
    if isinstance(alphabet, str):
        alphabet = load(alphabet)
    if isinstance(alphabet, AlphabetDictDefinition):
        from pydsl.Alphabet.Lexer import AlphabetDictLexer
        return AlphabetDictLexer(alphabet)
    elif isinstance(alphabet, BNFGrammar):
        from pydsl.Alphabet.Lexer import BNFLexer
        return BNFLexer(alphabet)
    else:
        raise ValueError(alphabet)

def load_parser(grammar, parser = "auto"):
    if isinstance(grammar, str):
        grammar = load(grammar)
    from pydsl.Grammar.BNF import BNFGrammar
    if isinstance(grammar, BNFGrammar):
        if parser == "descent":
            from pydsl.Grammar.Parser.RecursiveDescent import RecursiveDescentParser
            return RecursiveDescentParser(grammar)
        elif parser in ("auto" , "default" , "weighted"):
            #TODO Guess best parser
            from pydsl.Grammar.Parser.Weighted import WeightedParser
            return WeightedParser(grammar)
        else:
            raise Exception("Wrong parser name: " + parser)
    else:
        raise ValueError(grammar)



def load(identifier, memorylist = None):
    if not memorylist:
        from pydsl.Config import GLOBALCONFIG
        memorylist = GLOBALCONFIG.memorylist
    for memory in memorylist:
        if identifier in memory:
            return memory.load(identifier)
    raise KeyError(identifier)
