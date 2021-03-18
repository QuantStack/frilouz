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

def _keep_indent(toks):
    for tok in reversed(toks):
        if tok.exact_type in (token.INDENT, token.DEDENT, token.NEWLINE):
            continue
        return tok.exact_type == token.COLON
    return False

def _build_safe_code(code, error_line):
    '''
    Return a new version of `code` with the lines causing the error at
    `error_line` replaced by `pass`.
    Tries to be smart about which lines to prune
    '''

    # We have two recovery algorithm:
    #
    # 1. if the error happens at an indented line, we just prune all tokens
    #    until next DEDENT token
    #
    # 2. if the error happens on a non-indented line, we prune all tokens until
    #    next NEXLINE token
    all_lines = code.split('\n')
    tmp = io.BytesIO(code.encode())
    currindent = ''
    stop_on_tokens = ()
    prev_toks = []
    for tok in tokenize.tokenize(tmp.readline):
        # Pass in error erasure mode
        if tok.start[0] == error_line and not stop_on_tokens:
            # In case we find a def / class that holds extra indent information
            # we would like to use.
            if tok.exact_type == token.INDENT:
                stop_on_tokens = token.DEDENT, token.ENDMARKER
            else:
                stop_on_tokens = token.NEWLINE, token.ENDMARKER
        # or perform the actual error erasure
        elif tok.exact_type in stop_on_tokens:
            # if we're right after a colon, keep current line indentation
            if _keep_indent(prev_toks):
                indent = _indent(all_lines[error_line - 1])
            # otherwise use computed indentation
            else:
                indent = currindent

            # compute error boundary
            if tok.exact_type == token.DEDENT:
                correct_line = tok.start[0] - 1
            elif tok.exact_type == token.ENDMARKER:
                correct_line = len(all_lines)
            else:
                correct_line = tok.start[0]

            # actual erasure
            for i in range(error_line - 1, correct_line):
                all_lines[i] = indent + 'pass'

            break

        # register indentation level and previous tokens
        # as long as we're not in error mode
        elif not stop_on_tokens:
            if tok.exact_type == token.INDENT:
                currindent += tok.string
            elif tok.exact_type == token.DEDENT:
                currline = all_lines[tok.start[0] - 1]
                currindent = _indent(currline)

            # try to keep token history small
            if tok.exact_type == token.COLON:
                prev_toks.clear()
            prev_toks.append(tok)

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
