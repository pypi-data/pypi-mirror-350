# SPDX-FileCopyrightText: 2025 Adrian Herscu
#
# SPDX-License-Identifier: Apache-2.0

import concurrent.futures
import time
from datetime import timedelta

COMMON_EXECUTOR = concurrent.futures.ThreadPoolExecutor()


def sleep_for(duration: timedelta):
    """
    Sleep for the specified duration.
    Args:
        duration (timedelta): The amount of time to sleep.
    """
    time.sleep(duration.total_seconds())
