import subprocess
import sys
import io
import turbocore


def sshc_run(srczip, sshhost, remoteuser, target_buildroot):
    print("compiling remotely via SSH...")

    prep_cmd = """ssh %s 'del /f /q %s\\src.zip'""" % (sshhost, target_buildroot)
    print("="*64)
    print("(XX) %s" % prep_cmd)
    print("="*64)
    subprocess.call(prep_cmd, shell=True, universal_newlines=True)

    
    prep_cmd = """scp %s %s:%s""" % (srczip, sshhost, target_buildroot.replace("\\", "/"))
    print("="*64)
    print("(XX) %s" % prep_cmd)
    print("="*64)
    subprocess.call(prep_cmd, shell=True, universal_newlines=True)

    prep_cmd = """ssh %s 'rmdir /s /q %s\\src'""" % (sshhost, target_buildroot)
    print("="*64)
    print("(XX) %s" % prep_cmd)
    print("="*64)
    subprocess.call(prep_cmd, shell=True, universal_newlines=True)

    prep_cmd = """ssh %s 'cd %s & powershell -command "Expand-Archive -Path src.zip -DestinationPath ."'""" % (sshhost, target_buildroot)
    print("="*64)
    print("(XX) %s" % prep_cmd)
    print("="*64)
    subprocess.call(prep_cmd, shell=True, universal_newlines=True)

    prep_cmd = """ssh %s 'del /f /q %s\\src.zip'""" % (sshhost, target_buildroot)
    print("="*64)
    print("(XX) %s" % prep_cmd)
    print("="*64)
    subprocess.call(prep_cmd, shell=True, universal_newlines=True)

    prep_cmd = """ssh %s 'del /f /q %s\\build.zip'""" % (sshhost, target_buildroot)
    print("="*64)
    print("(XX) %s" % prep_cmd)
    print("="*64)
    subprocess.call(prep_cmd, shell=True, universal_newlines=True)

    prep_cmd = """ssh %s 'cd %s\\src & sshc.bat 1>out.txt 2>err.txt'""" % (sshhost, target_buildroot)
    print("="*64)
    print("="*64)
    print("="*64)
    print("="*64)
    print("(XX) %s" % prep_cmd)
    print("="*64)
    print("="*64)
    print("="*64)
    print("="*64)
    subprocess.call(prep_cmd, shell=True, universal_newlines=True)
    print("="*64)
    print("="*64)
    print("="*64)
    print("="*64)

    prep_cmd = """ssh %s 'cd %s & powershell -command "Compress-Archive -Path src -DestinationPath build.zip"'""" % (sshhost, target_buildroot)
    print("="*64)
    print("(XX) %s" % prep_cmd)
    print("="*64)
    subprocess.call(prep_cmd, shell=True, universal_newlines=True)

    prep_cmd = """ssh %s 'rmdir /s /q %s\\src'""" % (sshhost, target_buildroot)
    print("="*64)
    print("(XX) %s" % prep_cmd)
    print("="*64)
    subprocess.call(prep_cmd, shell=True, universal_newlines=True)

    prep_cmd = """scp %s:%s/build.zip .""" % (sshhost, target_buildroot.replace('\\', '/'))
    print("="*64)
    print("(XX) %s" % prep_cmd)
    print("="*64)
    subprocess.call(prep_cmd, shell=True, universal_newlines=True)

    prep_cmd = """ssh %s 'del /f /q %s\\build.zip'""" % (sshhost, target_buildroot)
    print("="*64)
    print("(XX) %s" % prep_cmd)
    print("="*64)
    subprocess.call(prep_cmd, shell=True, universal_newlines=True)



def main():
    turbocore.cli_this(__name__, "sshc_")
