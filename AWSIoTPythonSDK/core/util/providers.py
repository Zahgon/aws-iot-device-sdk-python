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


class CredentialsProvider(object):

    def __init__(self):
        self._ca_path = ""

    def set_ca_path(self, ca_path):
        pass

    def get_ca_path(self):
        pass


class CertificateCredentialsProvider(CredentialsProvider):

    def __init__(self):
        CredentialsProvider.__init__(self)
        self._cert_path = ""
        self._key_path = ""

    def set_cert_path(self,cert_path):
        pass

    def set_key_path(self, key_path):
        pass

    def get_cert_path(self):
        pass

    def get_key_path(self):
        pass


class IAMCredentialsProvider(CredentialsProvider):

    def __init__(self):
        CredentialsProvider.__init__(self)
        self._aws_access_key_id = ""
        self._aws_secret_access_key = ""
        self._aws_session_token = ""

    def set_access_key_id(self, access_key_id):
        pass

    def set_secret_access_key(self, secret_access_key):
        pass

    def set_session_token(self, session_token):
        pass

    def get_access_key_id(self):
        pass

    def get_secret_access_key(self):
        pass

    def get_session_token(self):
        pass


class EndpointProvider(object):

    def __init__(self):
        self._host = ""
        self._port = -1

    def set_host(self, host):
        pass

    def set_port(self, port):
        pass

    def get_host(self):
        pass

    def get_port(self):
        pass

class CiphersProvider(object):
    def __init__(self):
        self._ciphers = None

    def set_ciphers(self, ciphers=None):
        pass

    def get_ciphers(self):
        pass
