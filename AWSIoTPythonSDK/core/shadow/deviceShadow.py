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

import json
import logging
import uuid
from threading import Timer, Lock, Thread


class _shadowRequestToken:

    URN_PREFIX_LENGTH = 9

    def getNextToken(self):
        pass


def _validateJSON(jsonString):
    pass


class _basicJSONParser:

    def setString(self, srcString):
        pass

    def regenerateString(self):
        pass

    def getAttributeValue(self, srcAttributeKey):
        pass

    def setAttributeValue(self, srcAttributeKey, srcAttributeValue):
        pass

    def validateJSON(self):
        pass


class deviceShadow:
    _logger = logging.getLogger(__name__)

    def __init__(self, srcShadowName, srcIsPersistentSubscribe, srcShadowManager):
        """

        The class that denotes a local/client-side device shadow instance.

        Users can perform shadow operations on this instance to retrieve and modify the 
        corresponding shadow JSON document in AWS IoT Cloud. The following shadow operations 
        are available:

        - Get
        
        - Update

        - Delete

        - Listen on delta

        - Cancel listening on delta

        This is returned from :code:`AWSIoTPythonSDK.MQTTLib.AWSIoTMQTTShadowClient.createShadowWithName` function call. 
        No need to call directly from user scripts.

        """
        if srcShadowName is None or srcIsPersistentSubscribe is None or srcShadowManager is None:
            raise TypeError("None type inputs detected.")
        self._shadowName = srcShadowName
        # Tool handler
        self._shadowManagerHandler = srcShadowManager
        self._basicJSONParserHandler = _basicJSONParser()
        self._tokenHandler = _shadowRequestToken()
        # Properties
        self._isPersistentSubscribe = srcIsPersistentSubscribe
        self._lastVersionInSync = -1  # -1 means not initialized
        self._isGetSubscribed = False
        self._isUpdateSubscribed = False
        self._isDeleteSubscribed = False
        self._shadowSubscribeCallbackTable = dict()
        self._shadowSubscribeCallbackTable["get"] = None
        self._shadowSubscribeCallbackTable["delete"] = None
        self._shadowSubscribeCallbackTable["update"] = None
        self._shadowSubscribeCallbackTable["delta"] = None
        self._shadowSubscribeStatusTable = dict()
        self._shadowSubscribeStatusTable["get"] = 0
        self._shadowSubscribeStatusTable["delete"] = 0
        self._shadowSubscribeStatusTable["update"] = 0
        self._tokenPool = dict()
        self._dataStructureLock = Lock()

    def _doNonPersistentUnsubscribe(self, currentAction):
        pass

    def generalCallback(self, client, userdata, message):
        # In Py3.x, message.payload comes in as a bytes(string)
        # json.loads needs a string input
        pass

    def _parseTopicAction(self, srcTopic):
        pass

    def _parseTopicType(self, srcTopic):
        pass

    def _parseTopicShadowName(self, srcTopic):
        pass

    def _timerHandler(self, srcActionName, srcToken):
        pass

    def shadowGet(self, srcCallback, srcTimeout):
        """
        **Description**

        Retrieve the device shadow JSON document from AWS IoT by publishing an empty JSON document to the 
        corresponding shadow topics. Shadow response topics will be subscribed to receive responses from 
        AWS IoT regarding the result of the get operation. Retrieved shadow JSON document will be available 
        in the registered callback. If no response is received within the provided timeout, a timeout 
        notification will be passed into the registered callback.

        **Syntax**

        .. code:: python

          # Retrieve the shadow JSON document from AWS IoT, with a timeout set to 5 seconds
          BotShadow.shadowGet(customCallback, 5)

        **Parameters**

        *srcCallback* - Function to be called when the response for this shadow request comes back. Should 
        be in form :code:`customCallback(payload, responseStatus, token)`, where :code:`payload` is the 
        JSON document returned, :code:`responseStatus` indicates whether the request has been accepted, 
        rejected or is a delta message, :code:`token` is the token used for tracing in this request.

        *srcTimeout* - Timeout to determine whether the request is invalid. When a request gets timeout, 
        a timeout notification will be generated and put into the registered callback to notify users.

        **Returns**

        The token used for tracing in this shadow request.

        """
        pass

    def shadowDelete(self, srcCallback, srcTimeout):
        """
        **Description**

        Delete the device shadow from AWS IoT by publishing an empty JSON document to the corresponding 
        shadow topics. Shadow response topics will be subscribed to receive responses from AWS IoT 
        regarding the result of the get operation. Responses will be available in the registered callback. 
        If no response is received within the provided timeout, a timeout notification will be passed into 
        the registered callback.

        **Syntax**

        .. code:: python

          # Delete the device shadow from AWS IoT, with a timeout set to 5 seconds
          BotShadow.shadowDelete(customCallback, 5)

        **Parameters**

        *srcCallback* - Function to be called when the response for this shadow request comes back. Should 
        be in form :code:`customCallback(payload, responseStatus, token)`, where :code:`payload` is the 
        JSON document returned, :code:`responseStatus` indicates whether the request has been accepted, 
        rejected or is a delta message, :code:`token` is the token used for tracing in this request.

        *srcTimeout* - Timeout to determine whether the request is invalid. When a request gets timeout, 
        a timeout notification will be generated and put into the registered callback to notify users.

        **Returns**

        The token used for tracing in this shadow request.

        """
        pass

    def shadowUpdate(self, srcJSONPayload, srcCallback, srcTimeout):
        """
        **Description**

        Update the device shadow JSON document string from AWS IoT by publishing the provided JSON 
        document to the corresponding shadow topics. Shadow response topics will be subscribed to 
        receive responses from AWS IoT regarding the result of the get operation. Response will be 
        available in the registered callback. If no response is received within the provided timeout, 
        a timeout notification will be passed into the registered callback.

        **Syntax**

        .. code:: python

          # Update the shadow JSON document from AWS IoT, with a timeout set to 5 seconds
          BotShadow.shadowUpdate(newShadowJSONDocumentString, customCallback, 5)

        **Parameters**

        *srcJSONPayload* - JSON document string used to update shadow JSON document in AWS IoT.

        *srcCallback* - Function to be called when the response for this shadow request comes back. Should 
        be in form :code:`customCallback(payload, responseStatus, token)`, where :code:`payload` is the 
        JSON document returned, :code:`responseStatus` indicates whether the request has been accepted, 
        rejected or is a delta message, :code:`token` is the token used for tracing in this request.

        *srcTimeout* - Timeout to determine whether the request is invalid. When a request gets timeout, 
        a timeout notification will be generated and put into the registered callback to notify users.

        **Returns**

        The token used for tracing in this shadow request.

        """
        pass

    def shadowRegisterDeltaCallback(self, srcCallback):
        """
        **Description**

        Listen on delta topics for this device shadow by subscribing to delta topics. Whenever there 
        is a difference between the desired and reported state, the registered callback will be called 
        and the delta payload will be available in the callback.

        **Syntax**

        .. code:: python

          # Listen on delta topics for BotShadow
          BotShadow.shadowRegisterDeltaCallback(customCallback)

        **Parameters**

        *srcCallback* - Function to be called when the response for this shadow request comes back. Should 
        be in form :code:`customCallback(payload, responseStatus, token)`, where :code:`payload` is the 
        JSON document returned, :code:`responseStatus` indicates whether the request has been accepted, 
        rejected or is a delta message, :code:`token` is the token used for tracing in this request.

        **Returns**

        None

        """
        pass

    def shadowUnregisterDeltaCallback(self):
        """
        **Description**

        Cancel listening on delta topics for this device shadow by unsubscribing to delta topics. There will 
        be no delta messages received after this API call even though there is a difference between the 
        desired and reported state.

        **Syntax**

        .. code:: python

          # Cancel listening on delta topics for BotShadow
          BotShadow.shadowUnregisterDeltaCallback()

        **Parameters**

        None

        **Returns**

        None

        """
        pass
