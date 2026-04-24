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


try:
    import ssl
except:
    ssl = None


class SSLContextBuilder(object):

    def __init__(self):
        self.check_supportability()
        self._ssl_context = ssl.create_default_context()

    def check_supportability(self):
        pass

    def with_ca_certs(self, ca_certs):
        pass

    def with_cert_key_pair(self, cert_file, key_file):
        pass

    def with_cert_reqs(self, cert_reqs):
        pass

    def with_check_hostname(self, check_hostname):
        pass

    def with_ciphers(self, ciphers):
        pass

    def with_alpn_protocols(self, alpn_protocols):
        pass

    def build(self):
        pass
