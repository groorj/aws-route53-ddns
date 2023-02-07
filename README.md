# aws-route53-ddns

## Table of Contents
- [What does it do ?](https://github.com/groorj/aws-route53-ddns#what-does-it-do)
- [This project uses](https://github.com/groorj/aws-route53-ddns#this-project-uses)
- [Notes](https://github.com/groorj/aws-route53-ddns#notes)

## What does it do

Create a Dynamic DNS solution using AWS Route 53. You can use your own domain and update the DNS record when your IP changes.

This will be done by having a cronjob executing a Python3 script.

## This project uses / Dependencies

- AWS Route53
- Python3
  - boto3
  - yaml
  - ipaddress
  - urllib
  - datetime
  - pytz

## Install

Install the required Python modules. You can use a virtualenv if you wish.

```
pip3 -r requirements.txt
cp -p config.yml.example config.yml
```

## Configuration

Edit the file config.yml in order to configure your parameters.

1. Change `profile_name` with your AWS profile name. Check [here](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-profiles.html) how to configure your AWS profile.
2. Change `hostname` to the host you would like to use as the DDNS host.
3. Change `host_zone_id` with your Route53 HostId.
4. (optional) You can change `dns_ttl` as needed or keep it as is.

## How to run it

`python3 ddns-updater.py config.yml`

If everything worked, this is what you will get the first time you run.

```
My configured hostname is: test12345.exampledomain.com
You didn't had a recorded IP yet.
The IP address provided is valid.
My current address is: 98.98.98.123
The IP address provided is valid.
** Different IPs, the IP changed! Will update the DNS records.
```

This will have created the host you have provided. Here is what you will get if you check the DNS record.

```
$ dig test12345.exampledomain.com

; <<>> DiG 9.10.6 <<>> test12345.exampledomain.com
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 32243
;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 512
;; QUESTION SECTION:
;test12345.exampledomain.com.		IN	A

;; ANSWER SECTION:
test12345.exampledomain.com.	2399	IN	A	98.98.98.123

;; Query time: 69 msec
;; SERVER: 192.168.1.1#53(192.168.1.1)
;; WHEN: Tue Feb 07 10:38:42 EST 2023
;; MSG SIZE  rcvd: 64
```

You can also check when was the last time that the DNS record was updated.

```
$ dig test12345.exampledomain.com TXT

; <<>> DiG 9.10.6 <<>> test12345.exampledomain.com TXT
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 54569
;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 512
;; QUESTION SECTION:
;test12345.exampledomain.com.		IN	TXT

;; ANSWER SECTION:
test12345.exampledomain.com.	2399	IN	TXT	"Last updated: 2023-02-07 15:37:29 UTC+0000"

;; Query time: 141 msec
;; SERVER: 192.168.1.1#53(192.168.1.1)
;; WHEN: Tue Feb 07 10:52:17 EST 2023
;; MSG SIZE  rcvd: 103
```



When you run the script again, you will get a message similar to this.

```
My configured hostname is: test12345.exampledomain.com
My last address is was: 98.98.98.123
The IP address provided is valid.
My current address is: 98.98.98.123
The IP address provided is valid.
Same IP, it did not change! Will not make any updates.
```

## Notes

- Add the script to a cronjob in order to keep your DNS up to date. Interval for execution should be at least 60 seconds.
- Running this code will create AWS resources in your account that might not be included in the free tier.
- Use this code at your own risk, I am not responsible for anything related to its use.