# Copyright (c) 2012-2014 Roger Light <roger@atchoo.org>
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Eclipse Public License v1.0
# and Eclipse Distribution License v1.0 which accompany this distribution.
#
# The Eclipse Public License is available at
#    http://www.eclipse.org/legal/epl-v10.html
# and the Eclipse Distribution License is available at
#   http://www.eclipse.org/org/documents/edl-v10.php.
#
# Contributors:
#    Roger Light - initial API and implementation

"""
This is an MQTT v3.1 client module. MQTT is a lightweight pub/sub messaging
protocol that is easy to implement and suitable for low powered devices.
"""
import errno
import platform
import random
import select
import socket
HAVE_SSL = True
try:
    import ssl
    cert_reqs = ssl.CERT_REQUIRED
    tls_version = ssl.PROTOCOL_TLSv1
except:
    HAVE_SSL = False
    cert_reqs = None
    tls_version = None
import struct
import sys
import threading
import time
HAVE_DNS = True
try:
    import dns.resolver
except ImportError:
    HAVE_DNS = False

if platform.system() == 'Windows':
    EAGAIN = errno.WSAEWOULDBLOCK
else:
    EAGAIN = errno.EAGAIN

from AWSIoTPythonSDK.core.protocol.connection.cores import ProgressiveBackOffCore
from AWSIoTPythonSDK.core.protocol.connection.cores import SecuredWebSocketCore
from AWSIoTPythonSDK.core.protocol.connection.alpn import SSLContextBuilder

MQTTv31 = 3
MQTTv311 = 4

if sys.version_info[0] < 3:
    PROTOCOL_NAMEv31 = "MQIsdp"
    PROTOCOL_NAMEv311 = "MQTT"
else:
    PROTOCOL_NAMEv31 = b"MQIsdp"
    PROTOCOL_NAMEv311 = b"MQTT"

PROTOCOL_VERSION = 3

# Message types
CONNECT = 0x10
CONNACK = 0x20
PUBLISH = 0x30
PUBACK = 0x40
PUBREC = 0x50
PUBREL = 0x60
PUBCOMP = 0x70
SUBSCRIBE = 0x80
SUBACK = 0x90
UNSUBSCRIBE = 0xA0
UNSUBACK = 0xB0
PINGREQ = 0xC0
PINGRESP = 0xD0
DISCONNECT = 0xE0

# Log levels
MQTT_LOG_INFO = 0x01
MQTT_LOG_NOTICE = 0x02
MQTT_LOG_WARNING = 0x04
MQTT_LOG_ERR = 0x08
MQTT_LOG_DEBUG = 0x10

# CONNACK codes
CONNACK_ACCEPTED = 0
CONNACK_REFUSED_PROTOCOL_VERSION = 1
CONNACK_REFUSED_IDENTIFIER_REJECTED = 2
CONNACK_REFUSED_SERVER_UNAVAILABLE = 3
CONNACK_REFUSED_BAD_USERNAME_PASSWORD = 4
CONNACK_REFUSED_NOT_AUTHORIZED = 5

# SUBACK codes
SUBACK_ERROR = 0x80

# Connection state
mqtt_cs_new = 0
mqtt_cs_connected = 1
mqtt_cs_disconnecting = 2
mqtt_cs_connect_async = 3

# Message state
mqtt_ms_invalid = 0
mqtt_ms_publish= 1
mqtt_ms_wait_for_puback = 2
mqtt_ms_wait_for_pubrec = 3
mqtt_ms_resend_pubrel = 4
mqtt_ms_wait_for_pubrel = 5
mqtt_ms_resend_pubcomp = 6
mqtt_ms_wait_for_pubcomp = 7
mqtt_ms_send_pubrec = 8
mqtt_ms_queued = 9

