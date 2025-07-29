import hashlib
import urllib.parse
import turbocore
import os
import requests
from rich.pretty import pprint as PP
import sys
import textwrap


def sha256file(filename):
    h = hashlib.sha256()
    with open(filename, 'rb') as f:
        for chunk in iter(lambda: f.read(8192*4), b""):
            h.update(chunk)
    return h.hexdigest().lower()


def get_base_url():
    host = get_base_host()
    return "https://%s" % host

def get_base_host():
    host = os.environ.get("TJI_HOST")
    return host


def get_token():
    token = os.environ.get("TJI_TOKEN")
    return token


def get_user():
    token = os.environ.get("TJI_USER")
    return token


def req(verb, route, data=None, stream=False) -> requests.Response:
    
    if not route.startswith("/") and not route.startswith("http://") and not route.startswith("https://"):
        raise Exception("parameter 'route' must start with a '/'")

    f_ = {
        "GET": requests.get,
        "POST": requests.post,
    }

    if not verb.upper() in f_.keys():
        raise Exception("Unsupported http verb '%s'" % verb)

    hdr = {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    #    "Authorization": "Bearer %s" % get_token()

    auth=(get_user(), get_token())
    url = get_base_url() + route
    
    # special case we have a full url
    if not route.startswith("/"):
        url = route

    url_host_actual = url.split("//")[1].split("/")[0].split(":")[0]
    if url_host_actual is None or url_host_actual == "" or url_host_actual != get_base_host():
        raise Exception("Unsafe host in API call detected, %s" % str(url_host_actual))
    
    #res = f_[verb](url=url, headers=hdr, data=data)
    res = f_[verb](url=url, headers=hdr, data=data, auth=auth)
    return res


def ji_test():
    """test function.
    """
    print("test it is")

    res = req(verb="GET", route="/rest/api/3/myself")
    x = res.json()
    PP(x)
    sys.exit(0)


def apiget(src):
    res = req(verb="GET", route=src)
    return res.json()


def apistream(src, local_filename):
    res = req(verb="GET", route=src, stream=True)
    with open(local_filename, "wb") as f:
        for chunk in res.iter_content(chunk_size=8192*8):
            f.write(chunk)


def project_key():
    if os.path.isfile(".key"):
        with open(".key", "r") as f:
            return f.read().split("\n")[0].strip()
    return os.getcwd().split(os.sep)[-1]


def compat_alpha_num(src: str) -> str:
    alpha = " abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    res = ""
    for i in range(0, len(src)):
        c = src[i]
        if c in alpha:
            res += c
    while "  " in res:
        res = res.replace("  ", " ")
    return res.strip()


def parse_adf(doc_node):
    if isinstance(doc_node, dict):
        if doc_node.get("type") == "text":
            return doc_node.get("text", "")
        elif "content" in doc_node:
            calbr = ""
            if doc_node.get("type") == "paragraph":
                calbr = "\n"
            return "\n".join(parse_adf(child) for child in doc_node["content"]) + calbr
    elif isinstance(doc_node, list):
        return "\n".join(parse_adf(child) for child in doc_node)
    return ""


def ji_customs():
    res = req(verb="GET", route="/rest/api/2/field")
    reso = res.json()
    for field in reso:
        if field["custom"] == True:
            field_id = field["id"]
            field_name = field["name"]
            field_type = field["schema"]["type"]
            print("%s\t%s\t%s" % (field_id, field_name, field_type))


def ji_issue_data(issue_key):
    res = req(verb="GET", route="/rest/api/3/issue/%s?fields=description,attachment" % issue_key)
    reso = res.json()
    desc_adf = reso["fields"].get("description", {})
    txt = parse_adf(desc_adf)
    wrapper = textwrap.TextWrapper(width=64, break_long_words=False, break_on_hyphens=False, replace_whitespace=False)
    print("\n".join(wrapper.wrap(txt)))
    print("-"*80)
    #PP(reso["fields"]["attachment"])
    atti=0
    for att in reso["fields"]["attachment"]:
        atti+=1
        att_content = att["content"]
        att_filename = att["filename"]
        att_mime = att["mimeType"]
        att_size = int(att["size"])
        att_who = compat_alpha_num(att["author"]["displayName"])

        print(att_content)
        print(att_filename)
        print(att_mime)
        print(att_size)
        print(att_who)
        filename = "attach-%d" % atti
        apistream(att_content, filename)
        print(sha256file(filename))

    sys.exit(0)


def ji_changes(minutes_back=60):
    minutes = int(minutes_back)
    proj = project_key()
    res = req(verb="GET", route="/rest/api/3/search?maxResults=250&jql=" + urllib.parse.quote('created >= -%dm and project = %s' % (minutes, proj)))
    x = res.json()
    for iss in x["issues"]:
        i_k = iss["key"]
        i_self = iss["self"]
        i_labels = iss["fields"]["labels"]
        i_summary = iss["fields"]["summary"]
        i_status = iss["fields"]["status"]["name"]
        i_type = iss["fields"]["issuetype"]["name"]
        i_browse = get_base_url() + "/browse/" + i_k

        print(i_k)
        print(i_self)
        print(i_labels)
        print(i_summary)
        print(i_status)
        print(i_type)
        print(i_browse)
        print("--")


def ji_dev():
    """test dev function.
    """
    proj = project_key()
    last_int_hours = 48
    res = req(verb="GET", route="/rest/api/3/search?maxResults=250&jql=" + urllib.parse.quote('created >= -%dh and project = %s' % (last_int_hours, proj)))
    x = res.json()
    PP(x)

    sys.exit(0)


def main():
    turbocore.cli_this(__name__, 'ji_')
    return
