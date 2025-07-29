import re
from typing import List, Tuple

def transpile(tokens: List[Tuple]) -> str:
    includes = ['#include <stdio.h>', '#include <string.h>', '#include <stdbool.h>']
    lines = []
    var_types = {}
    depth = 1
    indent = '    '

    type_map = {
        'num': ('int', '%d'),
        'real': ('double', '%f'),
        'text': ('char*', '%s'),
        'yesno': ('bool', '%d')
    }

    def emit(line):
        lines.append(indent * depth + line)

    for tok in tokens:
        kind = tok[0]

        if kind == 'declare':
            dt, var, expr = tok[1], tok[2], tok[3]
            ctype, fmt = type_map.get(dt, (None, None))
            if dt == 'text' and not expr.startswith(('"', "'")):
                expr = f'"{expr}"'
            if dt == 'yesno':
                expr = 'true' if expr.lower() == 'true' else 'false'
            emit(f'{ctype} {var} = {expr};')
            var_types[var] = (dt, fmt)

        elif kind == 'assign':
            var, expr = tok[1], tok[2]
            if var not in var_types:
                emit(f'int {var} = {expr};')
                var_types[var] = ('num', '%d')
            else:
                emit(f'{var} = {expr};')

        elif kind == 'print':
            expr = tok[1]
            if expr.startswith(('"', "'")):
                emit(f'printf("%s\\n", {expr});')
            elif expr in var_types:
                vt, fmt = var_types[expr]
                emit(f'printf("{fmt}\\n", {expr});')
            else:
                names = re.findall(r"[A-Za-z_][A-Za-z0-9_]*", expr)
                uses_real = any(var_types.get(n, (None,))[0] == 'real' for n in names) or '.' in expr
                fmt = '%f' if uses_real else '%d'
                expr2 = expr.replace(' in ', ' >= ').replace('..', ' && ').replace(' &&  && ', ' && ')
                emit(f'printf("{fmt}\\n", {expr2});')

        elif kind == 'if':
            cond = tok[1]
            emit(f'if ({cond}) ' + '{')
            depth += 1

        elif kind == 'guard':
            cond = tok[1]
            emit(f'if (!({cond})) ' + '{')
            depth += 1

        elif kind == 'elif':
            depth -= 1
            cond = tok[1]
            emit(f'}} else if ({cond}) ' + '{')
            depth += 1

        elif kind == 'else':
            depth -= 1
            emit('} else {')
            depth += 1

        elif kind == 'endif':
            depth -= 1
            emit('}')

        elif kind == 'early_return':
            emit('return;')
            depth -= 1
            emit('}')

        elif kind == 'match':
            expr = tok[1]
            emit(f'switch ({expr}) ' + '{')
            depth += 1

        elif kind == 'case':
            pat = tok[1]
            emit(f'case {pat}:')

        elif kind == 'default':
            emit('default:')

        elif kind == 'endmatch':
            emit('break;')
            depth -= 1
            emit('}')

    preamble = '\n'.join(includes)
    main_function = 'int main() {\n' + '\n'.join(lines) + f'\n{indent}return 0;\n}}'
    full_code = preamble + '\n\nvoid early_return() {{}}\n' + main_function
    return full_code
