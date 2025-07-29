import sys
import requests

def main():
    # filename = sys.argv[1]
    # print("reading %s" % filename)


    # data = open(filename, "r").read().strip()

    data = requests.get("https://docs.docker.com/desktop/release-notes/").text
    data = data.replace("<h2", "\n<h2")
    data = data.replace("</", "\n</")
    lines = data.split("\n")

    count_h2 = 0

    first_h2 = []

    with open("dl.sh", "w") as o:
        for line_ in lines:
            line = line_.strip()
            if line.startswith("<h2"):
                count_h2+=1
            
            if count_h2 == 1:
                first_h2.append(line)
                #o.write(line + "\n")
        
        tmp = " ".join(first_h2).replace("  ", "").replace(" </a", "</a").strip().replace("<a ", "\n<a ")
        version_lines = [x for x in tmp.split("\n") if "<a " in x ]
        version_line = version_lines[0]

        link_lines = [x for x in version_lines if ".dmg" in x ]
        # o.write("\n".join(version_lines))

        for link_line in link_lines:
            href = link_line.split("href=")[1].split(">")[0].replace("'", "").replace('"', '')
            if "arm64" in href:
                o.write("#!/bin/bash\n\n\ncurl -L -o Docker.img '%s'" % href)
                o.write("\n")
        # o.write(version_line)
