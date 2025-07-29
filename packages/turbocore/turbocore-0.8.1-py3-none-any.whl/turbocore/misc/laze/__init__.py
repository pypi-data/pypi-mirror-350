import turbocore
import subprocess
import sys
import os
import base64


def mk_sshcbat(filename, name):
    with open(filename, 'w') as f:
        f.write("""
"C:\\lazarus34\\lazbuild.exe" %s\\%s.lpi
""" % (name, name))


def mk_Makefile(filename):
    bdata = """YWxsOgoJbWFrZSBjbGVhbgoJL2Jpbi9iYXNoIC1jICdkYXRlICslcycgPlQxCglt
YWtlIGJ1aWxkCgltYWtlIGV4dHJhY3QKCS9iaW4vYmFzaCAtYyAnZGF0ZSArJXMn
ID5UMgoJbWFrZSB0aW1pbmcKCmNsZWFuOgoJL2Jpbi9iYXNoIC1jICdnZmluZCBi
dWlsZCAtbWF4ZGVwdGggMSAtdHlwZSBkIC1wcmludDAgfCBneGFyZ3MgLXIwbjEg
Y2htb2QgYStyeCcKCS9iaW4vYmFzaCAtYyAnZ2ZpbmQgYnVpbGQgLW1heGRlcHRo
IDIgLXR5cGUgZCAtcHJpbnQwIHwgZ3hhcmdzIC1yMG4xIGNobW9kIGErcngnCgkv
YmluL2Jhc2ggLWMgJ2dmaW5kIGJ1aWxkIC1tYXhkZXB0aCAzIC10eXBlIGQgLXBy
aW50MCB8IGd4YXJncyAtcjBuMSBjaG1vZCBhK3J4JwoJL2Jpbi9iYXNoIC1jICdn
ZmluZCBidWlsZCAtbWF4ZGVwdGggNCAtdHlwZSBkIC1wcmludDAgfCBneGFyZ3Mg
LXIwbjEgY2htb2QgYStyeCcKCS9iaW4vYmFzaCAtYyAnZ2ZpbmQgYnVpbGQgLW1h
eGRlcHRoIDUgLXR5cGUgZCAtcHJpbnQwIHwgZ3hhcmdzIC1yMG4xIGNobW9kIGEr
cngnCglybSAtZnIgVDEgVDIgRFVSCglybSAtZnIgYnVpbGQKCXJtIC1mIHNyYy56
aXAKCXJtIC1mIGJ1aWxkLnppcAoKYnVpbGQ6Cgl6aXAgLXIgc3JjLnppcCBzcmMK
CS9iaW4vYmFzaCAtYyAnc3NoYyBydW4gc3JjLnppcCBseiBEZXZlbG9wZXIgc3Jj
XFx0bXBjJwoKZXh0cmFjdDoKCW1rZGlyIGJ1aWxkCgkvYmluL2Jhc2ggLWMgJ2Nk
IGJ1aWxkICYmIHVuemlwIC4uL2J1aWxkLnppcDsgZXhpdCAwJwoJL2Jpbi9iYXNo
IC1jICdnZmluZCBidWlsZCAtbWF4ZGVwdGggMSAtdHlwZSBkIC1wcmludDAgfCBn
eGFyZ3MgLXIwbjEgY2htb2QgYStyeCcKCS9iaW4vYmFzaCAtYyAnZ2ZpbmQgYnVp
bGQgLW1heGRlcHRoIDIgLXR5cGUgZCAtcHJpbnQwIHwgZ3hhcmdzIC1yMG4xIGNo
bW9kIGErcngnCgkvYmluL2Jhc2ggLWMgJ2dmaW5kIGJ1aWxkIC1tYXhkZXB0aCAz
IC10eXBlIGQgLXByaW50MCB8IGd4YXJncyAtcjBuMSBjaG1vZCBhK3J4JwoJL2Jp
bi9iYXNoIC1jICdnZmluZCBidWlsZCAtbWF4ZGVwdGggNCAtdHlwZSBkIC1wcmlu
dDAgfCBneGFyZ3MgLXIwbjEgY2htb2QgYStyeCcKCS9iaW4vYmFzaCAtYyAnZ2Zp
bmQgYnVpbGQgLW1heGRlcHRoIDUgLXR5cGUgZCAtcHJpbnQwIHwgZ3hhcmdzIC1y
MG4xIGNobW9kIGErcngnCgkjdW56aXAgLWogYnVpbGQuemlwICdzcmNcXFRoZUFw
cFxccHJvamVjdDEuZXhlJwoKdGltaW5nOgoJL2Jpbi9iYXNoIC1jICdUMT1gY2F0
IFQxYDtUMj1gY2F0IFQyYDsoKERVUj1UMi1UMSkpO2VjaG8gJCREVVInID5EVVIK
"""
    with open(filename, 'wb') as f:
        f.write(base64.b64decode(bdata))

