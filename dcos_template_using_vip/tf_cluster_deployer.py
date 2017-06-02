import argparse
import os
import jinja2
import json
import requests
from bs4 import BeautifulSoup

# to not log warning messages everytime we make a not verified TLS request
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


FLAGS = None


def get_deploymnet_json():

    # => Opening template
    template_path = os.path.join(os.getcwd(), "dcos.template.jinja2")
    with open(template_path, "r") as f:
        template = jinja2.Template(f.read())
        # => Rendering template
        deployment_json = template.render(**FLAGS)

        # => Validating json
        try:
            json.loads(deployment_json)
        except ValueError as e:
            return None

        return deployment_json


def deploy():

    # => Getting deployment json
    deployment_json = get_deploymnet_json()
    print(deployment_json)

    # => Getting cookie for Marathon request
    cookie = login_in_dcos()
    print(cookie)

    custom_headers = build_auth_req_headers(cookie)
    custom_headers['Content-Type'] = 'application/json'

    marathon_group_endpoint = "https://" + FLAGS["cluster_url"] + "/marathon/v2/groups"

    response = requests.post(
         marathon_group_endpoint,
         data=deployment_json,
         headers=custom_headers,
         verify=False
    )

def build_auth_req_headers(token_cookie):

    authorization_code = token_cookie.get("dcos-acs-auth-cookie")
    header = {'Cookie': '{key}={value}'.format(key="dcos-acs-auth-cookie", value=authorization_code)}
    return header



def login_in_dcos():
    """
    Function that simulates the login in DCOS flow with SSO to obtain a valid
    cookie that will be used to make requests to Marathon
    """

    # Mandatory parameters
    url = "https://" + FLAGS["cluster_url"] + "/login?firstUser=false"
    username = FLAGS["sso_username"]
    password = FLAGS["sso_password"]

    # First request to mesos master to be redirected to gosec sso login page and be given a session cookie
    first_response = requests.get(url, verify=False)
    callback_url = first_response.url
    session_id_cookie = first_response.history[-1].cookies

    # Parse response body for hidden tags needed in the data of our login post request
    body = first_response.text
    xml_parser = BeautifulSoup(body, "lxml")
    hidden_tags = [tag.attrs for tag in xml_parser.find_all("input", type="hidden")]
    data = {tag['name']: tag['value'] for tag in hidden_tags
            if tag['name'] == 'lt' or tag['name'] == 'execution'}

    # Add the rest of needed fields and login credentials in the data of our login post request and send it
    data.update(
        {'_eventId': 'submit',
         'submit': 'LOGIN',
         'username': username,
         'password': password
         }
    )
    login_response = requests.post(callback_url, data=data, cookies=session_id_cookie, verify=False)

    # Obtain dcos cookie from response
    return login_response.history[-1].cookies

if __name__ == '__main__':

    # => Parsing input arguments
    # ------------------------------------------------------------
    parser = argparse.ArgumentParser()
    parser.register("type", "bool", lambda v: v.lower() == "true")

    # => Deployment arguments (Mandatory)

    parser.add_argument("--cluster_url", type=str, help="", required=True)
    parser.add_argument("--sso_username", type=str, help="", required=True)
    parser.add_argument("--sso_password", type=str, help="", required=True)

    # => Tensorflow cluster configuration
    parser.add_argument("--cluster_name", type=str, default="test-tf-cluster", help="")
    parser.add_argument("--docker_image", type=str, default="intelligence-tensorflow:1.1.0", help="")

    parser.add_argument("--worker_replicas", type=int, default="3", help="")
    parser.add_argument("--worker_cpu", type=int, default="2", help="")
    parser.add_argument("--worker_mem", type=int, default="2048", help="")

    parser.add_argument("--ps_replicas", type=int, default="1", help="")
    parser.add_argument("--ps_cpu", type=int, default="1", help="")
    parser.add_argument("--ps_mem", type=int, default="1024", help="")

    parser.add_argument("--vip_port", type=int, default="2333", help="")

    parser.add_argument("--tensorboard", type=bool, default="false", help="")
    parser.add_argument("--tensorboard_cpu", type=int, default="1", help="")
    parser.add_argument("--tensorboard_mem", type=int, default="512", help="")
    parser.add_argument("--train_dir", type=str, default="/tmp/", help="")

    parsed, unparsed = parser.parse_known_args()
    FLAGS = vars(parsed)
    print(FLAGS)

    # => Deploying
    # ------------------------------------------------------------
    deploy()


