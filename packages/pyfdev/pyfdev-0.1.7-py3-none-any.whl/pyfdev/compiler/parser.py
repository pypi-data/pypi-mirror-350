from typing import List, Tuple

def parse(code: str) -> List[Tuple]:
    tokens = []
    indent_stack = [0]
    lines = code.splitlines()

    for raw in lines:
        indent = len(raw) - len(raw.lstrip(' '))
        line = raw.strip()

        if indent > indent_stack[-1]:
            indent_stack.append(indent)
        while indent < indent_stack[-1]:
            indent_stack.pop()
            tokens.append(('endif', None))

        if line.startswith('if ') and line.endswith(':'):
            cond = line[3:-1].strip()
            if ' when ' in cond:
                cond, guard = cond.split(' when ', 1)
                tokens.append(('if', cond.strip()))
                tokens.append(('guard', guard.strip()))
            else:
                tokens.append(('if', cond))

        elif line.startswith('elif ') and line.endswith(':'):
            cond = line[5:-1].strip()
            tokens.append(('elif', cond))

        elif line.startswith('else:'):
            tokens.append(('else', None))

        elif line.startswith('unless ') and line.endswith(':'):
            cond = line[7:-1].strip()
            tokens.append(('if', f'!({cond})'))

        elif line.startswith('guard ') and ' else:' in line:
            cond = line[6:line.index(' else:')].strip()
            tokens.append(('if', f'!({cond})'))
            tokens.append(('early_return', None))

        elif line.startswith('match ') and line.endswith('{'):
            expr = line[6:-1].strip()
            tokens.append(('match', expr))

        elif line.startswith('case ') and ':' in line:
            pat = line[5:line.index(':')].strip()
            tokens.append(('case', pat))

        elif line.startswith('_') and line.endswith(':'):
            tokens.append(('default', None))

        elif line == '}':
            tokens.append(('endmatch', None))

        elif line.startswith(('num ', 'real ', 'text ', 'yesno ', 'list ')):
            parts = line.split('=', 1)
            dt, var = parts[0].split()
            expr = parts[1].strip()
            tokens.append(('declare', dt, var, expr))

        elif line.startswith('print(') and line.endswith(')'):
            expr = line[6:-1].strip()
            tokens.append(('print', expr))

        elif '=' in line:
            var, expr = line.split('=', 1)
            tokens.append(('assign', var.strip(), expr.strip()))

    while len(indent_stack) > 1:
        indent_stack.pop()
        tokens.append(('endif', None))

    return tokens
