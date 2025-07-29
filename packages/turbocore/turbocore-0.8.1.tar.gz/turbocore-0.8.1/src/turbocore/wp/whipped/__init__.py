from rich.pretty import pprint as PP
import subprocess
import json


def remote_wp(host, wp_cli_cmd, as_json=False):
    base_cmd = '''/usr/local/bin/wp --allow-root --path=/var/www/html '''
    lines = subprocess.check_output(envelope_ssh(host, base_cmd + wp_cli_cmd), shell=True, universal_newlines=True).strip().split("\n")
    if json:
        try:
            return json.loads("\n".join(lines))
        except Exception as e:
            print(str(e))
            return None
    return lines

def envelope_ssh(host, local_cmd):
    return '''ssh -q %s "%s"''' % (host, local_cmd)


def wp_user_list(host):
    res = remote_wp(
        host=host,
        wp_cli_cmd="user list --format=json --fields=ID,user_login,user_email,user_registered,user_status,roles",
        as_json=True
        )
    return res

def wp_user_meta_list(host, user_id:int, only_keys=None):
    o_only_keys = ""
    if only_keys is not None:
        o_only_keys = " --keys=" + ",".join(only_keys)
    res = remote_wp(
        host=host,
        wp_cli_cmd="user meta list %d --format=json %s" % (user_id, o_only_keys),
        as_json=True
        )
    return res

def wp_test(p1:str, p2:str, p3:str):
    """Test Funktion."""
    print("p1=%s" % p1)
    print("p2=%s" % p2)
    print("p3=%s" % p3)

def main():
    import turbocore
    turbocore.cli_this(__name__, 'wp_')
    return

    host = "werkstatt"

    #users = wp_user_list(host)
    um = wp_user_meta_list(host, 1, only_keys=["nickname"])

    print("*"*80)
    # PP(users)
    PP(um)
    print("*"*80)
