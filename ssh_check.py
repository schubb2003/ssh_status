#!/usr/local/bin/python
# Author: Scott Chubb scott.chubb@netapp.com
# Written for Python 3.4 and above
# No warranty is offered, use at your own risk.  While these scripts have been tested in lab situations, all use cases cannot be accounted for.
# Date: 7-Jan-2019
# This scripts shows how to check SSH statu via the REST API using requests and web calls
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
args = parser.parse_args()

mvip_ip = args.sm
user_name = args.su
user_pass = args.sp

def main():
    # Web/REST auth credentials build authentication
    auth = (user_name + ":" + user_pass)
    encodeKey = base64.b64encode(auth.encode('utf-8'))
    basicAuth = bytes.decode(encodeKey)

    # Be certain of your API version path here
    url = "https://" + mvip_ip + "/json-rpc/10.3"

	# Various payload params in one liner
	# payload = "{\n\t\"method\": \"GetClusterSshInfo\",\n    },\n    \"id\": 1\n}"

	# payload in JSON multi-line
	payload = "{" + \
					"\n  \"method\": \"GetClusterSshInfo\"," + \
					"\n    \"id\": 1" + \
				"\n}"

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
