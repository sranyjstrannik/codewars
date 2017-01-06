import string
import re
import operator as op

def tokenize(expression):
    if expression == "":
        return []

    # TODO: разобрать это выражение
    regex = re.compile("\s*(=>|[-+*\/\%=\(\)]|[A-Za-z_][A-Za-z0-9_]*|[0-9]*\.?[0-9]+)\s*")
    tokens = regex.findall(expression)
    return [s for s in tokens if not s.isspace()]

class Interpreter:
    def __init__(self):
        self.vars = {}
        self.functions = {}

    def input(self, expression_):
        tokens = tokenize(expression_)
        print(self.expression(tokens))

    def expression(self, tokens):
        # expression ::= factor | expression operator expression
        # factor ::= number | identifier | assignment | '(' expression ')'
        # нужно проверить, является ли первый элемент массива token
        # однозначно указывающим на factor
        # если начинается с (, то парсим остаток до соответствующей закрывающей
        # скобки как expression
        # если ничего этого не происходит,
        # смотрим, похоже ли на identifier или на number
        if len(tokens) == 1:
            try:
                r = float(tokens[0])
                return r
            except: # identifier
                if tokens[0] in self.vars:
                    r = self.vars[tokens[0]]
                    return r
                else:
                    r = tokens[0]
                    raise Exception(
                        " ERROR: Invalid identifier. No variable with name {} was found.".format(r))

        # смотрим, похоже ли на assignment
        # assignment ::= identifier '=' expression
        elif tokens[1] == '=':
            id = tokens[0]
            r = self.expression(tokens[2:])
            self.vars[id] = r
            return r
        # проверяем, похоже ли на выражение в скобках
        #elif tokens[0] == '(' and tokens[-1] == ')':
        #    return self.expression(tokens[1:-2])

        # если программа дошла до этого места, значит, осталось
        #  выражение вида expression operator expression
        while len(tokens) != 1:
            # убираем скобки
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
                    tokens_to_replace = tokens[start_ind+1:finish_ind]
                    tokens = tokens[:start_ind]\
                             +[self.expression(tokens_to_replace)]\
                             +tokens[finish_ind+1:]
                else:
                    raise Exception("Incorrect expression")

            # вычисляем в порядке приоритета операторов
            else:
                first_level_operators = ['*', '/', '%']
                second_level_operators = ['+', '-']
                funct_dict ={
                    '*': op.mul,
                    '/': op.truediv,
                    '%': op.mod,
                    '+': op.add,
                    '-': op.sub
                }

                flag = False
                for flo in first_level_operators:
                    if flo in tokens:
                        funct = funct_dict[flo]
                        index_ = tokens.index(flo)
                        a = tokens[index_-1]
                        b = tokens[index_+1]
                        # здесь тоже нужно обрабатывать ошибки в идеале
                        # TODO
                        tokens = tokens[:index_-1]\
                                 +[funct(self.expression([a]),self.expression([b]))]\
                                 +tokens[index_+2:]
                        flag = True
                        break
                if flag: continue
                for slo in second_level_operators:
                    if flag: break
                    if slo in tokens:
                        funct = funct_dict[slo]
                        index_ = tokens.index(slo)
                        a = tokens[index_ - 1]
                        b = tokens[index_ + 1]
                        # здесь тоже нужно обрабатывать ошибки в идеале
                        # TODO
                        tokens = tokens[:index_ - 1] + [funct(self.expression([a]), self.expression([b]))] + tokens[index_ + 2:]
                        flag = True
                if not flag:
                        raise Exception('Incorrect input string')
        return float(tokens[0])

i = Interpreter()
i.input('dfs1 = 100')
i.input('4 / 2 * 3')
i.input('(7 + 3) / (2 * 2 + 1)')
