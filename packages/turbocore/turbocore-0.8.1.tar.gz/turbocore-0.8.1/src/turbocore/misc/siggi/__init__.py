import sys

def main():
    filename = sys.argv[1]
    all=[]
    q = "'"
    with open(filename, 'r') as f:
        for line_ in f:
            line = line_.strip()
            if line != "":
                all.append(q + line + q)
    print(", ".join(all), end=None)
