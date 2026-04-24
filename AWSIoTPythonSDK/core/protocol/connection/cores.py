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

# This class implements the progressive backoff logic for auto-reconnect.
# It manages the reconnect wait time for the current reconnect, controling
# when to increase it and when to reset it.


import re
import sys
import ssl
import errno
import struct
import socket
import base64
import time
import threading
import logging
import os
from datetime import datetime
import hashlib
import hmac
from AWSIoTPythonSDK.exception.AWSIoTExceptions import ClientError
from AWSIoTPythonSDK.exception.AWSIoTExceptions import wssNoKeyInEnvironmentError
from AWSIoTPythonSDK.exception.AWSIoTExceptions import wssHandShakeError
from AWSIoTPythonSDK.core.protocol.internal.defaults import DEFAULT_CONNECT_DISCONNECT_TIMEOUT_SEC
try:
    from urllib.parse import quote  # Python 3+
except ImportError:
    from urllib import quote
# INI config file handling
try:
    from configparser import ConfigParser  # Python 3+
    from configparser import NoOptionError
    from configparser import NoSectionError
except ImportError:
    from ConfigParser import ConfigParser
    from ConfigParser import NoOptionError
    from ConfigParser import NoSectionError


class ProgressiveBackOffCore:
    # Logger
    _logger = logging.getLogger(__name__)

    def __init__(self, srcBaseReconnectTimeSecond=1, srcMaximumReconnectTimeSecond=32, srcMinimumConnectTimeSecond=20):
        # The base reconnection time in seconds, default 1
        self._baseReconnectTimeSecond = srcBaseReconnectTimeSecond
        # The maximum reconnection time in seconds, default 32
        self._maximumReconnectTimeSecond = srcMaximumReconnectTimeSecond
        # The minimum time in milliseconds that a connection must be maintained in order to be considered stable
        # Default 20
        self._minimumConnectTimeSecond = srcMinimumConnectTimeSecond
        # Current backOff time in seconds, init to equal to 0
        self._currentBackoffTimeSecond = 1
        # Handler for timer
        self._resetBackoffTimer = None

    # For custom progressiveBackoff timing configuration
    def configTime(self, srcBaseReconnectTimeSecond, srcMaximumReconnectTimeSecond, srcMinimumConnectTimeSecond):
        pass

    # Block the reconnect logic for _currentBackoffTimeSecond
    # Update the currentBackoffTimeSecond for the next reconnect
    # Cancel the in-waiting timer for resetting backOff time
    # This should get called only when a disconnect/reconnect happens
    def backOff(self):
        pass

    # Start the timer for resetting _currentBackoffTimeSecond
    # Will be cancelled upon calling backOff
    def startStableConnectionTimer(self):
        pass

    def stopStableConnectionTimer(self):
        pass

    # Timer callback to reset _currentBackoffTimeSecond
    # If the connection is stable for longer than _minimumConnectTimeSecond,
    # reset the currentBackoffTimeSecond to _baseReconnectTimeSecond
    def _connectionStableThenResetBackoffTime(self):
        pass


class SigV4Core:

    _logger = logging.getLogger(__name__)

    def __init__(self):
        self._aws_access_key_id = ""
        self._aws_secret_access_key = ""
        self._aws_session_token = ""
        self._credentialConfigFilePath = "~/.aws/credentials"

    def setIAMCredentials(self, srcAWSAccessKeyID, srcAWSSecretAccessKey, srcAWSSessionToken):
        pass

    def _createAmazonDate(self):
        # Returned as a unicode string in Py3.x
        pass

    def _sign(self, key, message):
        # Returned as a utf-8 byte string in Py3.x
        pass

    def _getSignatureKey(self, key, dateStamp, regionName, serviceName):
        # Returned as a utf-8 byte string in Py3.x
        pass

    def _checkIAMCredentials(self):
        # Check custom config
        pass

    def _checkKeyInEnv(self):
        pass

    def _checkKeyInINIDefault(self, srcConfigParser, sectionName):
        pass

    def _checkKeyInFiles(self):
        pass

    def _checkKeyInCustomConfig(self):
        pass

    def createWebsocketEndpoint(self, host, port, region, method, awsServiceName, path):
        # Return the endpoint as unicode string in 3.x
        # Gather all the facts
        pass

    def _hasCredentialsNecessaryForWebsocket(self, allKeys):
        pass


# This is an internal class that buffers the incoming bytes into an
# internal buffer until it gets the full desired length of bytes.
# At that time, this bufferedReader will be reset.
# *Error handling:
# For retry errors (ssl.SSL_ERROR_WANT_READ, ssl.SSL_ERROR_WANT_WRITE, EAGAIN),
# leave them to the paho _packet_read for further handling (ignored and try
# again when data is available.
# For other errors, leave them to the paho _packet_read for error reporting.


class _BufferedReader:
    _sslSocket = None
    _internalBuffer = None
    _remainedLength = -1
    _bufferingInProgress = False

    def __init__(self, sslSocket):
        self._sslSocket = sslSocket
        self._internalBuffer = bytearray()
        self._bufferingInProgress = False

    def _reset(self):
        pass

    def read(self, numberOfBytesToBeBuffered):
        pass


# This is the internal class that sends requested data out chunk by chunk according
# to the availablity of the socket write operation. If the requested bytes of data
# (after encoding) needs to be sent out in separate socket write operations (most
# probably be interrupted by the error socket.error (errno = ssl.SSL_ERROR_WANT_WRITE).)
# , the write pointer is stored to ensure that the continued bytes will be sent next
# time this function gets called.
# *Error handling:
# For retry errors (ssl.SSL_ERROR_WANT_READ, ssl.SSL_ERROR_WANT_WRITE, EAGAIN),
# leave them to the paho _packet_read for further handling (ignored and try
# again when data is available.
# For other errors, leave them to the paho _packet_read for error reporting.


