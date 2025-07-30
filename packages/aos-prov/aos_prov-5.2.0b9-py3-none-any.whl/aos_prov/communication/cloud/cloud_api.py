#
#  Copyright (c) 2018-2024 Renesas Inc.
#  Copyright (c) 2018-2024 EPAM Systems Inc.
#
import sys
from urllib.parse import urlencode

import requests
from aos_keys.check_version import DOCS_URL
from aos_prov.utils.common import (
    REQUEST_TIMEOUT,
    print_error,
    print_left,
    print_message,
    print_success,
)
from aos_prov.utils.errors import CloudAccessError, DeviceRegisterError
from aos_prov.utils.user_credentials import UserCredentials
from packaging.version import Version
from requests.exceptions import InvalidJSONError

if sys.version_info > (3, 9):
    from importlib import resources as pkg_resources  # noqa: WPS433, WPS440
else:
    import importlib_resources as pkg_resources  # noqa: WPS433, WPS440

try:
    from importlib.metadata import version
except ImportError:
    from importlib_metadata import version

DEFAULT_REGISTER_HOST = 'aoscloud.io'
DEFAULT_REGISTER_PORT = 10000


class CloudAPI:
    FILES_DIR = 'aos_prov'
    ROOT_CA_CERT_FILENAME = 'files/1rootCA.crt'
    REGISTER_URI_TPL = 'https://{}:{}/api/v10/units/provisioning/'
    SUPPORTED_SOFTWARE_URI_TPL = 'https://{}:{}/api/v10/units/provisioning/supported-software/'
    USER_ME_URI_TPL = 'https://{}:{}/api/v10/users/me/'
    UNIT_STATUS_URL = 'https://{}:{}/api/v10/units/?{}'
    FIND_UNIT_TPL = 'https://{}:{}/api/v10/units/?{}'
    LINK_TO_THE_UNIT_ON_CLOUD_TPL = 'https://{}/oem/units/{}'

    def __init__(self, user_credentials: UserCredentials, cloud_api_port: int = DEFAULT_REGISTER_PORT):
        self._cloud_api_host = user_credentials.cloud_url
        self._cloud_api_port = cloud_api_port if cloud_api_port else DEFAULT_REGISTER_PORT
        self._user_credentials = user_credentials

    def check_cloud_access(self):
        """Check user access on the cloud and his role is OEM.

        Raises:
            CloudAccessError: If user haven't access to the cloud or his role is not OEM.
        """
        try:  # noqa: WPS229
            print_left('Checking of access to the AosEdge...')
            url = self.USER_ME_URI_TPL.format(self._cloud_api_host, self._cloud_api_port)
            server_certificate = pkg_resources.files(self.FILES_DIR) / self.ROOT_CA_CERT_FILENAME
            with pkg_resources.as_file(server_certificate) as server_certificate_path:
                with self._user_credentials.user_credentials as temp_creds:
                    resp = requests.get(
                        url,
                        verify=server_certificate_path,
                        cert=(temp_creds.cert_file_name, temp_creds.key_file_name),
                        timeout=REQUEST_TIMEOUT,
                    )

                if resp.status_code != 200:  # noqa: WPS432
                    print_message('[red]Received not HTTP 200 response. ' + str(resp.text))
                    raise CloudAccessError('You do not have access to the cloud!')

                user_info = resp.json()
                if user_info['role'] != 'oem':
                    print_message(f'[red]invalid user role: {resp.text}')
                    raise CloudAccessError('You should use OEM account!')

            print_success('DONE')
            print_left('Operation will be executed on domain:')
            print_success(self._cloud_api_host)
            print_left('OEM:')
            print_success(user_info['oem']['title'])
            print_left('user:')
            print_success(user_info['username'])
        except ConnectionError as exc:
            raise CloudAccessError('Failed to connect to the cloud with error: ' + str(exc)) from exc
        except InvalidJSONError as exc:
            raise CloudAccessError('Failed to parse the cloud response with error: ' + str(exc)) from exc
        except (requests.exceptions.RequestException, ValueError, OSError) as exc:
            raise CloudAccessError('Failed to connect to the cloud with error: ' + str(exc)) from exc

    def check_supported_software(self):  # noqa: WPS238
        """Check that Cloud supports current software version.

        Raises:
            CloudAccessError: If current software version is not supported by Cloud.
        """
        try:
            installed_version = Version(version('aos-prov'))
            print_left(f'Checking of current software version: {installed_version} with the cloud...')
            url = self.SUPPORTED_SOFTWARE_URI_TPL.format(self._cloud_api_host, self._cloud_api_port)
            server_certificate = pkg_resources.files(self.FILES_DIR) / self.ROOT_CA_CERT_FILENAME
            with pkg_resources.as_file(server_certificate) as server_certificate_path:
                with self._user_credentials.user_credentials as temp_creds:
                    resp = requests.get(
                        url,
                        verify=server_certificate_path,
                        cert=(temp_creds.cert_file_name, temp_creds.key_file_name),
                        timeout=REQUEST_TIMEOUT,
                    )

                if resp.status_code != 200:  # noqa: WPS432
                    print_message('[red]Received not HTTP 200 response. ' + str(resp.text))
                    raise CloudAccessError('You do not have access to the cloud!')

                supported_software = resp.json()
                if not supported_software.get('software'):
                    print_message(f'[red]invalid response: {resp.text}')
                    raise CloudAccessError('There is no software key into response!')

                supported = False
                for software in supported_software['software']:
                    if software.get('name') == 'aos-provisioning' and software.get('min_version'):
                        if installed_version > Version(software['min_version']):
                            print_success('DONE')
                            supported = True
                        else:
                            print_message(
                                f'[red]Current software version {installed_version} is not supported by Cloud. '
                                f'Minimum required version is {software["min_version"]}',
                            )
                        break

                if not supported:
                    print_message(f'Perform updating/installing package according to AosEdge documentation: {DOCS_URL}')
                    raise CloudAccessError('Current software is not supported by Cloud!')
        except ConnectionError as exc:
            raise CloudAccessError('Failed to connect to the cloud with error: ' + str(exc)) from exc
        except InvalidJSONError as exc:
            raise CloudAccessError('Failed to parse the cloud response with error: ' + str(exc)) from exc
        except (requests.exceptions.RequestException, ValueError, OSError) as exc:
            raise CloudAccessError('Failed to connect to the cloud with error: ' + str(exc)) from exc

    def register_device(self, payload):
        """Register device in cloud.

        Args:
            payload: Payload to register Unit

        Raises:
            DeviceRegisterError: Failed to register unit.

        Returns:
            registered metadata from Cloud
        """
        print_message('Registering the unit ...')
        end_point = self.REGISTER_URI_TPL.format(self._cloud_api_host, self._cloud_api_port)

        response = None
        try:
            server_certificate = pkg_resources.files(self.FILES_DIR) / self.ROOT_CA_CERT_FILENAME
            with pkg_resources.as_file(server_certificate) as server_certificate_path:
                with self._user_credentials.user_credentials as temp_creds:
                    ret = requests.post(
                        end_point,
                        json=payload,
                        verify=server_certificate_path,
                        cert=(temp_creds.cert_file_name, temp_creds.key_file_name),
                        timeout=REQUEST_TIMEOUT,
                    )

                    if ret.status_code == 400:  # noqa: WPS432
                        try:  # noqa: WPS505
                            try:  # noqa: WPS505
                                answer = ret.json()['non_field_errors'][0]
                                print_error(f'Registration error: {answer}')
                            except Exception:  # noqa: S110
                                pass  # noqa: WPS420

                        except UnicodeDecodeError:
                            pass  # noqa: WPS420
                    ret.raise_for_status()
                    response = ret.json()
        except InvalidJSONError as exc:
            raise DeviceRegisterError('Failed to parse the cloud response with error: ' + str(exc)) from exc
        except (requests.exceptions.RequestException, ValueError, OSError) as exc:
            raise DeviceRegisterError(f'Failed to register unit. Response: {response}') from exc

        return response

    def check_unit_is_not_provisioned(self, system_uid):
        print_message("Getting unit's status on the cloud ...")
        try:
            end_point = self.UNIT_STATUS_URL.format(
                self._cloud_api_host,
                self._cloud_api_port,
                urlencode({'system_uid': system_uid}),
            )
            server_certificate = pkg_resources.files(self.FILES_DIR) / self.ROOT_CA_CERT_FILENAME
            with pkg_resources.as_file(server_certificate) as server_certificate_path:
                with self._user_credentials.user_credentials as temp_creds:
                    response = requests.get(
                        end_point,
                        verify=server_certificate_path,
                        cert=(temp_creds.cert_file_name, temp_creds.key_file_name),
                        timeout=REQUEST_TIMEOUT,
                    )

        except InvalidJSONError as exc:
            raise DeviceRegisterError('Failed to parse the cloud response with error: ' + str(exc)) from exc
        except (requests.exceptions.RequestException, ValueError, OSError) as exc:
            raise DeviceRegisterError('Failed to HTTP GET: ', exc) from exc

        try:
            response_json = response.json()
        except InvalidJSONError as exc:
            raise DeviceRegisterError('Failed to parse the cloud response with error: ' + str(exc)) from exc

        if response_json.get('items') is None or response_json.get('total') is None:
            raise DeviceRegisterError('Invalid answer from the cloud. Please update current library')

        if response_json.get('total') == 0:
            # There is no such unit on the cloud
            return

        status = response_json.get('items', [{}])[0].get('status')
        if status is None:
            return

        if status != 'new':
            raise DeviceRegisterError(f'Unit is in status "{status}". Please do deprovisioning first.')

    def get_unit_link_by_system_uid(self, system_uid):
        end_point = self.FIND_UNIT_TPL.format(
            self._cloud_api_host,
            self._cloud_api_port,
            urlencode({'system_uid': system_uid}),
        )
        try:
            server_certificate = pkg_resources.files(self.FILES_DIR) / self.ROOT_CA_CERT_FILENAME
            with pkg_resources.as_file(server_certificate) as server_certificate_path:
                with self._user_credentials.user_credentials as temp_creds:
                    response = requests.get(
                        end_point,
                        verify=server_certificate_path,
                        cert=(temp_creds.cert_file_name, temp_creds.key_file_name),
                        timeout=REQUEST_TIMEOUT,
                    )
            unit_id = response.json()['items'][0]['id']
            unit_domain = self._cloud_api_host
            if not unit_domain.startswith('oem.'):
                unit_domain = f'oem.{unit_domain}'
            return self.LINK_TO_THE_UNIT_ON_CLOUD_TPL.format(unit_domain, unit_id)
        except Exception:
            return None
