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

import ssl
import logging
from threading import Lock
from numbers import Number
import AWSIoTPythonSDK.core.protocol.paho.client as mqtt
from AWSIoTPythonSDK.core.protocol.paho.client import MQTT_ERR_SUCCESS
from AWSIoTPythonSDK.core.protocol.internal.events import FixedEventMids


class ClientStatus(object):

    IDLE = 0
    CONNECT = 1
    RESUBSCRIBE = 2
    DRAINING = 3
    STABLE = 4
    USER_DISCONNECT = 5
    ABNORMAL_DISCONNECT = 6


class ClientStatusContainer(object):

    def __init__(self):
        self._status = ClientStatus.IDLE

    def get_status(self):
        pass

    def set_status(self, status):
        pass


class InternalAsyncMqttClient(object):

    _logger = logging.getLogger(__name__)

    def __init__(self, client_id, clean_session, protocol, use_wss):
        self._paho_client = self._create_paho_client(client_id, clean_session, None, protocol, use_wss)
        self._use_wss = use_wss
        self._event_callback_map_lock = Lock()
        self._event_callback_map = dict()

    def _create_paho_client(self, client_id, clean_session, user_data, protocol, use_wss):
        pass

    #  TODO: Merge credentials providers configuration into one
    def set_cert_credentials_provider(self, cert_credentials_provider, ciphers_provider):
        # History issue from Yun SDK where AR9331 embedded Linux only have Python 2.7.3
        # pre-installed. In this version, TLSv1_2 is not even an option.
        # SSLv23 is a work-around which selects the highest TLS version between the client
        # and service. If user installs opensslv1.0.1+, this option will work fine for Mutual
        # Auth.
        # Note that we cannot force TLSv1.2 for Mutual Auth. in Python 2.7.3 and TLS support
        # in Python only starts from Python2.7.
        # See also: https://docs.python.org/2/library/ssl.html#ssl.PROTOCOL_SSLv23
        pass

    def set_iam_credentials_provider(self, iam_credentials_provider):
        pass

    def set_endpoint_provider(self, endpoint_provider):
        pass

    def configure_last_will(self, topic, payload, qos, retain=False):
        pass

    def configure_alpn_protocols(self, alpn_protocols):
        pass

    def clear_last_will(self):
        pass

    def set_username_password(self, username, password=None):
        pass

    def set_socket_factory(self, socket_factory):
        pass
        
    def configure_reconnect_back_off(self, base_reconnect_quiet_sec, max_reconnect_quiet_sec, stable_connection_sec):
        pass

    def connect(self, keep_alive_sec, ack_callback=None):
        pass

    def start_background_network_io(self):
        pass

    def stop_background_network_io(self):
        pass

    def disconnect(self, ack_callback=None):
        pass

    def _create_combined_on_connect_callback(self, ack_callback):
        pass

    def _create_combined_on_disconnect_callback(self, ack_callback):
        pass

    def _create_converted_on_message_callback(self):
        pass

    # For client online notification
    def on_online(self):
        pass

    # For client offline notification
    def on_offline(self):
        pass

    # For client message reception notification
    def on_message(self, message):
        pass

    def publish(self, topic, payload, qos, retain=False, ack_callback=None):
        pass

    def subscribe(self, topic, qos, ack_callback=None):
        pass

    def unsubscribe(self, topic, ack_callback=None):
        pass

    def register_internal_event_callbacks(self, on_connect, on_disconnect, on_publish, on_subscribe, on_unsubscribe, on_message):
        pass

    def unregister_internal_event_callbacks(self):
        pass

    def invoke_event_callback(self, mid, data=None):
        pass

    def remove_event_callback(self, mid):
        pass

    def clean_up_event_callbacks(self):
        pass

    def get_event_callback_map(self):
        pass
