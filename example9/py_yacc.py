#! /usr/bin/env python
# coding=utf-8
import ply.yacc as yacc
from py_lex import *
from node import node, num_node


# YACC for parsing Python

def simple_node(t, name):
    t[0] = node(name)
    for i in range(1, len(t)):
        t[0].add(node(t[i]))
    return t[0]


def p_program(t):
    '''program : statements'''
    if len(t) == 2:
        t[0] = node('[PROGRAM]')
        t[0].add(t[1])


def p_statements(t):
    '''statements : statements statement
                  | statement'''
    if len(t) == 3:
        t[0] = node('[STATEMENTS]')
        t[0].add(t[1])
        t[0].add(t[2])
    elif len(t) == 2:
        t[0] = node('[STATEMENTS]')
        t[0].add(t[1])


def p_statement(t):
    ''' statement : assignment
                  | print'''
    if len(t) == 2:
        t[0] = node('[STATEMENT]')
        t[0].add(t[1])


def p_assignment(t):
    '''assignment : VARIABLE '=' expr'''
    if len(t) == 4:
        t[0] = node('[ASSIGNMENT]')
        t[0].add(node(t[1]))
        t[0].add(node(t[2]))
        t[0].add(t[3])


def p_expr(t):
    '''expr : expr '+' term
            | expr '-' term
            | term'''
    if len(t) == 4:
        t[0] = node('[EXPRESSION]')
        t[0].add(t[1])
        t[0].add(node(t[2]))
        t[0].add(t[3])
    elif len(t) == 2:
        t[0] = node('[EXPRESSION]')
        t[0].add(t[1])


def p_term(t):
    '''term : term '*' factor
            | term '/' factor
            | factor'''
    if len(t) == 4:
        t[0] = node('[TERM]')
        t[0].add(t[1])
        t[0].add(node(t[2]))
        t[0].add(t[3])
    elif len(t) == 2:
        t[0] = node('[TERM]')
        t[0].add(t[1])


def p_factor_num(t):
    '''factor : NUMBER'''
    if len(t) == 2:
        t[0] = node('[FACTOR]')
        t[0].add(num_node(t[1]))


def p_factor(t):
    '''factor : VARIABLE
              | '(' expr ')' '''
    if len(t) == 2:
        t[0] = node('[FACTOR]')
        t[0].add(node(t[1]))
    elif len(t) == 4:
        t[0] = node('[FACTOR]')
        t[0].add(t[2])


def p_print(t):
    '''print : PRINT '(' variables ')' '''
    if len(t) == 5:
        t[0] = node('[PRINT]')
        t[0].add(t[3])


def p_variables(t):
    '''variables : VARIABLE
                 | variables ',' VARIABLE'''
    if len(t) == 2:
        t[0] = node('[VARIABLES]')
        t[0].add(node(t[1]))
    elif len(t) == 4:
        t[0] = node('[VARIABLES]')
        t[0].add(t[1])
        t[0].add(node(t[3]))


def p_error(t):
    print("Syntax error at '%s'" % t.value)


yacc.yacc()
