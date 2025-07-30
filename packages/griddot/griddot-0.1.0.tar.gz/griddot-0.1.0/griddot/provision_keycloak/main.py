import json
import sys
import time
import requests
import urllib3

# Disable warnings for self-signed certs
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

ADMIN_USERNAME = "temp-admin"
DEFAULT_URL = "https://localhost:8443"


def import_realm(
        url: str,
        admin_username: str,
        admin_password: str,
        realm_json_path: str,
        delete_user_when_provisioned: bool,
        email_provider_password: str = None,
        send_emails: bool = False
):
    print(f'Provisioning Keycloak at {url}')
    wait_for_keycloak_to_start(url)
    token = get_access_token(url, admin_username, admin_password)

    realm = json.load(open(realm_json_path, "r", encoding="utf-8"))

    if email_provider_password:
        if "smtpServer" in realm:
            realm["smtpServer"]["password"] = email_provider_password

    create_realm(url, realm, token)
    send_emails_to_users(url, realm["realm"], token, realm.get("users", []), send_emails=send_emails)

    if delete_user_when_provisioned:
        user_id = get_user_uuid_by_username(url, "master", token, ADMIN_USERNAME)
        delete_user(url, "master", token, user_id)
        print(f"Deleted user {ADMIN_USERNAME} from master realm.")


def get_user_uuid_by_username(url, realm, token, username):
    all_users = get_users(url, realm, token)
    for user in all_users:
        if user["username"] == username:
            return user["id"]

    raise Exception(f"User {username} not found in realm {realm}")


def wait_for_keycloak_to_start(url):
    max_retries = 60
    retries = max_retries
    while retries > 0:
        try:
            response = requests.get(url, verify=False)
            print()
            if response.status_code == 200:
                print("Keycloak is up and running.", flush=True)
                break
            else:
                print(f"Keycloak is not ready yet. Status code: {response.status_code}")
        except requests.exceptions.RequestException:
            if retries == max_retries:
                print(f"Keycloak is not ready yet .", end="", flush=True)
            else:
                print(".", end="", flush=True)
        time.sleep(1)
        retries -= 1
    else:
        print("Keycloak did not start in time.", flush=True)
        sys.exit(1)


def get_access_token(url, username, password):
    token_url = f"{url}/realms/master/protocol/openid-connect/token"
    data = {
        "client_id": "admin-cli",
        "username": username,
        "password": password,
        "grant_type": "password"
    }
    response = requests.post(token_url, data=data, verify=False)
    if response.status_code != 200:
        print("Failed to get access token:", response.text)
        sys.exit(1)
    return response.json()["access_token"]


def send_emails_to_users(url, realm, token, users, send_emails=False):
    for user in users:
        user_uuid = get_user_uuid_by_username(url, realm, token, user["username"])
        credentials_url = f"{url}/admin/realms/{realm}/users/{user_uuid}/credentials"
        credentials_response = requests.get(credentials_url, headers=get_token_header(token), verify=False)

        has_user_password = False
        if credentials_response.status_code == 200:
            has_user_password = len(credentials_response.json()) > 0

        if not has_user_password:
            if send_emails:
                print(f"Dry run: Would send email to {user['username']} for password setup.")
            else:
                send_email_for_password_setup(url, realm, token, user_uuid)
                print(f"Sent email to {user['username']} for password setup.")


def delete_user(url, realm, token, user_id):
    delete_url = f"{url}/admin/realms/{realm}/users/{user_id}"
    response = requests.delete(
        delete_url,
        headers=get_token_header(token),
        verify=False
    )
    response.raise_for_status()


def get_users(url, realm, token):
    users_url = f"{url}/admin/realms/{realm}/users"
    response = requests.get(users_url, headers=get_token_header(token), verify=False)
    response.raise_for_status()
    return response.json()


def create_realm(url, realm, token):
    realm_name = realm.get("realm")
    if not realm_name:
        raise Exception("The 'realm' dictionary must contain a 'realm' key.")

    th = get_token_header(token)

    # Check if the realm already exists
    check_url = f"{url}/admin/realms/{realm_name}"
    response = requests.get(check_url, headers=th, verify=False)

    # Update realm if it already exists
    if response.status_code == 200:
        update_url = f"{url}/admin/realms/{realm_name}"
        update_response = requests.put(update_url, headers=th, data=json.dumps(realm), verify=False)
        update_response.raise_for_status()
        print(f"Realm {realm_name} updated successfully.")
        return

    realm_url = f"{url}/admin/realms"
    response = requests.post(realm_url, headers=th, data=json.dumps(realm), verify=False)
    response.raise_for_status()
    print(f"Realm {realm_name} created successfully.")


def send_email_for_password_setup(url, realm, token, user_id):
    send_email_url = f"{url}/admin/realms/{realm}/users/{user_id}/execute-actions-email"
    send_email_response = requests.put(send_email_url,
                                       headers=get_token_header(token),
                                       params={
                                           "lifespan": 3600 * 24 * 7,
                                           "client_id": "account-console",
                                       },
                                       data=json.dumps(["UPDATE_PASSWORD"]),
                                       verify=False)
    send_email_response.raise_for_status()


def get_token_header(token):
    return {"Authorization": f"Bearer {token}",
            "Content-Type": "application/json"}
