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


KEY_GROUP_LIST = "GGGroups"
KEY_GROUP_ID = "GGGroupId"
KEY_CORE_LIST = "Cores"
KEY_CORE_ARN = "thingArn"
KEY_CA_LIST = "CAs"
KEY_CONNECTIVITY_INFO_LIST = "Connectivity"
KEY_CONNECTIVITY_INFO_ID = "Id"
KEY_HOST_ADDRESS = "HostAddress"
KEY_PORT_NUMBER = "PortNumber"
KEY_METADATA = "Metadata"


class ConnectivityInfo(object):
    """

    Class the stores one set of the connectivity information.
    This is the data model for easy access to the discovery information from the discovery request function call. No
    need to call directly from user scripts.

    """

    def __init__(self, id, host, port, metadata):
        self._id = id
        self._host = host
        self._port = port
        self._metadata = metadata

    @property
    def id(self):
        """

        Connectivity Information Id.

        """
        pass

    @property
    def host(self):
        """

        Host address.

        """
        pass

    @property
    def port(self):
        """

        Port number.

        """
        pass

    @property
    def metadata(self):
        """

        Metadata string.

        """
        pass


class CoreConnectivityInfo(object):
    """

    Class that stores the connectivity information for a Greengrass core.
    This is the data model for easy access to the discovery information from the discovery request function call. No
    need to call directly from user scripts.

    """

    def __init__(self, coreThingArn, groupId):
        self._core_thing_arn = coreThingArn
        self._group_id = groupId
        self._connectivity_info_dict = dict()

    @property
    def coreThingArn(self):
        """

        Thing arn for this Greengrass core.

        """
        pass

    @property
    def groupId(self):
        """

        Greengrass group id that this Greengrass core belongs to.

        """
        pass

    @property
    def connectivityInfoList(self):
        """

        The list of connectivity information that this Greengrass core has.

        """
        pass

    def getConnectivityInfo(self, id):
        """

        **Description**

        Used for quickly accessing a certain set of connectivity information by id.

        **Syntax**

        .. code:: python

          myCoreConnectivityInfo.getConnectivityInfo("CoolId")

        **Parameters**

        *id* - The id for the desired connectivity information.

        **Return**

        :code:`AWSIoTPythonSDK.core.greengrass.discovery.models.ConnectivityInfo` object.

        """
        pass

    def appendConnectivityInfo(self, connectivityInfo):
        """

        **Description**

        Used for adding a new set of connectivity information to the list for this Greengrass core. This is used by the
        SDK internally. No need to call directly from user scripts.

        **Syntax**

        .. code:: python

          myCoreConnectivityInfo.appendConnectivityInfo(newInfo)

        **Parameters**

        *connectivityInfo* - :code:`AWSIoTPythonSDK.core.greengrass.discovery.models.ConnectivityInfo` object.

        **Returns**

        None

        """
        pass


class GroupConnectivityInfo(object):
    """

    Class that stores the connectivity information for a specific Greengrass group.
    This is the data model for easy access to the discovery information from the discovery request function call. No
    need to call directly from user scripts.

    """
    def __init__(self, groupId):
        self._group_id = groupId
        self._core_connectivity_info_dict = dict()
        self._ca_list = list()

    @property
    def groupId(self):
        """

        Id for this Greengrass group.

        """
        pass

    @property
    def coreConnectivityInfoList(self):
        """

        A list of Greengrass cores
        (:code:`AWSIoTPythonSDK.core.greengrass.discovery.models.CoreConnectivityInfo` object) that belong to this
        Greengrass group.

        """
        pass

    @property
    def caList(self):
        """

        A list of CA content strings for this Greengrass group.

        """
        pass

    def getCoreConnectivityInfo(self, coreThingArn):
        """

        **Description**

        Used to retrieve the corresponding :code:`AWSIoTPythonSDK.core.greengrass.discovery.models.CoreConnectivityInfo`
        object by core thing arn.

        **Syntax**

        .. code:: python

          myGroupConnectivityInfo.getCoreConnectivityInfo("YourOwnArnString")

        **Parameters**

        coreThingArn - Thing arn for the desired Greengrass core.

        **Returns**

        :code:`AWSIoTPythonSDK.core.greengrass.discovery.CoreConnectivityInfo` object.

        """
        pass

    def appendCoreConnectivityInfo(self, coreConnectivityInfo):
        """

        **Description**

        Used to append new core connectivity information to this group connectivity information. This is used by the
        SDK internally. No need to call directly from user scripts.

        **Syntax**

        .. code:: python

          myGroupConnectivityInfo.appendCoreConnectivityInfo(newCoreConnectivityInfo)

        **Parameters**

        *coreConnectivityInfo* - :code:`AWSIoTPythonSDK.core.greengrass.discovery.models.CoreConnectivityInfo` object.

        **Returns**

        None

        """
        pass

    def appendCa(self, ca):
        """

        **Description**

        Used to append new CA content string to this group connectivity information. This is used by the SDK internally.
        No need to call directly from user scripts.

        **Syntax**

        .. code:: python

          myGroupConnectivityInfo.appendCa("CaContentString")

        **Parameters**

        *ca* - Group CA content string.

        **Returns**

        None

        """
        pass


