#!/usr/local/bin/python
# Author: Scott Chubb scott.chubb@netapp.com
# Written for Python 3.4 and above
# No warranty is offered, use at your own risk.  While these scripts have been tested in lab situations, all use cases cannot be accounted for.
# Date: 7-Jan-2019
# This scripts shows how to enable and disable SSH via the REST API using requests and web calls
#   At this time there is no SDK option for this call
import requests
import base64
import json
import argparse
from solidfire.factory import ElementFactory


parser = argparse.ArgumentParser()
parser.add_argument('-sm', type=str,
                    required=True,
                    metavar='mvip',
                    help='MVIP/node name or IP')
parser.add_argument('-su', type=str,
                    required=True,
                    metavar='username',
                    help='username to connect with')
parser.add_argument('-sp', type=str,
                    required=True,
                    metavar='password',
                    help='password for user')
parser.add_argument('-st',
					choices=['enable','disable'],
                    required=True,
                    metavar='state to set ssh',
                    help='enable or disable ssh')
parser.add_argument('-dt', type=int,
                    required=False,
                    metavar='duration',
                    help='amount of time (in minutes) to enable ssh for, default is 15 minutes')
args = parser.parse_args()

mvip_ip = args.sm
user_name = args.su
user_pass = args.sp
ssh_enable = args.st
set_duration = args.dt
if set_duration == None:
	enable_duration = "00:15:00"
else:
	enable_duration = set_duration

def main():
    # Web/REST auth credentials build authentication
    auth = (user_name + ":" + user_pass)
    encodeKey = base64.b64encode(auth.encode('utf-8'))
    basicAuth = bytes.decode(encodeKey)

    # Be certain of your API version path here
    url = "https://" + mvip_ip + "/json-rpc/10.3"

	if ssh_enable == enable:
		# Various payload params in one liner
		# payload = "{\n\t\"method\": \"EnableClusterSsh\",\n    \"params\": {\n        \"duration\": "00:15:00 "\n    },\n    \"id\": 1\n}"

		# payload in JSON multi-line
		payload = "{" + \
						"\n  \"method\": \"EnableClusterSsh\"," + \
						"\n    \"params\": {" + \
						"\n    \t\"duration\": \"" + enable_duration + "\"" + \
						"\n    }," + \
						"\n    \"id\": 1" + \
					"\n}"
		# if response.status_code == 200:
			# json.loads(response.text)
		# else:
			# print("Error code returned: {}".format(response.status_code))
	else:
		# Various payload params in one liner
		# payload = "{\n\t\"method\": \"DisableClusterSsh\",\n    \n    },\n    \"id\": 1\n}"

		# payload in JSON multi-line
		payload = "{" + \
						"\n  \"method\": \"DisableClusterSsh\"," + \
						"\n    \"id\": 1" + \
					"\n}"
		# if response.status_code == 200:
			# json.loads(response.text)
		# else:
			# print("Error code returned: {}".format(response.status_code))


    headers = {
        'Content-Type': "application/json",
        'Authorization': "Basic %s" % basicAuth,
        'Cache-Control': "no-cache",
        }

    response = requests.request("POST", url, data=payload, headers=headers, verify=False)

    raw = json.loads(response.text)

    print(json.dumps(raw, indent=4, sort_keys=True))

if __name__ == "__main__":
    main()
