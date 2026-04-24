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

import time
import logging
from threading import Thread
from threading import Event
from AWSIoTPythonSDK.core.protocol.internal.events import EventTypes
from AWSIoTPythonSDK.core.protocol.internal.events import FixedEventMids
from AWSIoTPythonSDK.core.protocol.internal.clients import ClientStatus
from AWSIoTPythonSDK.core.protocol.internal.queues import OfflineRequestQueue
from AWSIoTPythonSDK.core.protocol.internal.requests import RequestTypes
from AWSIoTPythonSDK.core.protocol.paho.client import topic_matches_sub
from AWSIoTPythonSDK.core.protocol.internal.defaults import DEFAULT_DRAINING_INTERNAL_SEC


class EventProducer(object):

    _logger = logging.getLogger(__name__)

    def __init__(self, cv, event_queue):
        self._cv = cv
        self._event_queue = event_queue

    def on_connect(self, client, user_data, flags, rc):
        pass

    def on_disconnect(self, client, user_data, rc):
        pass

    def on_publish(self, client, user_data, mid):
        pass

    def on_subscribe(self, client, user_data, mid, granted_qos):
        pass

    def on_unsubscribe(self, client, user_data, mid):
        pass

    def on_message(self, client, user_data, message):
        pass

    def _add_to_queue(self, mid, event_type, data):
        pass


class EventConsumer(object):

    MAX_DISPATCH_INTERNAL_SEC = 0.01
    _logger = logging.getLogger(__name__)

    def __init__(self, cv, event_queue, internal_async_client,
                 subscription_manager, offline_requests_manager, client_status):
        self._cv = cv
        self._event_queue = event_queue
        self._internal_async_client = internal_async_client
        self._subscription_manager = subscription_manager
        self._offline_requests_manager = offline_requests_manager
        self._client_status = client_status
        self._is_running = False
        self._draining_interval_sec = DEFAULT_DRAINING_INTERNAL_SEC
        self._dispatch_methods = {
            EventTypes.CONNACK : self._dispatch_connack,
            EventTypes.DISCONNECT : self._dispatch_disconnect,
            EventTypes.PUBACK : self._dispatch_puback,
            EventTypes.SUBACK : self._dispatch_suback,
            EventTypes.UNSUBACK : self._dispatch_unsuback,
            EventTypes.MESSAGE : self._dispatch_message
        }
        self._offline_request_handlers = {
            RequestTypes.PUBLISH : self._handle_offline_publish,
            RequestTypes.SUBSCRIBE : self._handle_offline_subscribe,
            RequestTypes.UNSUBSCRIBE : self._handle_offline_unsubscribe
        }
        self._stopper = Event()

    def update_offline_requests_manager(self, offline_requests_manager):
        pass

    def update_draining_interval_sec(self, draining_interval_sec):
        pass

    def get_draining_interval_sec(self):
        pass

    def is_running(self):
        pass

    def start(self):
        pass

    def stop(self):
        pass

    def _clean_up(self):
        pass

    def wait_until_it_stops(self, timeout_sec):
        pass

    def is_fully_stopped(self):
        pass

    def _dispatch(self):
        pass

    def _dispatch_one(self):
        pass

    def _need_to_stop_dispatching(self, mid):
        pass

    def _dispatch_connack(self, mid, rc):
        pass

    def _need_recover(self):
        pass

    def _clean_up_debt(self):
        pass

    def _handle_resubscribe(self):
        pass

    def _handle_draining(self):
        pass

    def _has_user_disconnect_request(self):
        pass

    def _dispatch_disconnect(self, mid, rc):
        pass

    # For puback, suback and unsuback, ack callback invocation is handled in dispatch_one
    # Do nothing in the event dispatching itself
    def _dispatch_puback(self, mid, rc):
        pass

    def _dispatch_suback(self, mid, rc):
        pass

    def _dispatch_unsuback(self, mid, rc):
        pass

    def _dispatch_message(self, mid, message):
        pass

    def _handle_offline_publish(self, request):
        pass

    def _handle_offline_subscribe(self, request):
        pass

    def _handle_offline_unsubscribe(self, request):
        pass


class SubscriptionManager(object):

    _logger = logging.getLogger(__name__)

    def __init__(self):
        self._subscription_map = dict()

    def add_record(self, topic, qos, message_callback, ack_callback):
        pass

    def remove_record(self, topic):
        pass

    def list_records(self):
        pass


class OfflineRequestsManager(object):

    _logger = logging.getLogger(__name__)

    def __init__(self, max_size, drop_behavior):
        self._queue = OfflineRequestQueue(max_size, drop_behavior)

    def has_more(self):
        pass

    def add_one(self, request):
        pass

    def get_next(self):
        pass
