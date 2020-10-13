class BracketsError(Exception):
    pass


def parse_strings(line):
    strings = []
    stack = []
    p = ''
    for i, char in enumerate(line):
        if char in '\'\"':
            if not stack:
                if char == line[i + 1] == line[i + 2]:
                    stack.append((char * 3, i))
                    p = char * 3
                else:
                    stack.append((char, i))
                    p = char
            elif char == p[0]:
                if line[i - 1] == '\\':
                    continue
                if len(p) == 1:
                    s, start = stack.pop()
                    yield (start, i)
                elif len(p) == 3 and line[i - 2] == line [i - 1] == char and line[i - 3] != '\\':
                    s, start = stack.pop()
                    yield (start, i)


def parse_brackets(line, ignored_fragments):
    stack = []
    n = len(line)
    ignored_fragments = ignored_fragments + [(n, n)]
    i = 0
    for start, end in ignored_fragments:
        while i < start:
            char = line[i]
            if char in '([{':
                stack.append((char, i))
            elif char in ')]}':
                if not stack:
                    raise BracketsError(
                        "closinging bracket {char} at pos {i} without opening bracket"
                        .format(char=char, i=i)
                    )
                last = stack.pop()
                if last[0] + char not in '()[]{}':
                    raise BracketsError(
                        "closinging bracket {char} at pos {i} doesn't correspond to open bracket"
                        .format(char=char, i=i)
                    )
                yield last[1], i
            i += 1
        i = end + 1

    while stack:
        last = stack.pop()
        yield last[1], None


def parse_commas(line, start, end, ignored_fragments):
    ignored_fragments = ignored_fragments + [(end, end)]
    i = start
    for fr_start, fr_end in ignored_fragments:
        while i < fr_start:
            char = line[i]
            if char == ',':
                yield i
            i += 1
        i = fr_end + 1


def main_brackets(line, ignored_fragments):
    brackets = list(parse_brackets(line, ignored_fragments))
    main = max(
        filter(lambda x: x[1], brackets),
        key=lambda x: x[1] - x[0]
    )
    inner = sorted(x for x in brackets if main[0] < x[1] < main[1])
    i = 1
    while i < len(inner):
        if inner[i - 1][1] > inner[i][0]:
            inner.pop(i)
        else:
            i += 1
    return main, inner


def indentetion(line):
    i = 0
    while line[i] == ' ':
        i += 1
    return i


def trim_line(line):
    idn = indentetion(line)
    ignored_fragments = sorted(list(parse_strings(line)))
    (start, end), inner = main_brackets(line, ignored_fragments)
    ignored_fragments = sorted(ignored_fragments + inner)
    p = start + 1
    result = line[:p] + '\n'
    for c in list(parse_commas(line, start, end, ignored_fragments)) + [end - 1]:
        s = line[p:c + 1]
        while s.startswith(' '):
            s = s[1:]
        fragment = ' ' * (idn + 4) + s + '\n'
        if len(fragment) > 78:
            fragment = trim_line(fragment)
        result += fragment
        p = c + 1
    result += ' ' * idn + line[end:]
    return result