# Error values
MQTT_ERR_AGAIN = -1
MQTT_ERR_SUCCESS = 0
MQTT_ERR_NOMEM = 1
MQTT_ERR_PROTOCOL = 2
MQTT_ERR_INVAL = 3
MQTT_ERR_NO_CONN = 4
MQTT_ERR_CONN_REFUSED = 5
MQTT_ERR_NOT_FOUND = 6
MQTT_ERR_CONN_LOST = 7
MQTT_ERR_TLS = 8
MQTT_ERR_PAYLOAD_SIZE = 9
MQTT_ERR_NOT_SUPPORTED = 10
MQTT_ERR_AUTH = 11
MQTT_ERR_ACL_DENIED = 12
MQTT_ERR_UNKNOWN = 13
MQTT_ERR_ERRNO = 14

# MessageQueueing DropBehavior
MSG_QUEUEING_DROP_OLDEST = 0
MSG_QUEUEING_DROP_NEWEST = 1


if sys.version_info[0] < 3:
    sockpair_data = "0"
else:
    sockpair_data = b"0"

def error_string(mqtt_errno):
    """Return the error string associated with an mqtt error number."""
    pass


def connack_string(connack_code):
    """Return the string associated with a CONNACK result."""
    pass


def topic_matches_sub(sub, topic):
    """Check whether a topic matches a subscription.

    For example:

    foo/bar would match the subscription foo/# or +/bar
    non/matching would not match the subscription non/+/+
    """
    result = True
    multilevel_wildcard = False

    slen = len(sub)
    tlen = len(topic)

    if slen > 0 and tlen > 0:
        if (sub[0] == '$' and topic[0] != '$') or (topic[0] == '$' and sub[0] != '$'):
            return False

    spos = 0
    tpos = 0

    while spos < slen and tpos < tlen:
        if sub[spos] == topic[tpos]:
            if tpos == tlen-1:
                # Check for e.g. foo matching foo/#
                if spos == slen-3 and sub[spos+1] == '/' and sub[spos+2] == '#':
                    result = True
                    multilevel_wildcard = True
                    break

            spos += 1
            tpos += 1

            if tpos == tlen and spos == slen-1 and sub[spos] == '+':
                spos += 1
                result = True
                break
        else:
            if sub[spos] == '+':
                spos += 1
                while tpos < tlen and topic[tpos] != '/':
                    tpos += 1
                if tpos == tlen and spos == slen:
                    result = True
                    break

            elif sub[spos] == '#':
                multilevel_wildcard = True
                if spos+1 != slen:
                    result = False
                    break
                else:
                    result = True
                    break

            else:
                result = False
                break

    if not multilevel_wildcard and (tpos < tlen or spos < slen):
        result = False

    return result


def _socketpair_compat():
    """TCP/IP socketpair including Windows support"""
    pass


class MQTTMessage:
    """ This is a class that describes an incoming message. It is passed to the
    on_message callback as the message parameter.

    Members:

    topic : String. topic that the message was published on.
    payload : String/bytes the message payload.
    qos : Integer. The message Quality of Service 0, 1 or 2.
    retain : Boolean. If true, the message is a retained message and not fresh.
    mid : Integer. The message id.
    """
    def __init__(self):
        self.timestamp = 0
        self.state = mqtt_ms_invalid
        self.dup = False
        self.mid = 0
        self.topic = ""
        self.payload = None
        self.qos = 0
        self.retain = False


