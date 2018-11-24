

_REPLACE_CHAR = "<HEXCODE>"

def _findNext(line):
    try:
        return line.index("\x1b")
    except ValueError:
        return -1

def _cleanup(line):
    i = 0
    while i < len(line) - 1:
        if line[i] == _REPLACE_CHAR and line[i+1] == _REPLACE_CHAR:
            del line[i]
            continue
        i += 1
    return line

def stripSpecialChars(line):
    if isinstance(line, str):
        line = list(line)
    index = _findNext(line)

    while index+1:
        line[index] = _REPLACE_CHAR
        for i in range(7):
            temp = index + i + 1
            if line[temp] == "m":
                print(index)
                line[temp] = None
                index = _findNext(line)
                break
            elif line[temp] in "[;" or line[temp].isdigit() or line[temp]:
                line[temp] = None

    return _cleanup(list(filter(bool, line)))

# print("".join(stripSpecialChars(test)))
