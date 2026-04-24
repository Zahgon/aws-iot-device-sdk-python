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

import logging
from AWSIoTPythonSDK.core.util.enums import DropBehaviorTypes


class AppendResults(object):
    APPEND_FAILURE_QUEUE_FULL = -1
    APPEND_FAILURE_QUEUE_DISABLED = -2
    APPEND_SUCCESS = 0


class OfflineRequestQueue(list):
    _logger = logging.getLogger(__name__)

    def __init__(self, max_size, drop_behavior=DropBehaviorTypes.DROP_NEWEST):
        if not isinstance(max_size, int) or not isinstance(drop_behavior, int):
            self._logger.error("init: MaximumSize/DropBehavior must be integer.")
            raise TypeError("MaximumSize/DropBehavior must be integer.")
        if drop_behavior != DropBehaviorTypes.DROP_OLDEST and drop_behavior != DropBehaviorTypes.DROP_NEWEST:
            self._logger.error("init: Drop behavior not supported.")
            raise ValueError("Drop behavior not supported.")

        list.__init__([])
        self._drop_behavior = drop_behavior
        # When self._maximumSize > 0, queue is limited
        # When self._maximumSize == 0, queue is disabled
        # When self._maximumSize < 0. queue is infinite
        self._max_size = max_size

    def _is_enabled(self):
        pass

    def _need_drop_messages(self):
        # Need to drop messages when:
        # 1. Queue is limited and full
        # 2. Queue is disabled
        pass

    def set_behavior_drop_newest(self):
        pass

    def set_behavior_drop_oldest(self):
        pass

    # Override
    # Append to a queue with a limited size.
    # Return APPEND_SUCCESS if the append is successful
    # Return APPEND_FAILURE_QUEUE_FULL if the append failed because the queue is full
    # Return APPEND_FAILURE_QUEUE_DISABLED if the append failed because the queue is disabled
    def append(self, data):
        pass