def mk_minizip(filename):
    bdata = """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
AMIKAAAAAA==
"""
    with open(filename, 'wb') as f:
        f.write(base64.b64decode(bdata))


def text_replace(filename, text, repl):
    lines = None
    try:
        with open(filename, 'r') as f:
            lines = f.read().split("\n")
        nlines = [line.replace(text, repl) for line in lines]
    except Exception as e:
        print("fehler %s %s" % (filename, str(e)))
        sys.exit(1)
    with open(filename, 'w') as f:
        for line in nlines:
            f.write(line + "\n")


def rename_project(from_name, to_name, srcdir):
    print("renaming project from %s to %s in dir %s" % (from_name, to_name, srcdir))

    from_filename = from_name + ".lpi"
    to_filename = to_name + ".lpi"
    subprocess.call("mv %s/%s %s/%s" % (srcdir, from_filename, srcdir, to_filename), shell=True)
    text_replace(srcdir+"/"+to_filename, from_name, to_name)

    from_filename = from_name + ".lpr"
    to_filename = to_name + ".lpr"
    subprocess.call("mv %s/%s %s/%s" % (srcdir, from_filename, srcdir, to_filename), shell=True)
    text_replace(srcdir+"/"+to_filename, from_name, to_name)
    
    from_filename = from_name + ".lps"
    to_filename = to_name + ".lps"
    subprocess.call("mv %s/%s %s/%s" % (srcdir, from_filename, srcdir, to_filename), shell=True)
    text_replace(srcdir+"/"+to_filename, from_name, to_name)
    
    from_filename = from_name + ".res"
    to_filename = to_name + ".res"
    subprocess.call("mv %s/%s %s/%s" % (srcdir, from_filename, srcdir, to_filename), shell=True)
    #not needed text_replace(srcdir+"/"+to_filename, from_name, to_name)




def laze_create(name):
    subprocess.call("""/bin/bash -c 'rm -f build.exe out.txt err.txt dur.txt'""", shell=True)
    os.makedirs("src/%s/src" % name)
    mk_minizip("src/%s/src/mini.zip" % name)
    subprocess.call("""/bin/bash -c 'cd "src/%s/src" && unzip mini.zip; rm -f mini.zip; mv mini %s;'""" % (name, name), shell=True)
    mk_Makefile("src/%s/Makefile" % name)
    mk_sshcbat("src/%s/src/sshc.bat" % name, name)
    rename_project("project1", name, "src/%s/src/%s" % (name, name))
    subprocess.call("""/bin/bash -c 'ln -s src/%s/build/src/%s/%s.exe build.exe'""" % (name, name, name), shell=True)
    subprocess.call("""/bin/bash -c 'ln -s src/%s/build/src/out.txt out.txt'""" % (name), shell=True)
    subprocess.call("""/bin/bash -c 'ln -s src/%s/build/src/err.txt err.txt'""" % (name), shell=True)
    subprocess.call("""/bin/bash -c 'ln -s src/%s/DUR dur.txt'""" % (name), shell=True)
    with open("build.sh", 'w') as f:
        f.write("""#!/bin/bash

( cd src/%s && make )
""" % name )
    subprocess.call("""/bin/bash -c 'chmod a+x build.sh'""", shell=True)




def main():
    turbocore.cli_this(__name__, 'laze_')
