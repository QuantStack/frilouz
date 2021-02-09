import tokenize, token, re, io

def _indent(line):
    indent = ''
    for c in line:
        if c == ' ':
            indent += c
        elif c == '\t':
            indent += c
        else:
            break
    return indent

def _isdefcls(tok):
    if tok.exact_type != token.NAME:
        return False
    return tok.string == 'def' or tok.string == 'class'

def _build_safe_code(code, error_line):
    all_lines = code.split('\n')
    tmp = io.BytesIO(code.encode())
    lastdeforcls = 0
    lastdeforclsindent = ''
    error_recovery = False
    for tok in tokenize.tokenize(tmp.readline):
        if tok.exact_type == token.ENDMARKER:
            continue
        if error_recovery:
            if _isdefcls(tok):
                error_recovery = False
                lastdeforcls = tok.start[0] - 1
                lastdeforclsindent = _indent(all_lines[lastdeforcls])
                break
            elif tok.exact_type != token.DEDENT:
                all_lines[tok.start[0] - 1] = lastdeforclsindent + 'pass'
        elif _isdefcls(tok):
            lastdeforcls = tok.start[0] - 1
            lastdeforclsindent = _indent(all_lines[lastdeforcls])
        elif tok.start[0] == error_line:
            error_recovery = True
            for i in range(lastdeforcls, error_line):
                all_lines[i] = lastdeforclsindent + 'pass'
    return '\n'.join(all_lines)

def parse(parser, code, *args, **kwargs):
    error_lineno = -1
    error_offset = -1
    errors = []
    while True:
        try:
            return parser(code, *args, **kwargs), errors
        except SyntaxError as se:
            errors.append(se)
            # make sure we are making progress in the error detection
            if se.lineno == error_lineno and se.offset == error_offset:
                code = ''
            else:
                code = _build_safe_code(code, se.lineno)
                error_lineno = se.lineno
                error_offset = se.offset

if __name__ == '__main__':
    import sys
    import ast
    if len(sys.argv) != 2:
        print("Usage: frilouz input.py", file=sys.stderr)
        sys.exit(1)
    with open(sys.argv[1]) as fd:
        code = fd.read()
        tree, errors = parse(ast.parse, code, filename=sys.argv[1])
        if status is TOTAL:
            print("valid Python code")
        else:
            print("invalid Python code, met the following errors:")
            for error in errors:
                print('*', error)
