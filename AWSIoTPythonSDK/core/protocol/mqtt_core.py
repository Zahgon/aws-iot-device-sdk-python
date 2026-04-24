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

import AWSIoTPythonSDK
from AWSIoTPythonSDK.core.protocol.internal.clients import InternalAsyncMqttClient
from AWSIoTPythonSDK.core.protocol.internal.clients import ClientStatusContainer
from AWSIoTPythonSDK.core.protocol.internal.clients import ClientStatus
from AWSIoTPythonSDK.core.protocol.internal.workers import EventProducer
from AWSIoTPythonSDK.core.protocol.internal.workers import EventConsumer
from AWSIoTPythonSDK.core.protocol.internal.workers import SubscriptionManager
from AWSIoTPythonSDK.core.protocol.internal.workers import OfflineRequestsManager
from AWSIoTPythonSDK.core.protocol.internal.requests import RequestTypes
from AWSIoTPythonSDK.core.protocol.internal.requests import QueueableRequest
from AWSIoTPythonSDK.core.protocol.internal.defaults import DEFAULT_CONNECT_DISCONNECT_TIMEOUT_SEC
from AWSIoTPythonSDK.core.protocol.internal.defaults import DEFAULT_OPERATION_TIMEOUT_SEC
from AWSIoTPythonSDK.core.protocol.internal.defaults import METRICS_PREFIX
from AWSIoTPythonSDK.core.protocol.internal.defaults import ALPN_PROTCOLS
from AWSIoTPythonSDK.core.protocol.internal.events import FixedEventMids
from AWSIoTPythonSDK.core.protocol.paho.client import MQTT_ERR_SUCCESS, SUBACK_ERROR
from AWSIoTPythonSDK.exception.AWSIoTExceptions import connectError
from AWSIoTPythonSDK.exception.AWSIoTExceptions import connectTimeoutException
from AWSIoTPythonSDK.exception.AWSIoTExceptions import disconnectError
from AWSIoTPythonSDK.exception.AWSIoTExceptions import disconnectTimeoutException
from AWSIoTPythonSDK.exception.AWSIoTExceptions import publishError
from AWSIoTPythonSDK.exception.AWSIoTExceptions import publishTimeoutException
from AWSIoTPythonSDK.exception.AWSIoTExceptions import publishQueueFullException
from AWSIoTPythonSDK.exception.AWSIoTExceptions import publishQueueDisabledException
from AWSIoTPythonSDK.exception.AWSIoTExceptions import subscribeQueueFullException
from AWSIoTPythonSDK.exception.AWSIoTExceptions import subscribeQueueDisabledException
from AWSIoTPythonSDK.exception.AWSIoTExceptions import unsubscribeQueueFullException
from AWSIoTPythonSDK.exception.AWSIoTExceptions import unsubscribeQueueDisabledException
from AWSIoTPythonSDK.exception.AWSIoTExceptions import subscribeError, subackError
from AWSIoTPythonSDK.exception.AWSIoTExceptions import subscribeTimeoutException
from AWSIoTPythonSDK.exception.AWSIoTExceptions import unsubscribeError
from AWSIoTPythonSDK.exception.AWSIoTExceptions import unsubscribeTimeoutException
from AWSIoTPythonSDK.core.protocol.internal.queues import AppendResults
from AWSIoTPythonSDK.core.util.enums import DropBehaviorTypes
from AWSIoTPythonSDK.core.protocol.paho.client import MQTTv31
from threading import Condition
from threading import Event
import logging
import sys
if sys.version_info[0] < 3:
    from Queue import Queue
else:
    from queue import Queue


class SubackPacket(object):
    def __init__(self):
        self.event = Event()
        self.data = None


