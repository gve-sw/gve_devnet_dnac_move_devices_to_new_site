#!/usr/bin/env python3
""" Copyright (c) 2023 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at
           https://developer.cisco.com/docs/licenses
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""

import requests, json, os
from requests.auth import HTTPBasicAuth
import time 

import urllib3
urllib3.disable_warnings()

from dotenv import load_dotenv
load_dotenv()

USERNAME=os.getenv("USERNAME")
PASSWORD=os.getenv("PASSWORD")
BASE_URL=os.getenv("BASE_URL")

WLC_IP=os.getenv("WLC_IP")
NEW_SITE=os.getenv("NEW_SITE")
PROFILE=os.getenv("PROFILE")


AUTH_URL = '/dna/system/api/v1/auth/token'
SITE_URL = '/dna/intent/api/v1/site'

def get_dnac_jwt_token():
    response = requests.post(BASE_URL + AUTH_URL,
                             auth=HTTPBasicAuth(USERNAME, PASSWORD),
                             verify=False)
    token = response.json()['Token']
    
    get_devices(token)
  
def get_devices(token):
    url = "/dna/intent/api/v1/network-device"
    payload = None
    headers = {
        "X-Auth-Token": token,
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    devices = requests.get(BASE_URL+url, headers=headers, data = payload, verify=False).json()
    
    WLCs=[]
    for device in devices["response"]:
        wlc_entry={}
        if device["family"] == "Wireless Controller":
            wlc_entry["ip"]=device["managementIpAddress"]
            wlc_entry["id"]=device["id"]
            wlc_entry["name"]=device["hostname"]
            wlc_entry["APs"]=[]
            WLCs.append(wlc_entry)
    
    for device in devices["response"]:
        if device["family"] == "Unified AP":
            for wlc in WLCs:
                if wlc["ip"]== device["associatedWlcIp"]:
                    wlc["APs"].append(device["hostname"])

    delete_device(token, WLCs)
    
def delete_device(token,WLCs):
    target_wlc_ip=WLC_IP
    target_wlc_id=""

    
    for wlc in WLCs:
        if wlc["ip"] == target_wlc_ip:
            target_wlc_id=wlc["id"]
            wlc_name=wlc["name"]
            print("Target WLC IP: ",target_wlc_id)
            print("Target WLC ID: ",target_wlc_ip)

            url = f"/dna/intent/api/v1/network-device/{target_wlc_id}"
            
            payload = None
            headers = {
                "X-Auth-Token": token,
                "Content-Type": "application/json",
                "Accept": "application/json"
            }

            response = requests.delete(BASE_URL +url, headers=headers, data = payload, verify=False).json()
          
            print(json.dumps(response, indent=2))
            taskId=response["response"]["taskId"]
            print("Task ID is:", taskId)

            time.sleep(200)
            deletion_status=get_task(token,taskId)
            print("========================")
            if deletion_status != "flase":

                add_taskID=add_device(token,target_wlc_ip)
                print("Add Device Status")
                time.sleep(200)
                add_status=get_task(token,taskId=add_taskID)
                if deletion_status != "flase":

                    print("PROVISION WLC")
                    provision_status=provision_wlc(token,wlc_name)
                    if provision_status == "SUCCESS":

                        print("PROVISION APs")
                        provision_ap(token, wlc["APs"])
            



def get_task(token,taskId):
    url = f"/dna/intent/api/v1/task/{taskId}"

    payload = None

    headers = {
        "X-Auth-Token": token,
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    response = requests.request('GET', BASE_URL +url, headers=headers, data = payload, verify=False).json()
    print(json.dumps(response, indent=2))
    print("==============================")

    return str(response["response"]["isError"])
    
   


def add_device(token,target_wlc_ip):
    url = "/dna/intent/api/v1/network-device"
    device_ip=target_wlc_ip
   
    CREDS_file = open('wlc_creds.json')
    CREDS = json.load(CREDS_file)
    

    device_object = {
            "ipAddress": [
                device_ip
            ],
            "type": CREDS["type"],
            "computeDevice": False,
            "snmpVersion": CREDS["snmp_version"],
            "snmpROCommunity": CREDS["snmp_ro_community"],
            "snmpRWCommunity": CREDS["snmp_rw_community"],
            "snmpRetry": CREDS["snmp_retry"],
            "snmpTimeout": CREDS["snmp_timeout"],
            "cliTransport": CREDS["cli_transport"],
            "userName": CREDS["username"],
            "password": CREDS["password"],
            "enablePassword": CREDS["enable_password"],
            "netconfPort": CREDS["netconf_port"]
        }
    CREDS_file.close()
    #print(device_object)

    headers = {
        "X-Auth-Token": token,
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    response = requests.post(BASE_URL +url, data=json.dumps(device_object), headers=headers, verify=False).json()
    print(json.dumps(response, indent=2))
    taskId=response["response"]["taskId"]
    print("Task ID is:", taskId)
    return taskId
   


def get_execution(token,executionId):
    url = f"/dna/intent/api/v1/dnacaap/management/execution-status/{executionId}"

    payload = None

    headers = {
        "X-Auth-Token": token,
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    response = requests.request('GET', BASE_URL + url, headers=headers, data = payload, verify=False).json()
    print(json.dumps(response, indent=2))
    return str(response["status"])
    

def provision_wlc(token,WLC_NAME):

    url = "/dna/intent/api/v1/wireless/provision"
    headers={
        "X-Auth-Token": token,
        "Content-Type": "application/json",
        "Accept": "application/json"
    }


    payload = [
        {
            "deviceName": WLC_NAME,
            "site": NEW_SITE,
            "managedAPLocations": [
                NEW_SITE
            ],
          
        },
    ]

    print(payload)
    response = requests.post(BASE_URL + url,headers=headers, data=json.dumps(payload), verify=False).json()
    print(json.dumps(response, indent=2))
    executionId=response["executionId"]
    print("Execution Id:", executionId)
    time.sleep(200)
    status=get_execution(token,executionId)
    return status

def provision_ap(token,APs):
    for ap in APs:
        print("PROVISION", ap)
        
        url='/dna/intent/api/v1/wireless/ap-provision'
        headers={
            "X-Auth-Token": token,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
       
        payload = {
                    "rfProfile": PROFILE,
                    "siteId": NEW_SITE,
                    "deviceName": ap,
                    "type": "ApWirelessConfiguration",
                    "siteNameHierarchy": NEW_SITE
                }

        response = requests.post(BASE_URL+url, headers=headers, data=json.dumps(payload), verify=False).json()
        print(json.dumps(response, indent=2))
        executionId=response["executionId"]
        print("Execution Id:", executionId)
        time.sleep(90)
        get_execution(token,executionId)
        print("================")

if __name__ == '__main__':
    get_dnac_jwt_token()