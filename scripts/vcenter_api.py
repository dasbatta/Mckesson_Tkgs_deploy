#!/usr/bin/env python3

import base64
import json
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from pyVmomi import vim
import pmsg

def api_get(server, path, token):
    header = {"vmware-api-session-id": token}
    url = "https://"+server+path
    response = requests.get(url, headers=header, verify=False)
    if response.status_code > 299:
        #pmsg.fail ("Call to " + server + path + " Failed. Error occured in prepare-vsphere.pl: function: api_get ("+path+")")
        return None
    json_obj = json.loads(response.content.decode())
    return json_obj

def api_delete(server, path, token):
    if not dry_run:
        header = {"vmware-api-session-id": token}
        url = "https://"+server+path
        response = requests.delete(url, headers=header, verify=False)
        if response.status_code > 299:
            pmsg.fail ("Call to " + server + path + " Failed. Error occured in prepare-vsphere.pl: function api_delete.")
            exit (2)
    else:
        pmsg.dry_run  ("Not deleting " + path + ".")
    return True

def api_post(server, path, token, data, success_code):
    # Returns True or False
    header = {"vmware-api-session-id": token, "Content-Type": "application/json"}
    url = "https://"+server+path
    response = requests.post(url, headers=header, verify=False, json=data)

    # Some posts don't return content
    try:
        json_obj = json.loads(response.content.decode())
    except:
        pass
    if response.status_code == success_code:
        return True
    pmsg.warning ("Response: " + "api_post with data: " + str(data) + " returned status code: " + str(response.status_code))
    return False

def vcenter_login(server, username, pw):
    args = {'host': server, 'port': 443, 'user': username, 'password': pw, 'disable_ssl_verification': True}
    url = "https://" + server + "/rest/com/vmware/cis/session"
    creds = username + ":" + pw
    base64_creds = base64.b64encode(bytes(creds,'utf-8'))
    header = {"authorization": "Basic "+base64_creds.decode('ascii')}
    response = requests.post(url, headers=header, verify=False)
    if response.status_code == 200:
        jcontent = json.loads(response.content.decode())
        return jcontent["value"]
    return ''
