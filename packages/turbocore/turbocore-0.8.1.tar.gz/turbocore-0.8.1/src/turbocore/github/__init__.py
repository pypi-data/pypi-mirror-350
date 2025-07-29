import os
import requests
from rich.pretty import pprint as PP


def base_url():
    return "https://api.github.com"


def hdr():
    return {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer %s" % os.environ.get("TC_GHT", "missing-token-in-env-TC_GHT")
    }


def gh_repo():
    x = requests.get(base_url() + "/user/repos?affiliation=collaborator", headers=hdr())
    PP(x.json())

def gh_me():
    x = requests.get(base_url() + "/user", headers=hdr())
    PP(x.json())


def main():
    import turbocore
    turbocore.cli_this(__name__, 'gh_')
