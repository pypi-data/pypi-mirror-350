import datetime
import turbocore
import sys
import re

from rich.pretty import pprint as PP



def private_extract_ip4(src):
    digit_src = ""
    for i in range(0, len(src)):
        c = src[i]
        m = re.fullmatch(r'[0-9]+', c)
        if m is None:
            if c == ".":
                digit_src+=""+c
            else:
                digit_src+=" "
        else:
            digit_src+=""+c
    digit_src = digit_src.strip()
    
    for w in digit_src.split(" "):
        addr = re.fullmatch(r'[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}', w)
        if addr is not None:
            cols = [int(x) for x in w.split(".")]
            if len(cols) != 4:
                continue
            if cols[0] < 0 or cols[0] > 255:
                continue
            if cols[1] < 0 or cols[1] > 255:
                continue
            if cols[2] < 0 or cols[2] > 255:
                continue
            if cols[3] < 0 or cols[3] > 255:
                continue
            return "%d.%d.%d.%d" % (cols[0],cols[1],cols[2],cols[3])

    return ""

def a2_errorlog(filename, funnel, transformation, selection):
    """Read typical apache errorlog.
    """

    selections = None
    if selection != "":
        selections = [ int(x) for x in  selection.split(",") ]

    transformations = {}
    if transformation != "":
        for colsrc in transformation.split(","):
            cols = colsrc.split("=")
            transformations[cols[0]] = private_extract_ip4

    funnels = []
    if funnel != "":
        for f in funnel.split(","):
            cols = f.split("=")
            funnels.append([
                int(cols[0]),
                cols[1]
                ])

    with open(filename, 'r') as f:
        for line_ in f:
            if line_.strip() == "":
                continue
            line = line_.strip().replace("] [", "\t", 4).replace("[", "", 1).replace("] ", "\t", 1)
            cols = line.split("\t")
            in_funnel = True
            try:
                for fun in funnels:
                    if not fun[1].upper() in cols[fun[0]].upper():
                        in_funnel=False
                        break
            except:
                in_funnel = False

            if in_funnel:
                time_form = "%a %b %d %H:%M:%S.%f %Y"
                t = datetime.datetime.strptime(cols[0], time_form)
                t = t.replace(tzinfo=datetime.UTC)
                cols[0] = t.isoformat()
                
                colso_transformed = []
                for trans_i in range(0, len(cols)):
                    if str(trans_i) in transformations.keys():
                        colso_transformed.append(transformations[str(trans_i)](cols[trans_i]))
                    else:
                        colso_transformed.append(cols[trans_i])

                colso = colso_transformed
                if selections is not None:
                    # colso = [str(xx_) for xx_ in selections]
                    colso = [colso_transformed[xx_] for xx_ in selections]

                print("\t".join(colso))


def main():
    turbocore.cli_this(__name__, 'a2_')
    return
