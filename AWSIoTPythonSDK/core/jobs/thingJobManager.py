# /*
# * Copyright 2010-2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
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

_BASE_THINGS_TOPIC = "$aws/things/"
_NOTIFY_OPERATION =  "notify"
_NOTIFY_NEXT_OPERATION = "notify-next"
_GET_OPERATION = "get"
_START_NEXT_OPERATION =  "start-next"
_WILDCARD_OPERATION = "+"
_UPDATE_OPERATION = "update"
_ACCEPTED_REPLY = "accepted"
_REJECTED_REPLY =  "rejected"
_WILDCARD_REPLY = "#"

#Members of this enum are tuples
_JOB_ID_REQUIRED_INDEX = 1
_JOB_OPERATION_INDEX = 2

_STATUS_KEY = 'status'
_STATUS_DETAILS_KEY = 'statusDetails'
_EXPECTED_VERSION_KEY = 'expectedVersion'
_EXEXCUTION_NUMBER_KEY = 'executionNumber'
_INCLUDE_JOB_EXECUTION_STATE_KEY = 'includeJobExecutionState'
_INCLUDE_JOB_DOCUMENT_KEY = 'includeJobDocument'
_CLIENT_TOKEN_KEY = 'clientToken'
_STEP_TIMEOUT_IN_MINUTES_KEY = 'stepTimeoutInMinutes'

#The type of job topic.
class jobExecutionTopicType(object):
    JOB_UNRECOGNIZED_TOPIC = (0, False, '')
    JOB_GET_PENDING_TOPIC = (1, False, _GET_OPERATION)
    JOB_START_NEXT_TOPIC = (2, False, _START_NEXT_OPERATION)
    JOB_DESCRIBE_TOPIC = (3, True, _GET_OPERATION)
    JOB_UPDATE_TOPIC = (4, True, _UPDATE_OPERATION)
    JOB_NOTIFY_TOPIC = (5, False, _NOTIFY_OPERATION)
    JOB_NOTIFY_NEXT_TOPIC = (6, False, _NOTIFY_NEXT_OPERATION)
    JOB_WILDCARD_TOPIC = (7, False, _WILDCARD_OPERATION)

#Members of this enum are tuples
_JOB_SUFFIX_INDEX = 1
#The type of reply topic, or #JOB_REQUEST_TYPE for topics that are not replies.
class jobExecutionTopicReplyType(object):
    JOB_UNRECOGNIZED_TOPIC_TYPE = (0, '')
    JOB_REQUEST_TYPE = (1, '')
    JOB_ACCEPTED_REPLY_TYPE = (2, '/' + _ACCEPTED_REPLY)
    JOB_REJECTED_REPLY_TYPE = (3, '/' + _REJECTED_REPLY)
    JOB_WILDCARD_REPLY_TYPE = (4, '/' + _WILDCARD_REPLY)

_JOB_STATUS_INDEX = 1
class jobExecutionStatus(object):
    JOB_EXECUTION_STATUS_NOT_SET = (0, None)
    JOB_EXECUTION_QUEUED = (1, 'QUEUED')
    JOB_EXECUTION_IN_PROGRESS = (2, 'IN_PROGRESS')
    JOB_EXECUTION_FAILED = (3, 'FAILED')
    JOB_EXECUTION_SUCCEEDED = (4, 'SUCCEEDED')
    JOB_EXECUTION_CANCELED = (5, 'CANCELED')
    JOB_EXECUTION_REJECTED = (6, 'REJECTED')
    JOB_EXECUTION_UNKNOWN_STATUS = (99, None)

def _getExecutionStatus(jobStatus):
    pass

def _isWithoutJobIdTopicType(srcJobExecTopicType):
    pass

class thingJobManager:
    def __init__(self, thingName, clientToken = None):
        self._thingName = thingName
        self._clientToken = clientToken

    def getJobTopic(self, srcJobExecTopicType, srcJobExecTopicReplyType=jobExecutionTopicReplyType.JOB_REQUEST_TYPE, jobId=None):
        pass

    def serializeJobExecutionUpdatePayload(self, status, statusDetails=None, expectedVersion=0, executionNumber=0, includeJobExecutionState=False, includeJobDocument=False, stepTimeoutInMinutes=None):
        pass

    def serializeDescribeJobExecutionPayload(self, executionNumber=0, includeJobDocument=True):
        pass

    def serializeStartNextPendingJobExecutionPayload(self, statusDetails=None, stepTimeoutInMinutes=None):
        pass

    def serializeClientTokenPayload(self):
        pass
