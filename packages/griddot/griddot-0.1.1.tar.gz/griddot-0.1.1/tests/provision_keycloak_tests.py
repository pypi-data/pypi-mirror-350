import subprocess
import pytest
from click.testing import CliRunner

from griddot.cli import cli
from griddot.provision_keycloak import get_access_token, wait_for_keycloak_to_start, import_realm

USERNAME = "temp-admin"
PASSWORD = "bEpTkGFAAcroN2LcCsxF1Y5WKCMs2c"
EMAIL_PASSWORD = "ppgb ddgj sjki xbya"


@pytest.fixture(scope="module", autouse=True)
def setup_once_for_module():
    # This runs once before any tests in this module
    setup_keycloak(False, False)
    yield
    # This runs once after all tests in this module


def setup_keycloak(clean, build_images):
    if build_images:
        print("Building Keycloak images...")
        subprocess.run("python3 build_images.py", check=True, shell=True, cwd="../../containers")

    if clean:
        cwd = "../../containers/keycloak"
        print("Deleting existing Keycloak resources...")
        subprocess.run("podman kube play --down --force dev.yaml", check=False, shell=True, cwd=cwd)

        print("Starting Keycloak...")
        subprocess.run("podman kube play --replace dev.yaml", check=True, shell=True, cwd=cwd)


def wait_for_keycloak_and_get_token():
    url = "https://localhost:8443"
    wait_for_keycloak_to_start(url)
    token = get_access_token(url, USERNAME, PASSWORD)
    return url, token


def test_keycloak_provisioner():
    url, _ = wait_for_keycloak_and_get_token()
    platform_realm = "../../containers/keycloak/realms/platform-realm.json"
    import_realm(url, USERNAME, PASSWORD, platform_realm, False, EMAIL_PASSWORD, True)


def test_cli():
    url, _ = wait_for_keycloak_and_get_token()

    runner = CliRunner()
    result = runner.invoke(cli, [
        'provision-keycloak',
        '--url', url,
        '--username', USERNAME,
        '--password', PASSWORD,
        '--realms-dir', '../../containers/keycloak/realms',
        '--delete-user-when-provisioned', 'No',
        '--email-password', EMAIL_PASSWORD
    ])

    assert result.exit_code == 0, result.output
