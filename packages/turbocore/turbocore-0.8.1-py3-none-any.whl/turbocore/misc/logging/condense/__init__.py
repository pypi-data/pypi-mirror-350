import turbocore
import sys

def lcon_simple(filename):
    lines = None
    with open(filename, 'r') as f:
        lines = f.read().strip().split("\n")
    lines_actual = []
    s = ""
    for i in range(0, len(lines)):
        part = lines[i]
        if s == "":
            s = part
        else:
            if part.startswith(" ") or part == "}":
                s += part
                #lines_actual.append(s)
                #s = ""
            else:
                lines_actual.append(s)
                s = part
    if s != "":
        lines_actual.append(s)

    for la in lines_actual:
        print(la)

def main():
    turbocore.cli_this(__name__, 'lcon_')
    return
