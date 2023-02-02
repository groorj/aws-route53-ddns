#!/usr/bin/env python

# from __future__ import print_function
import sys
import yaml
# import pprint
import boto3
import ipaddress
import urllib.request

class DDNSUpdater:

    def __init__(self, config):
        self.config = config

    def validate_ip_address(ip_address):
        try:
            ip_object = ipaddress.ip_address(ip_address)
            print("The IP address '{ip_object}' is valid.")
        except ValueError:
            print("The IP address '{ip_string}' is not valid")

# get configs
def _get_config_from_file(filename):
    config = {}
    with open(filename, "r") as stream:
        config = yaml.load(stream, Loader=yaml.SafeLoader)
    return config

# start boto3 session
def get_boto_session(profile_name, aws_region):
    return boto3.Session(profile_name=profile_name, region_name=aws_region)

# 
def get_latest_ip_address(my_hostname):
    response = client.test_dns_answer(
        HostedZoneId=host_zone_id,
        RecordName=my_hostname,
        RecordType='A',
    )
    # print(response)

    if response['RecordData']:
        # print("it has value")
        # print(response['RecordName'])
        # print(response['RecordData'][0])
        return response['RecordData'][0]
    else:
        # print("it DOES NOT have value")
        False

# get public IP
def get_public_ip():
    public_ip = urllib.request.urlopen('http://checkip.amazonaws.com/').read().decode('utf8')
    # treat exceptions like connection timeout
    # return "127.0.0.1"
    return public_ip.strip()

# main
if __name__ == "__main__":
    # get config
    config = _get_config_from_file(sys.argv[1])
    ddns_updater = DDNSUpdater(config)
    # print("Current configuration:\n", yaml.dump(config, default_flow_style=False))
    
    # config variables
    profile_name = config.get("profile_name")
    my_hostname = config.get("assertions").get("hostname", []) 
    aws_region = config.get("assertions").get("region", [])
    save_txt_record = config.get("assertions").get("save_txt_record", [])
    host_zone_id = config.get("assertions").get("host_zone_id", [])

    # start boto Session
    boto_session = get_boto_session(config["profile_name"], aws_region)
    client = boto_session.client("route53", region_name=aws_region)

    # get the latest IP address based on the provided hostname
    my_ip_address = get_latest_ip_address(my_hostname)
    print(my_ip_address)

    # check if IP address is valid
    DDNSUpdater.validate_ip_address(my_ip_address)

    # get current IP address
    public_ip = get_public_ip()
    print(public_ip)

    # check if current IP address is valid
    DDNSUpdater.validate_ip_address(public_ip)

    # compare if current IP address is different from latest
    if my_ip_address == public_ip:
        print("Same IP, did not change!")
    else:
        print("Different IPs, IP changed!")

    # update DNS accordingly 



    # print(profile_name)
    # print(aws_region)
    # print(save_txt_record)
    # print(host_zone_id)

# End;
