import subprocess

def main():
    runr([
        "x <- c(1,2,3)",
        """write.table(x, file = "test.tsv", sep = "\\t", row.names = FALSE, col.names = FALSE)"""
    ])

def runr(lines):
    tmpdir = subprocess.check_output("mktemp -d /tmp/runr-XXXXXXXXXX", shell=True, universal_newlines=True).strip().split("\n")[0]
    subprocess.check_output("/bin/bash -c 'mkdir -p %s/workspace'" % tmpdir, shell=True, universal_newlines=True)
    with open('%s/main.R' % tmpdir, 'w') as f:
        for line in lines:
            f.write(line)
            f.write("\n")
    subprocess.check_output("/bin/bash -c 'cd %s/workspace && R --no-save < ../main.R 1>../o 2>../e'" % tmpdir, shell=True, universal_newlines=True)
    print(tmpdir)
    subprocess.check_output("""/bin/bash -c 'rm -f outr.tar.gz; tar cvzfC outr.tar.gz %s .'""" % tmpdir, shell=True, universal_newlines=True)
    subprocess.check_output("""/bin/bash -c 'rm -fr "%s"'""" % tmpdir, shell=True, universal_newlines=True)
