#! /usr/bin/env python
# coding=utf-8
from __future__ import division

v_table = {}  # variable table


def update_v_table(name, value):
    v_table[name] = value


def trans(node):
    for c in node.getchildren():
        trans(c)

    # Translation

    # assignment
    if node.getdata() == '[ASSIGNMENT]':
        '''assignment : VARIABLE '=' expr'''
        value = node.getchild(2).getvalue()
        node.getchild(0).setvalue(value)
        # update v_table
        update_v_table(node.getchild(0).getdata(), value)

    # expr
    elif node.getdata() == '[EXPRESSION]':
        '''expr : expr '+' term
                | expr '-' term
                | term'''
        if len(node.getchildren()) == 3:
            arg0 = node.getchild(0).getvalue()
            arg1 = node.getchild(2).getvalue()
            op = node.getchild(1).getdata()

            if op == '+':
                value = arg0 + arg1
            elif op == '-':
                value = arg0 - arg1

            node.setvalue(value)
        elif len(node.getchildren()) == 1:
            value = node.getchild(0).getvalue()

            node.setvalue(value)

    # term
    elif node.getdata() == '[TERM]':
        '''term : term '*' factor
                | term '/' factor
                | factor'''
        if len(node.getchildren()) == 3:
            arg0 = node.getchild(0).getvalue()
            arg1 = node.getchild(2).getvalue()
            op = node.getchild(1).getdata()

            if op == '*':
                value = arg0 * arg1
            elif op == '/':
                value = arg0 / arg1

            node.setvalue(value)
        elif len(node.getchildren()) == 1:
            value = node.getchild(0).getvalue()

            node.setvalue(value)

    # factor
    elif node.getdata() == '[FACTOR]':
        '''factor : NUMBER
                  | VARIABLE
                  | '(' expr ')' '''
        if len(node.getchildren()) == 1:
            value = node.getchild(0).getvalue()
            if value is None:       # 判断是NUMBER还是VARIABLE，如果是None，即为VARIABLE
                value = v_table[node.getchild(0).getdata()]
            node.setvalue(value)

    # Print
    elif node.getdata() == '[PRINT]':
        '''print : PRINT '(' variables ')' '''
        arg0 = node.getchild(0).getvalue()
        print arg0

    # variables
    elif node.getdata() == '[VARIABLES]':
        if len(node.getchildren()) == 1:
            value = v_table[node.getchild(0).getdata()]

            node.setvalue(value)
        elif len(node.getchildren()) == 2:
            arg0 = node.getchild(0).getvalue()
            arg1 = v_table[node.getchild(1).getdata()]

            value = str(arg0) + ' ' + str(arg1)

            node.setvalue(value)
