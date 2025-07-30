# SPDX-FileCopyrightText: 2025 Adrian Herscu
#
# SPDX-License-Identifier: Apache-2.0

import inspect
import logging.config
from pathlib import Path
import sys
from typing import Callable, Optional

import pytest


def configure(config: pytest.Config,
              path: Path = Path(__file__).parent / "logging.ini") -> None:
    """
    Configures logging for pytest using a specified INI file, or defaults to internal logging.ini.
    """
    caller_module = inspect.getmodule(inspect.stack()[1][0])
    module_name = caller_module.__name__ if caller_module else "unknown"

    if path.is_file():
        logging.config.fileConfig(path)
        logging.info(f"{module_name} loaded logs config from: {path}")
    else:
        sys.stderr.write(f"{module_name} couldn't find logs config file {path}")


def makereport(
        item: pytest.Item, call: pytest.CallInfo[None]) -> pytest.TestReport:
    report = pytest.TestReport.from_item_and_call(item, call)

    if call.when == "call":
        report.sections.append(('body', get_test_body(item)))

    return report


def get_test_body(item: pytest.Item) -> str:
    function: Optional[Callable[..., None]] = getattr(item, 'function', None)
    if function is None:
        return "No function found for this test item."

    try:
        return inspect.getsource(function)
    except Exception as e:
        return f"Could not get source code: {str(e)}"