class DiscoveryInfo(object):
    """

    Class that stores the discovery information coming back from the discovery request.
    This is the data model for easy access to the discovery information from the discovery request function call. No
    need to call directly from user scripts.

    """
    def __init__(self, rawJson):
        self._raw_json = rawJson

    @property
    def rawJson(self):
        """

        JSON response string that contains the discovery information. This is reserved in case users want to do
        some process by themselves.

        """
        pass

    def getAllCores(self):
        """

        **Description**

        Used to retrieve the list of :code:`AWSIoTPythonSDK.core.greengrass.discovery.models.CoreConnectivityInfo`
        object for this discovery information. The retrieved cores could be from different Greengrass groups. This is
        designed for uses who want to iterate through all available cores at the same time, regardless of which group
        those cores are in.

        **Syntax**

        .. code:: python

          myDiscoveryInfo.getAllCores()

        **Parameters**

        None

        **Returns**

        List of :code:`AWSIoTPythonSDK.core.greengrass.discovery.models.CoreConnectivtyInfo` object.

        """
        pass

    def getAllCas(self):
        """

        **Description**

        Used to retrieve the list of :code:`(groupId, caContent)` pair for this discovery information. The retrieved
        pairs could be from different Greengrass groups. This is designed for users who want to iterate through all
        available cores/groups/CAs at the same time, regardless of which group those CAs belong to.

        **Syntax**

        .. code:: python

          myDiscoveryInfo.getAllCas()

        **Parameters**

        None

        **Returns**

        List of :code:`(groupId, caContent)` string pair, where :code:`caContent` is the CA content string and
        :code:`groupId` is the group id that this CA belongs to.

        """
        pass

    def getAllGroups(self):
        """

        **Description**

        Used to retrieve the list of :code:`AWSIoTPythonSDK.core.greengrass.discovery.models.GroupConnectivityInfo`
        object for this discovery information. This is designed for users who want to iterate through all available
        groups that this Greengrass aware device (GGAD) belongs to.

        **Syntax**

        .. code:: python

          myDiscoveryInfo.getAllGroups()

        **Parameters**

        None

        **Returns**

        List of :code:`AWSIoTPythonSDK.core.greengrass.discovery.models.GroupConnectivityInfo` object.

        """
        pass

    def toObjectAtGroupLevel(self):
        """

        **Description**

        Used to get a dictionary of Greengrass group discovery information, with group id string as key and the
        corresponding :code:`AWSIoTPythonSDK.core.greengrass.discovery.models.GroupConnectivityInfo` object as the
        value. This is designed for users who know exactly which group, which core and which set of connectivity info
        they want to use for the Greengrass aware device to connect.

        **Syntax**

        .. code:: python

          # Get to the targeted connectivity information for a specific core in a specific group
          groupLevelDiscoveryInfoObj = myDiscoveryInfo.toObjectAtGroupLevel()
          groupConnectivityInfoObj = groupLevelDiscoveryInfoObj.toObjectAtGroupLevel("IKnowMyGroupId")
          coreConnectivityInfoObj = groupConnectivityInfoObj.getCoreConnectivityInfo("IKnowMyCoreThingArn")
          connectivityInfo = coreConnectivityInfoObj.getConnectivityInfo("IKnowMyConnectivityInfoSetId")
          # Now retrieve the detailed information
          caList = groupConnectivityInfoObj.caList
          host = connectivityInfo.host
          port = connectivityInfo.port
          metadata = connectivityInfo.metadata
          # Actual connecting logic follows...

        """
        pass

    def _decode_group_info(self, group_object):
        pass

    def _decode_core_info(self, core_object, group_id):
        pass