class Client(object):
    """MQTT version 3.1/3.1.1 client class.

    This is the main class for use communicating with an MQTT broker.

    General usage flow:

    * Use connect()/connect_async() to connect to a broker
    * Call loop() frequently to maintain network traffic flow with the broker
    * Or use loop_start() to set a thread running to call loop() for you.
    * Or use loop_forever() to handle calling loop() for you in a blocking
    * function.
    * Use subscribe() to subscribe to a topic and receive messages
    * Use publish() to send messages
    * Use disconnect() to disconnect from the broker

    Data returned from the broker is made available with the use of callback
    functions as described below.

    Callbacks
    =========

    A number of callback functions are available to receive data back from the
    broker. To use a callback, define a function and then assign it to the
    client:

    def on_connect(client, userdata, flags, rc):
        print("Connection returned " + str(rc))

    client.on_connect = on_connect

    All of the callbacks as described below have a "client" and an "userdata"
    argument. "client" is the Client instance that is calling the callback.
    "userdata" is user data of any type and can be set when creating a new client
    instance or with user_data_set(userdata).

    The callbacks:

    on_connect(client, userdata, flags, rc): called when the broker responds to our connection
      request.
      flags is a dict that contains response flags from the broker:
        flags['session present'] - this flag is useful for clients that are
            using clean session set to 0 only. If a client with clean
            session=0, that reconnects to a broker that it has previously
            connected to, this flag indicates whether the broker still has the
            session information for the client. If 1, the session still exists.
      The value of rc determines success or not:
        0: Connection successful
        1: Connection refused - incorrect protocol version
        2: Connection refused - invalid client identifier
        3: Connection refused - server unavailable
        4: Connection refused - bad username or password
        5: Connection refused - not authorised
        6-255: Currently unused.

    on_disconnect(client, userdata, rc): called when the client disconnects from the broker.
      The rc parameter indicates the disconnection state. If MQTT_ERR_SUCCESS
      (0), the callback was called in response to a disconnect() call. If any
      other value the disconnection was unexpected, such as might be caused by
      a network error.

    on_message(client, userdata, message): called when a message has been received on a
      topic that the client subscribes to. The message variable is a
      MQTTMessage that describes all of the message parameters.

    on_publish(client, userdata, mid): called when a message that was to be sent using the
      publish() call has completed transmission to the broker. For messages
      with QoS levels 1 and 2, this means that the appropriate handshakes have
      completed. For QoS 0, this simply means that the message has left the
      client. The mid variable matches the mid variable returned from the
      corresponding publish() call, to allow outgoing messages to be tracked.
      This callback is important because even if the publish() call returns
      success, it does not always mean that the message has been sent.

    on_subscribe(client, userdata, mid, granted_qos): called when the broker responds to a
      subscribe request. The mid variable matches the mid variable returned
      from the corresponding subscribe() call. The granted_qos variable is a
      list of integers that give the QoS level the broker has granted for each
      of the different subscription requests.

    on_unsubscribe(client, userdata, mid): called when the broker responds to an unsubscribe
      request. The mid variable matches the mid variable returned from the
      corresponding unsubscribe() call.

    on_log(client, userdata, level, buf): called when the client has log information. Define
      to allow debugging. The level variable gives the severity of the message
      and will be one of MQTT_LOG_INFO, MQTT_LOG_NOTICE, MQTT_LOG_WARNING,
      MQTT_LOG_ERR, and MQTT_LOG_DEBUG. The message itself is in buf.

    """
    def __init__(self, client_id="", clean_session=True, userdata=None, protocol=MQTTv31, useSecuredWebsocket=False):
        """client_id is the unique client id string used when connecting to the
        broker. If client_id is zero length or None, then one will be randomly
        generated. In this case, clean_session must be True. If this is not the
        case a ValueError will be raised.

        clean_session is a boolean that determines the client type. If True,
        the broker will remove all information about this client when it
        disconnects. If False, the client is a persistent client and
        subscription information and queued messages will be retained when the
        client disconnects.
        Note that a client will never discard its own outgoing messages on
        disconnect. Calling connect() or reconnect() will cause the messages to
        be resent.  Use reinitialise() to reset a client to its original state.

        userdata is user defined data of any type that is passed as the "userdata"
        parameter to callbacks. It may be updated at a later point with the
        user_data_set() function.

        The protocol argument allows explicit setting of the MQTT version to
        use for this client. Can be paho.mqtt.client.MQTTv311 (v3.1.1) or
        paho.mqtt.client.MQTTv31 (v3.1), with the default being v3.1. If the
        broker reports that the client connected with an invalid protocol
        version, the client will automatically attempt to reconnect using v3.1
        instead.

        useSecuredWebsocket is a boolean that determines whether the client uses
        MQTT over Websocket with sigV4 signing (True) or MQTT with plain TCP
        socket. If True, the client will try to find AWS_ACCESS_KEY_ID and
        AWS_SECRET_ACCESS_KEY in the system environment variables and start the
        sigV4 signing and Websocket handshake. Under this configuration, all
        outbound MQTT packets will be wrapped around with Websocket framework. All
        inbound MQTT packets will be automatically wss-decoded.
        """
        if not clean_session and (client_id == "" or client_id is None):
            raise ValueError('A client id must be provided if clean session is False.')

        self._protocol = protocol
        self._userdata = userdata
        self._sock = None
        self._sockpairR, self._sockpairW = _socketpair_compat()
        self._keepalive = 60
        self._message_retry = 20
        self._last_retry_check = 0
        self._clean_session = clean_session
        if client_id == "" or client_id is None:
            self._client_id = "paho/" + "".join(random.choice("0123456789ADCDEF") for x in range(23-5))
        else:
            self._client_id = client_id

        self._username = ""
        self._password = ""
        self._in_packet = {
            "command": 0,
            "have_remaining": 0,
            "remaining_count": [],
            "remaining_mult": 1,
            "remaining_length": 0,
            "packet": b"",
            "to_process": 0,
            "pos": 0}
        self._out_packet = []
        self._current_out_packet = None
        self._last_msg_in = time.time()
        self._last_msg_out = time.time()
        self._ping_t = 0
        self._last_mid = 0
        self._state = mqtt_cs_new
        self._max_inflight_messages = 20
        self._out_messages = []
        self._in_messages = []
        self._inflight_messages = 0
        self._will = False
        self._will_topic = ""
        self._will_payload = None
        self._will_qos = 0
        self._will_retain = False
        self.on_disconnect = None
        self.on_connect = None
        self.on_publish = None
        self.on_message = None
        self.on_message_filtered = []
        self.on_subscribe = None
        self.on_unsubscribe = None
        self.on_log = None
        self._host = ""
        self._port = 1883
        self._bind_address = ""
        self._socket_factory = None
        self._in_callback = False
        self._strict_protocol = False
        self._callback_mutex = threading.Lock()
        self._state_mutex = threading.Lock()
        self._out_packet_mutex = threading.Lock()
        self._current_out_packet_mutex = threading.Lock()
        self._msgtime_mutex = threading.Lock()
        self._out_message_mutex = threading.Lock()
        self._in_message_mutex = threading.Lock()
        self._mid_generate_mutex = threading.Lock()
        self._thread = None
        self._thread_terminate = False
        self._ssl = None
        self._tls_certfile = None
        self._tls_keyfile = None
        self._tls_ca_certs = None
        self._tls_cert_reqs = None
        self._tls_ciphers = None
        self._tls_version = tls_version
        self._tls_insecure = False
        self._useSecuredWebsocket = useSecuredWebsocket  # Do we enable secured websocket
        self._backoffCore = ProgressiveBackOffCore()  # Init the backoffCore using default configuration
        self._AWSAccessKeyIDCustomConfig = ""
        self._AWSSecretAccessKeyCustomConfig = ""
        self._AWSSessionTokenCustomConfig = ""
        self._alpn_protocols = None

    def __del__(self):
        # Closes socket in client destructor to avoid FD leak.
        self._reset_sockets()


    def setBackoffTiming(self, srcBaseReconnectTimeSecond, srcMaximumReconnectTimeSecond, srcMinimumConnectTimeSecond):
        """
        Make custom settings for backoff timing for reconnect logic
        srcBaseReconnectTimeSecond - The base reconnection time in seconds
        srcMaximumReconnectTimeSecond - The maximum reconnection time in seconds
        srcMinimumConnectTimeSecond - The minimum time in seconds that a connection must be maintained in order to be considered stable
        * Raise ValueError if input params are malformed
        """
        pass

    def configIAMCredentials(self, srcAWSAccessKeyID, srcAWSSecretAccessKey, srcAWSSessionToken):
        """
        Make custom settings for IAM credentials for websocket connection
        srcAWSAccessKeyID - AWS IAM access key
        srcAWSSecretAccessKey - AWS IAM secret key
        srcAWSSessionToken - AWS Session Token
        """
        pass

    def config_alpn_protocols(self, alpn_protocols):
        """
        Make custom settings for ALPN protocols
        :param alpn_protocols: Array of strings that specifies the alpn protocols to be used
        :return: None
        """
        pass

    # Closes socket in client destructor to avoid FD leak.
    def _reset_sockets(self):
        pass

    # Closes socket in client destructor to avoid FD leak.
    def reinitialise(self, client_id="", clean_session=True, userdata=None):
        pass

    def tls_set(self, ca_certs, certfile=None, keyfile=None, cert_reqs=cert_reqs, tls_version=tls_version, ciphers=None):
        """Configure network encryption and authentication options. Enables SSL/TLS support.

        ca_certs : a string path to the Certificate Authority certificate files
        that are to be treated as trusted by this client. If this is the only
        option given then the client will operate in a similar manner to a web
        browser. That is to say it will require the broker to have a
        certificate signed by the Certificate Authorities in ca_certs and will
        communicate using TLS v1, but will not attempt any form of
        authentication. This provides basic network encryption but may not be
        sufficient depending on how the broker is configured.

        certfile and keyfile are strings pointing to the PEM encoded client
        certificate and private keys respectively. If these arguments are not
        None then they will be used as client information for TLS based
        authentication.  Support for this feature is broker dependent. Note
        that if either of these files in encrypted and needs a password to
        decrypt it, Python will ask for the password at the command line. It is
        not currently possible to define a callback to provide the password.

        cert_reqs allows the certificate requirements that the client imposes
        on the broker to be changed. By default this is ssl.CERT_REQUIRED,
        which means that the broker must provide a certificate. See the ssl
        pydoc for more information on this parameter.

        tls_version allows the version of the SSL/TLS protocol used to be
        specified. By default TLS v1 is used. Previous versions (all versions
        beginning with SSL) are possible but not recommended due to possible
        security problems.

        ciphers is a string specifying which encryption ciphers are allowable
        for this connection, or None to use the defaults. See the ssl pydoc for
        more information.

        Must be called before connect() or connect_async()."""
        pass

    def tls_insecure_set(self, value):
        """Configure verification of the server hostname in the server certificate.

        If value is set to true, it is impossible to guarantee that the host
        you are connecting to is not impersonating your server. This can be
        useful in initial server testing, but makes it possible for a malicious
        third party to impersonate your server through DNS spoofing, for
        example.

        Do not use this function in a real system. Setting value to true means
        there is no point using encryption.

        Must be called before connect()."""
        pass

    def connect(self, host, port=1883, keepalive=60, bind_address=""):
        """Connect to a remote broker.

        host is the hostname or IP address of the remote broker.
        port is the network port of the server host to connect to. Defaults to
        1883. Note that the default port for MQTT over SSL/TLS is 8883 so if you
        are using tls_set() the port may need providing.
        keepalive: Maximum period in seconds between communications with the
        broker. If no other messages are being exchanged, this controls the
        rate at which the client will send ping messages to the broker.
        """
        pass

    def connect_srv(self, domain=None, keepalive=60, bind_address=""):
        """Connect to a remote broker.

        domain is the DNS domain to search for SRV records; if None,
        try to determine local domain name.
        keepalive and bind_address are as for connect()
        """
        pass

    def connect_async(self, host, port=1883, keepalive=60, bind_address=""):
        """Connect to a remote broker asynchronously. This is a non-blocking
        connect call that can be used with loop_start() to provide very quick
        start.

        host is the hostname or IP address of the remote broker.
        port is the network port of the server host to connect to. Defaults to
        1883. Note that the default port for MQTT over SSL/TLS is 8883 so if you
        are using tls_set() the port may need providing.
        keepalive: Maximum period in seconds between communications with the
        broker. If no other messages are being exchanged, this controls the
        rate at which the client will send ping messages to the broker.
        """
        pass

    def reconnect(self):
        """Reconnect the client after a disconnect. Can only be called after
        connect()/connect_async()."""
        pass

    def loop(self, timeout=1.0, max_packets=1):
        """Process network events.

        This function must be called regularly to ensure communication with the
        broker is carried out. It calls select() on the network socket to wait
        for network events. If incoming data is present it will then be
        processed. Outgoing commands, from e.g. publish(), are normally sent
        immediately that their function is called, but this is not always
        possible. loop() will also attempt to send any remaining outgoing
        messages, which also includes commands that are part of the flow for
        messages with QoS>0.

        timeout: The time in seconds to wait for incoming/outgoing network
          traffic before timing out and returning.
        max_packets: Not currently used.

        Returns MQTT_ERR_SUCCESS on success.
        Returns >0 on error.

        A ValueError will be raised if timeout < 0"""
        pass

    def publish(self, topic, payload=None, qos=0, retain=False):
        """Publish a message on a topic.

        This causes a message to be sent to the broker and subsequently from
        the broker to any clients subscribing to matching topics.

        topic: The topic that the message should be published on.
        payload: The actual message to send. If not given, or set to None a
        zero length message will be used. Passing an int or float will result
        in the payload being converted to a string representing that number. If
        you wish to send a true int/float, use struct.pack() to create the
        payload you require.
        qos: The quality of service level to use.
        retain: If set to true, the message will be set as the "last known
        good"/retained message for the topic.

        Returns a tuple (result, mid), where result is MQTT_ERR_SUCCESS to
        indicate success or MQTT_ERR_NO_CONN if the client is not currently
        connected.  mid is the message ID for the publish request. The mid
        value can be used to track the publish request by checking against the
        mid argument in the on_publish() callback if it is defined.

        A ValueError will be raised if topic is None, has zero length or is
        invalid (contains a wildcard), if qos is not one of 0, 1 or 2, or if
        the length of the payload is greater than 268435455 bytes."""
        pass

    def username_pw_set(self, username, password=None):
        """Set a username and optionally a password for broker authentication.

        Must be called before connect() to have any effect.
        Requires a broker that supports MQTT v3.1.

        username: The username to authenticate with. Need have no relationship to the client id.
                  [MQTT-3.1.3-11].
                  Set to None to reset client back to not using username/password for broker authentication.
        password: The password to authenticate with. Optional, set to None if not required.
        """
        pass

    def socket_factory_set(self, socket_factory):
        """Set a socket factory to custom configure a different socket type for
        mqtt connection.
        Must be called before connect() to have any effect.
        socket_factory: create_connection function which creates a socket to user's specification
        """
        pass
        
    def disconnect(self):
        """Disconnect a connected client from the broker."""
        pass

    def subscribe(self, topic, qos=0):
        """Subscribe the client to one or more topics.

        This function may be called in three different ways:

        Simple string and integer
        -------------------------
        e.g. subscribe("my/topic", 2)

        topic: A string specifying the subscription topic to subscribe to.
        qos: The desired quality of service level for the subscription.
             Defaults to 0.

        String and integer tuple
        ------------------------
        e.g. subscribe(("my/topic", 1))

        topic: A tuple of (topic, qos). Both topic and qos must be present in
               the tuple.
        qos: Not used.

        List of string and integer tuples
        ------------------------
        e.g. subscribe([("my/topic", 0), ("another/topic", 2)])

        This allows multiple topic subscriptions in a single SUBSCRIPTION
        command, which is more efficient than using multiple calls to
        subscribe().

        topic: A list of tuple of format (topic, qos). Both topic and qos must
               be present in all of the tuples.
        qos: Not used.

        The function returns a tuple (result, mid), where result is
        MQTT_ERR_SUCCESS to indicate success or (MQTT_ERR_NO_CONN, None) if the
        client is not currently connected.  mid is the message ID for the
        subscribe request. The mid value can be used to track the subscribe
        request by checking against the mid argument in the on_subscribe()
        callback if it is defined.

        Raises a ValueError if qos is not 0, 1 or 2, or if topic is None or has
        zero string length, or if topic is not a string, tuple or list.
        """
        pass

    def unsubscribe(self, topic):
        """Unsubscribe the client from one or more topics.

        topic: A single string, or list of strings that are the subscription
               topics to unsubscribe from.

        Returns a tuple (result, mid), where result is MQTT_ERR_SUCCESS
        to indicate success or (MQTT_ERR_NO_CONN, None) if the client is not
        currently connected.
        mid is the message ID for the unsubscribe request. The mid value can be
        used to track the unsubscribe request by checking against the mid
        argument in the on_unsubscribe() callback if it is defined.

        Raises a ValueError if topic is None or has zero string length, or is
        not a string or list.
        """
        pass

    def loop_read(self, max_packets=1):
        """Process read network events. Use in place of calling loop() if you
        wish to handle your client reads as part of your own application.

        Use socket() to obtain the client socket to call select() or equivalent
        on.

        Do not use if you are using the threaded interface loop_start()."""
        pass

    def loop_write(self, max_packets=1):
        """Process read network events. Use in place of calling loop() if you
        wish to handle your client reads as part of your own application.

        Use socket() to obtain the client socket to call select() or equivalent
        on.

        Use want_write() to determine if there is data waiting to be written.

        Do not use if you are using the threaded interface loop_start()."""
        pass

    def want_write(self):
        """Call to determine if there is network data waiting to be written.
        Useful if you are calling select() yourself rather than using loop().
        """
        pass

    def loop_misc(self):
        """Process miscellaneous network events. Use in place of calling loop() if you
        wish to call select() or equivalent on.

        Do not use if you are using the threaded interface loop_start()."""
        pass

    def max_inflight_messages_set(self, inflight):
        """Set the maximum number of messages with QoS>0 that can be part way
        through their network flow at once. Defaults to 20."""
        pass

    def message_retry_set(self, retry):
        """Set the timeout in seconds before a message with QoS>0 is retried.
        20 seconds by default."""
        pass

    def user_data_set(self, userdata):
        """Set the user data variable passed to callbacks. May be any data type."""
        pass

    def will_set(self, topic, payload=None, qos=0, retain=False):
        """Set a Will to be sent by the broker in case the client disconnects unexpectedly.

        This must be called before connect() to have any effect.

        topic: The topic that the will message should be published on.
        payload: The message to send as a will. If not given, or set to None a
        zero length message will be used as the will. Passing an int or float
        will result in the payload being converted to a string representing
        that number. If you wish to send a true int/float, use struct.pack() to
        create the payload you require.
        qos: The quality of service level to use for the will.
        retain: If set to true, the will message will be set as the "last known
        good"/retained message for the topic.

        Raises a ValueError if qos is not 0, 1 or 2, or if topic is None or has
        zero string length.
        """
        pass

    def will_clear(self):
        """ Removes a will that was previously configured with will_set().

        Must be called before connect() to have any effect."""
        pass

    def socket(self):
        """Return the socket or ssl object for this client."""
        pass

    def loop_forever(self, timeout=1.0, max_packets=1, retry_first_connection=False):
        """This function call loop() for you in an infinite blocking loop. It
        is useful for the case where you only want to run the MQTT client loop
        in your program.

        loop_forever() will handle reconnecting for you. If you call
        disconnect() in a callback it will return.


        timeout: The time in seconds to wait for incoming/outgoing network
          traffic before timing out and returning.
        max_packets: Not currently used.
        retry_first_connection: Should the first connection attempt be retried on failure.

        Raises socket.error on first connection failures unless retry_first_connection=True
        """
        pass

    def loop_start(self):
        """This is part of the threaded client interface. Call this once to
        start a new thread to process network traffic. This provides an
        alternative to repeatedly calling loop() yourself.
        """
        pass

    def loop_stop(self, force=False):
        """This is part of the threaded client interface. Call this once to
        stop the network thread previously created with loop_start(). This call
        will block until the network thread finishes.

        The force parameter is currently ignored.
        """
        pass

    def message_callback_add(self, sub, callback):
        """Register a message callback for a specific topic.
        Messages that match 'sub' will be passed to 'callback'. Any
        non-matching messages will be passed to the default on_message
        callback.
        
        Call multiple times with different 'sub' to define multiple topic
        specific callbacks.
        
        Topic specific callbacks may be removed with
        message_callback_remove()."""
        pass

    def message_callback_remove(self, sub):
        """Remove a message callback previously registered with
        message_callback_add()."""
        pass

    # ============================================================
    # Private functions
    # ============================================================

    def _loop_rc_handle(self, rc):
        pass

    def _packet_read(self):
        # This gets called if pselect() indicates that there is network data
        # available - ie. at least one byte.  What we do depends on what data we
        # already have.
        # If we've not got a command, attempt to read one and save it. This should
        # always work because it's only a single byte.
        # Then try to read the remaining length. This may fail because it is may
        # be more than one byte - will need to save data pending next read if it
        # does fail.
        # Then try to read the remaining payload, where 'payload' here means the
        # combined variable header and actual payload. This is the most likely to
        # fail due to longer length, so save current data and current position.
        # After all data is read, send to _mqtt_handle_packet() to deal with.
        # Finally, free the memory and reset everything to starting conditions.
        pass

    def _packet_write(self):
        pass

    def _easy_log(self, level, buf):
        pass

    def _check_keepalive(self):
        # Fix for keepalive=0 causing an infinite disconnect/reconnect loop.
        pass

    def _mid_generate(self):
        # Make sure mid generation that was thread-safe.
        pass

    def _topic_wildcard_len_check(self, topic):
        # Search for + or # in a topic. Return MQTT_ERR_INVAL if found.
         # Also returns MQTT_ERR_INVAL if the topic string is too long.
         # Returns MQTT_ERR_SUCCESS if everything is fine.
        pass

    def _send_pingreq(self):
        pass

    def _send_pingresp(self):
        pass

    def _send_puback(self, mid):
        pass

    def _send_pubcomp(self, mid):
        pass

    def _pack_remaining_length(self, packet, remaining_length):
        pass

    def _pack_str16(self, packet, data):
        pass

    def _send_publish(self, mid, topic, payload=None, qos=0, retain=False, dup=False):
        pass

    def _send_pubrec(self, mid):
        pass

    def _send_pubrel(self, mid, dup=False):
        pass

    def _send_command_with_mid(self, command, mid, dup):
        # For PUBACK, PUBCOMP, PUBREC, and PUBREL
        pass

    def _send_simple_command(self, command):
        # For DISCONNECT, PINGREQ and PINGRESP
        pass

    def _send_connect(self, keepalive, clean_session):
        pass

    def _send_disconnect(self):
        pass

    def _send_subscribe(self, dup, topics):
        pass

    def _send_unsubscribe(self, dup, topics):
        pass

    def _message_retry_check_actual(self, messages, mutex):
        pass

    def _message_retry_check(self):
        pass

    def _messages_reconnect_reset_out(self):
        pass

    def _messages_reconnect_reset_in(self):
        pass

    def _messages_reconnect_reset(self):
        pass

    def _packet_queue(self, command, packet, mid, qos):
        pass

    def _packet_handle(self):
        pass

    def _handle_pingreq(self):
        pass

    def _handle_pingresp(self):
        pass

    def _handle_connack(self):
        pass

    def _handle_suback(self):
        pass

    def _handle_publish(self):
        pass

    def _handle_pubrel(self):
        pass

    def _update_inflight(self):
        # Dont lock message_mutex here
        pass

    def _handle_pubrec(self):
        pass

    def _handle_unsuback(self):
        pass

    def _handle_pubackcomp(self, cmd):
        pass

    def _handle_on_message(self, message):
        pass

    def _thread_main(self):
        pass

    def _host_matches_cert(self, host, cert_host):
        pass

    def _tls_match_hostname(self):
        pass


# Compatibility class for easy porting from mosquitto.py. 
class Mosquitto(Client):
    def __init__(self, client_id="", clean_session=True, userdata=None):
        super(Mosquitto, self).__init__(client_id, clean_session, userdata)
