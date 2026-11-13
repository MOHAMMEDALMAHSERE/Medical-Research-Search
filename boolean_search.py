"""Boolean retrieval with AND, OR, NOT and parentheses.
Precedence: NOT > AND > OR; all operators are case-insensitive.
"""
import re
from preprocessing import preprocess

OPERATORS = {"AND", "OR", "NOT"}
PRECEDENCE = {"OR": 1, "AND": 2, "NOT": 3}

def _tokenize(query):
    raw = re.findall(r"\(|\)|[^\s()]+", query)
    if not raw:
        raise ValueError('Empty Boolean query')
    result = []
    for token in raw:
        upper = token.upper()
        if upper in OPERATORS or token in ('(', ')'):
            result.append(upper)
        else:
            terms = preprocess(token)
            if not terms:
                raise ValueError(f'No searchable term in: {token!r}')
            # Multi-token punctuation expansion: implicit AND.
            for term in terms:
                if result and result[-1] not in OPERATORS and result[-1] != '(':
                    result.append('AND')
                result.append(term)
    return result

def boolean_search(query: str, index: dict[str, set[str]], all_ids: set[str]) -> set[str]:
    tokens = _tokenize(query)
    output = []
    ops = []
    for token in tokens:
        if token == '(':
            ops.append(token)
        elif token == ')':
            while ops and ops[-1] != '(':
                output.append(ops.pop())
            if not ops:
                raise ValueError('Unmatched closing parenthesis')
            ops.pop()
        elif token in OPERATORS:
            # NOT is prefix and right associative.
            while (ops and ops[-1] in OPERATORS and
                   (PRECEDENCE[ops[-1]] > PRECEDENCE[token] or
                    (PRECEDENCE[ops[-1]] == PRECEDENCE[token] and token != 'NOT'))):
                output.append(ops.pop())
            ops.append(token)
        else:
            output.append(token)
    while ops:
        operator = ops.pop()
        if operator == '(':
            raise ValueError('Unmatched opening parenthesis')
        output.append(operator)
    stack = []
    for token in output:
        if token == 'NOT':
            if not stack:
                raise ValueError('NOT needs an operand')
            stack.append(all_ids - stack.pop())
        elif token in ('AND', 'OR'):
            if len(stack) < 2:
                raise ValueError(f'{token} needs two operands')
            right, left = stack.pop(), stack.pop()
            stack.append(left & right if token == 'AND' else left | right)
        else:
            stack.append(set(index.get(token, set())))
    if len(stack) != 1:
        raise ValueError('Malformed Boolean query: use explicit AND / OR / NOT')
    return stack[0]
