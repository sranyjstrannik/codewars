import string
import re
import operator as op


def tokenize(expression):
    if expression == "":
        return []
    regex = re.compile("\s*(=>|[-+*\/\%=\(\)]|[A-Za-z_][A-Za-z0-9_]*|[0-9]*\.?[0-9]+)\s*")
    tokens = regex.findall(expression)
    return [s for s in tokens if not s.isspace()]


class Interpreter:
    def __init__(self):
        self.vars = {}
        self.functions = {}
        self.first_level_operators = ['*', '/', '%']
        self.second_level_operators = ['+', '-']
        self.funct_dict = {
            '*': op.mul,
            '/': op.truediv,
            '%': op.mod,
            '+': op.add,
            '-': op.sub
        }

    def input(self, expression_):
        tokens = tokenize(expression_)
        print(tokens)
        print(self.expression(tokens))
        return self.expression(tokens)

    def expression(self, tokens):
        if not len(tokens): return ''
        if len(tokens) == 1:
            try:
                r = float(tokens[0])
                return r
            except:
                if tokens[0] in self.vars:
                    r = self.vars[tokens[0]]
                    return r
                else:
                    r = tokens[0]
                    if r not in self.functions:
                        raise Exception(" ERROR: Invalid identifier. No variable with name {} was found.".format(r))
                    intr = Interpreter()
                    args, fun = self.functions[r]
                    r = intr.expression(fun)
                    return r


        elif tokens[0] == 'fn':
            # Should throw an error when a function with the name of an existing variable is declared
            if tokens[1] in self.vars: raise Exception()
            identifiers = []
            if tokens[2] != '=>': identifiers = tokens[2:tokens.index('=>')]
            self.functions[tokens[1]] = [identifiers, tokens[tokens.index('=>') + 1:]]

            testIntrpt = Interpreter()
            testIntrpt.vars = {key: value for key, value in zip(identifiers, [1] * len(identifiers))}
            if len(testIntrpt.vars) != len(identifiers):
                raise Exception()
            testIntrpt.expression(tokens[tokens.index('=>') + 1:])
            return ''

        elif tokens[1] == '=':
            id = tokens[0]
            if id in self.functions:
                raise Exception()
            r = self.expression(tokens[2:])
            self.vars[id] = r
            return r

        for t in tokens[::-1]:
            if t in self.functions:
                intr = Interpreter()
                args, fun = self.functions[t]
                start_from = len(tokens) - 1 - tokens[::-1].index(t)
                end_with = start_from + len(args)
                for arg, value in zip(args, tokens[start_from + 1:end_with + 1]): intr.vars[arg] = float(value)
                r = intr.expression(fun)
                return self.expression(tokens[:start_from]
                                       + [r]
                                       + tokens[end_with + 1:])

        while len(tokens) != 1:
            if '(' in tokens:
                start_ind = tokens.index('(')
                finish_ind = -1
                i = start_ind + 1
                bracesCount = 1
                while i < len(tokens) and bracesCount:
                    if tokens[i] == '(': bracesCount += 1
                    if tokens[i] == ')': bracesCount -= 1
                    if not bracesCount:
                        finish_ind = i
                        break
                    else:
                        i += 1

                if finish_ind > -1:
                    tokens_to_replace = tokens[start_ind + 1:finish_ind]
                    tokens = tokens[:start_ind] \
                             + [self.expression(tokens_to_replace)] \
                             + tokens[finish_ind + 1:]
                else:
                    raise Exception("Incorrect expression")
            else:
                flag = False
                for t in tokens:
                    if t in self.first_level_operators:
                        funct = self.funct_dict[t]
                        index_ = tokens.index(t)
                        a = tokens[index_ - 1]
                        b = tokens[index_ + 1]
                        tokens = tokens[:index_ - 1] \
                                 + [funct(self.expression([a]), self.expression([b]))] \
                                 + tokens[index_ + 2:]
                        flag = True
                        break
                if flag: continue
                for t in tokens:
                    if t in self.second_level_operators:
                        if flag: break
                        funct = self.funct_dict[t]
                        index_ = tokens.index(t)
                        a = tokens[index_ - 1]
                        b = tokens[index_ + 1]
                        tokens = tokens[:index_ - 1] \
                                 + [funct(self.expression([a]), self.expression([b]))] \
                                 + tokens[index_ + 2:]
                        flag = True
                if not flag:
                    raise Exception('Incorrect input string')
        return float(tokens[0])