class _BufferedWriter:
    _sslSocket = None
    _internalBuffer = None
    _writingInProgress = False
    _requestedDataLength = -1

    def __init__(self, sslSocket):
        self._sslSocket = sslSocket
        self._internalBuffer = bytearray()
        self._writingInProgress = False
        self._requestedDataLength = -1

    def _reset(self):
        pass

    # Input data for this function needs to be an encoded wss frame
    # Always request for packet[pos=0:] (raw MQTT data)
    def write(self, encodedData, payloadLength):
        # encodedData should always be bytearray
        # Check if we have a frame that is partially sent
        pass


class SecuredWebSocketCore:
    # Websocket Constants
    _OP_CONTINUATION = 0x0
    _OP_TEXT = 0x1
    _OP_BINARY = 0x2
    _OP_CONNECTION_CLOSE = 0x8
    _OP_PING = 0x9
    _OP_PONG = 0xa
    # Websocket Connect Status
    _WebsocketConnectInit = -1
    _WebsocketDisconnected = 1

    _logger = logging.getLogger(__name__)

    def __init__(self, socket, hostAddress, portNumber, AWSAccessKeyID="", AWSSecretAccessKey="", AWSSessionToken=""):
        self._connectStatus = self._WebsocketConnectInit
        # Handlers
        self._sslSocket = socket
        self._sigV4Handler = self._createSigV4Core()
        self._sigV4Handler.setIAMCredentials(AWSAccessKeyID, AWSSecretAccessKey, AWSSessionToken)
        # Endpoint Info
        self._hostAddress = hostAddress
        self._portNumber = portNumber
        # Section Flags
        self._hasOpByte = False
        self._hasPayloadLengthFirst = False
        self._hasPayloadLengthExtended = False
        self._hasMaskKey = False
        self._hasPayload = False
        # Properties for current websocket frame
        self._isFIN = False
        self._RSVBits = None
        self._opCode = None
        self._needMaskKey = False
        self._payloadLengthBytesLength = 1
        self._payloadLength = 0
        self._maskKey = None
        self._payloadDataBuffer = bytearray()  # Once the whole wss connection is lost, there is no need to keep the buffered payload
        try:
            self._handShake(hostAddress, portNumber)
        except wssNoKeyInEnvironmentError:  # Handle SigV4 signing and websocket handshaking errors
            raise ValueError("No Access Key/KeyID Error")
        except wssHandShakeError:
            raise ValueError("Websocket Handshake Error")
        except ClientError as e:
            raise ValueError(e.message)
        # Now we have a socket with secured websocket...
        self._bufferedReader = _BufferedReader(self._sslSocket)
        self._bufferedWriter = _BufferedWriter(self._sslSocket)

    def _createSigV4Core(self):
        pass

    def _generateMaskKey(self):
        pass
        # os.urandom returns ascii str in 2.x, converted to bytearray
        # os.urandom returns bytes in 3.x, converted to bytearray

    def _reset(self):  # Reset the context for wss frame reception
        # Control info
        pass
        # Never reset the payloadData since we might have fragmented MQTT data from the pervious frame

    def _generateWSSKey(self):
        pass

    def _verifyWSSResponse(self, response, clientKey):
        # Check if it is a 101 response
        pass

    def _verifyWSSAcceptKey(self, srcAcceptKey, clientKey):
        pass

    def _handShake(self, hostAddress, portNumber):
        pass

    def _getTimeoutSec(self):
        pass

    # Used to create a single wss frame
    # Assume that the maximum length of a MQTT packet never exceeds the maximum length
    # for a wss frame. Therefore, the FIN bit for the encoded frame will always be 1.
    # Frames are encoded as BINARY frames.
    def _encodeFrame(self, rawPayload, opCode, masked=1):
        pass

    # Used for the wss client to close a wss connection
    # Create and send a masked wss closing frame
    def _closeWssConnection(self):
        # Frames sent from client to server must be masked
        pass

    # Used for the wss client to respond to a wss PING from server
    # Create and send a masked PONG frame
    def _sendPONG(self):
        # Frames sent from client to server must be masked
        pass

    # Override sslSocket read. Always read from the wss internal payload buffer, which
    # contains the masked MQTT packet. This read will decode ONE wss frame every time
    # and load in the payload for MQTT _packet_read. At any time, MQTT _packet_read
    # should be able to read a complete MQTT packet from the payload (buffered per wss
    # frame payload). If the MQTT packet is break into separate wss frames, different
    # chunks will be buffered in separate frames and MQTT _packet_read will not be able
    # to collect a complete MQTT packet to operate on until the necessary payload is
    # fully buffered.
    # If the requested number of bytes are not available, SSL_ERROR_WANT_READ will be
    # raised to trigger another call of _packet_read when the data is available again.
    def read(self, numberOfBytes):
        # Check if we have enough data for paho
        # _payloadDataBuffer will not be empty ony when the payload of a new wss frame
        # has been unmasked.
        pass

    def write(self, bytesToBeSent):
        # When there is a disconnection, select will report a TypeError which triggers the reconnect.
        # In reconnect, Paho will set the socket object (mocked by wss) to None, blocking other ops
        # before a connection is re-established.
        # This 'low-level' socket write op should always be able to write to plain socket.
        # Error reporting is performed by Python socket itself.
        # Wss closing frame handling is performed in the wss read.
        pass

    def close(self):
        pass

    def getpeercert(self):
        pass

    def getSSLSocket(self):
        pass
