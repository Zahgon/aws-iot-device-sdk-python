# /*
# * Copyright 2010-2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# *
# * Licensed under the Apache License, Version 2.0 (the "License").
# * You may not use this file except in compliance with the License.
# * A copy of the License is located at
# *
# *  http://aws.amazon.com/apache2.0
# *
# * or in the "license" file accompanying this file. This file is distributed
# * on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# * express or implied. See the License for the specific language governing
# * permissions and limitations under the License.
# */


from AWSIoTPythonSDK.exception.AWSIoTExceptions import DiscoveryInvalidRequestException
from AWSIoTPythonSDK.exception.AWSIoTExceptions import DiscoveryUnauthorizedException
from AWSIoTPythonSDK.exception.AWSIoTExceptions import DiscoveryDataNotFoundException
from AWSIoTPythonSDK.exception.AWSIoTExceptions import DiscoveryThrottlingException
from AWSIoTPythonSDK.exception.AWSIoTExceptions import DiscoveryTimeoutException
from AWSIoTPythonSDK.exception.AWSIoTExceptions import DiscoveryFailure
from AWSIoTPythonSDK.core.greengrass.discovery.models import DiscoveryInfo
from AWSIoTPythonSDK.core.protocol.connection.alpn import SSLContextBuilder
import re
import sys
import ssl
import time
import errno
import logging
import socket
import platform
if platform.system() == 'Windows':
    EAGAIN = errno.WSAEWOULDBLOCK
else:
    EAGAIN = errno.EAGAIN


class DiscoveryInfoProvider(object):

    REQUEST_TYPE_PREFIX = "GET "
    PAYLOAD_PREFIX = "/greengrass/discover/thing/"
    PAYLOAD_SUFFIX = " HTTP/1.1\r\n" # Space in the front
    HOST_PREFIX = "Host: "
    HOST_SUFFIX = "\r\n\r\n"
    HTTP_PROTOCOL = r"HTTP/1.1 "
    CONTENT_LENGTH = r"content-length: "
    CONTENT_LENGTH_PATTERN = CONTENT_LENGTH + r"([0-9]+)\r\n"
    HTTP_RESPONSE_CODE_PATTERN = HTTP_PROTOCOL + r"([0-9]+) "

    HTTP_SC_200 = "200"
    HTTP_SC_400 = "400"
    HTTP_SC_401 = "401"
    HTTP_SC_404 = "404"
    HTTP_SC_429 = "429"

    LOW_LEVEL_RC_COMPLETE = 0
    LOW_LEVEL_RC_TIMEOUT = -1

    _logger = logging.getLogger(__name__)

    def __init__(self, caPath="", certPath="", keyPath="", host="", port=8443, timeoutSec=120):
        """

        The class that provides functionality to perform a Greengrass discovery process to the cloud.

        Users can perform Greengrass discovery process for a specific Greengrass aware device to retrieve
        connectivity/identity information of Greengrass cores within the same group.

        **Syntax**

        .. code:: python

          from AWSIoTPythonSDK.core.greengrass.discovery.providers import DiscoveryInfoProvider

          # Create a discovery information provider
          myDiscoveryInfoProvider = DiscoveryInfoProvider()
          # Create a discovery information provider with custom configuration
          myDiscoveryInfoProvider = DiscoveryInfoProvider(caPath=myCAPath, certPath=myCertPath, keyPath=myKeyPath, host=myHost, timeoutSec=myTimeoutSec)

        **Parameters**

        *caPath* - Path to read the root CA file.

        *certPath* - Path to read the certificate file.

        *keyPath* - Path to read the private key file.

        *host* - String that denotes the host name of the user-specific AWS IoT endpoint.

        *port* - Integer that denotes the port number to connect to. For discovery purpose, it is 8443 by default.

        *timeoutSec* - Time out configuration in seconds to consider a discovery request sending/response waiting has
        been timed out.

        **Returns**

        AWSIoTPythonSDK.core.greengrass.discovery.providers.DiscoveryInfoProvider object

        """
        self._ca_path = caPath
        self._cert_path = certPath
        self._key_path = keyPath
        self._host = host
        self._port = port
        self._timeout_sec = timeoutSec
        self._expected_exception_map = {
            self.HTTP_SC_400 : DiscoveryInvalidRequestException(),
            self.HTTP_SC_401 : DiscoveryUnauthorizedException(),
            self.HTTP_SC_404 : DiscoveryDataNotFoundException(),
            self.HTTP_SC_429 : DiscoveryThrottlingException()
        }

    def configureEndpoint(self, host, port=8443):
        """

        **Description**

        Used to configure the host address and port number for the discovery request to hit. Should be called before
        the discovery request happens.

        **Syntax**

        .. code:: python

          # Using default port configuration, 8443
          myDiscoveryInfoProvider.configureEndpoint(host="prefix.iot.us-east-1.amazonaws.com")
          # Customize port configuration
          myDiscoveryInfoProvider.configureEndpoint(host="prefix.iot.us-east-1.amazonaws.com", port=8888)

        **Parameters**

        *host* - String that denotes the host name of the user-specific AWS IoT endpoint.

        *port* - Integer that denotes the port number to connect to. For discovery purpose, it is 8443 by default.

        **Returns**

        None

        """
        pass

    def configureCredentials(self, caPath, certPath, keyPath):
        """

        **Description**

        Used to configure the credentials for discovery request. Should be called before the discovery request happens.

        **Syntax**

        .. code:: python

          myDiscoveryInfoProvider.configureCredentials("my/ca/path", "my/cert/path", "my/key/path")

        **Parameters**

        *caPath* - Path to read the root CA file.

        *certPath* - Path to read the certificate file.

        *keyPath* - Path to read the private key file.

        **Returns**

        None

        """
        pass

    def configureTimeout(self, timeoutSec):
        """

        **Description**

        Used to configure the time out in seconds for discovery request sending/response waiting. Should be called before
        the discovery request happens.

        **Syntax**

        .. code:: python

          # Configure the time out for discovery to be 10 seconds
          myDiscoveryInfoProvider.configureTimeout(10)

        **Parameters**

        *timeoutSec* - Time out configuration in seconds to consider a discovery request sending/response waiting has
        been timed out.

        **Returns**

        None

        """
        pass

    def discover(self, thingName):
        """

        **Description**

        Perform the discovery request for the given Greengrass aware device thing name.

        **Syntax**

        .. code:: python

          myDiscoveryInfoProvider.discover(thingName="myGGAD")

        **Parameters**

        *thingName* - Greengrass aware device thing name.

        **Returns**

        :code:`AWSIoTPythonSDK.core.greengrass.discovery.models.DiscoveryInfo` object.

        """
        pass

    def _create_tcp_connection(self):
        pass

    def _create_ssl_connection(self, sock):
        pass

    def _tls_match_hostname(self, ssl_sock):
        pass

    def _host_matches_cert(self, host, cert_host):
        pass

    def _send_discovery_request(self, ssl_sock, thing_name):
        pass

    def _receive_discovery_response(self, ssl_sock):
        pass

    def _receive_until(self, ssl_sock, criteria_function, extra_data=None):
        pass

    def _convert_to_int_py3(self, input_char):
        pass

    def _got_enough_bytes(self, data):
        pass

    def _got_two_crlfs(self, data):
        pass

    def _handle_discovery_response_header(self, rc, response):
        pass

    def _handle_discovery_response_body(self, rc, response):
        pass

    def _raise_on_timeout(self, rc):
        pass

    def _raise_if_not_200(self, status_code, response_body):  # response_body here is str in Py3
        pass