class MqttCore(object):

    _logger = logging.getLogger(__name__)

    def __init__(self, client_id, clean_session, protocol, use_wss):
        self._use_wss = use_wss
        self._username = ""
        self._password = None
        self._enable_metrics_collection = True
        self._event_queue = Queue()
        self._event_cv = Condition()
        self._event_producer = EventProducer(self._event_cv, self._event_queue)
        self._client_status = ClientStatusContainer()
        self._internal_async_client = InternalAsyncMqttClient(client_id, clean_session, protocol, use_wss)
        self._subscription_manager = SubscriptionManager()
        self._offline_requests_manager = OfflineRequestsManager(-1, DropBehaviorTypes.DROP_NEWEST)  # Infinite queue
        self._event_consumer = EventConsumer(self._event_cv,
                                             self._event_queue,
                                             self._internal_async_client,
                                             self._subscription_manager,
                                             self._offline_requests_manager,
                                             self._client_status)
        self._connect_disconnect_timeout_sec = DEFAULT_CONNECT_DISCONNECT_TIMEOUT_SEC
        self._operation_timeout_sec = DEFAULT_OPERATION_TIMEOUT_SEC
        self._init_offline_request_exceptions()
        self._init_workers()
        self._logger.info("MqttCore initialized")
        self._logger.info("Client id: %s" % client_id)
        self._logger.info("Protocol version: %s" % ("MQTTv3.1" if protocol == MQTTv31 else "MQTTv3.1.1"))
        self._logger.info("Authentication type: %s" % ("SigV4 WebSocket" if use_wss else "TLSv1.2 certificate based Mutual Auth."))

    def _init_offline_request_exceptions(self):
        pass

    def _init_workers(self):
        pass

    def _start_workers(self):
        pass

    def use_wss(self):
        pass

    # Used for general message event reception
    def on_message(self, message):
        pass

    # Used for general online event notification
    def on_online(self):
        pass

    # Used for general offline event notification
    def on_offline(self):
        pass

    def configure_cert_credentials(self, cert_credentials_provider, ciphers_provider):
        pass

    def configure_iam_credentials(self, iam_credentials_provider):
        pass

    def configure_endpoint(self, endpoint_provider):
        pass

    def configure_connect_disconnect_timeout_sec(self, connect_disconnect_timeout_sec):
        pass

    def configure_operation_timeout_sec(self, operation_timeout_sec):
        pass

    def configure_reconnect_back_off(self, base_reconnect_quiet_sec, max_reconnect_quiet_sec, stable_connection_sec):
        pass

    def configure_alpn_protocols(self):
        pass

    def configure_last_will(self, topic, payload, qos, retain=False):
        pass

    def clear_last_will(self):
        pass

    def configure_username_password(self, username, password=None):
        pass

    def configure_socket_factory(self, socket_factory):
        pass
        
    def enable_metrics_collection(self):
        pass

    def disable_metrics_collection(self):
        pass

    def configure_offline_requests_queue(self, max_size, drop_behavior):
        pass

    def configure_draining_interval_sec(self, draining_interval_sec):
        pass

    def connect(self, keep_alive_sec):
        pass

    def connect_async(self, keep_alive_sec, ack_callback=None):
        pass

    def _load_callbacks(self):
        pass

    def _load_username_password(self):
        pass

    def disconnect(self):
        pass

    def disconnect_async(self, ack_callback=None):
        pass

    def publish(self, topic, payload, qos, retain=False):
        pass

    def publish_async(self, topic, payload, qos, retain=False, ack_callback=None):
        pass

    def _publish_async(self, topic, payload, qos, retain=False, ack_callback=None):
        pass

    def subscribe(self, topic, qos, message_callback=None):
        pass

    def subscribe_async(self, topic, qos, ack_callback=None, message_callback=None):
        pass

    def _subscribe_async(self, topic, qos, ack_callback=None, message_callback=None):
        pass

    def unsubscribe(self, topic):
        pass

    def unsubscribe_async(self, topic, ack_callback=None):
        pass

    def _unsubscribe_async(self, topic, ack_callback=None):
        pass

    def _create_blocking_ack_callback(self, event):
        pass

    def _create_blocking_suback_callback(self, ack: SubackPacket):
        pass

    def _handle_offline_request(self, type, data):
        pass
