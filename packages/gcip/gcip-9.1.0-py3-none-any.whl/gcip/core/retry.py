"""This module represents the Gitlab CI [Retry](https://docs.gitlab.com/ee/ci/yaml/#retry) keyword.

    Use `Retry` to specify a retry count to use for the `gcip.core.job.Job`.

```
job1.set_retry(Retry(RetryCound.2))
job2.set_retry(Retry("gcr.io/kaniko-project/executor:debug", entrypoint=[""]))
```
"""

from __future__ import annotations

from copy import deepcopy
from enum import Enum
from typing import Dict, List, Optional, Union

__author__ = "Thomas Steinbach"
__copyright__ = "Copyright 2020 DB Systel GmbH"
__credits__ = ["Thomas Steinbach", "Daniel von Eßen"]
# SPDX-License-Identifier: Apache-2.0
__license__ = "Apache-2.0"
__maintainer__ = "Thomas Steinbach"
__email__ = "thomas.t.steinbach@deutschebahn.com"


class RetryWhen(Enum):
    always = "always"
    unknown_failure = "unknown_failure"
    script_failure = "script_failure"
    api_failure = "api_failure"
    stuck_or_timeout_failure = "stuck_or_timeout_failure"
    runner_system_failure = "runner_system_failure"
    runner_unsupported = "runner_unsupported"
    stale_schedule = "stale_schedule"
    job_execution_timeout = "job_execution_timeout"
    archived_failure = "archived_failure"
    unmet_prerequisites = "unmet_prerequisites"
    scheduler_failure = "scheduler_failure"
    data_integrity_failure = "data_integrity_failure"


class Retry:
    """This module represents the Gitlab CI [Retry](https://docs.gitlab.com/ee/ci/yaml/#retry) keyword.

    Use `Retry` to specify a retry count to use for the `gcip.core.job.Job`.

    Args:
        max (int): Maximum number of job retrys. As of the Gitlab CI documentation in 2024, the
            number cannot be higher than 2.
        when (Optional[List[RetryWhen]]): Use retry:when with retry:max to retry jobs for
            only specific failure cases.
        exit_codes (Optional[List[int]]): Use retry:exit_codes with retry:max to retry jobs for
            only specific failure cases.
    """

    def __init__(
        self,
        *,
        max: int,
        when: Optional[List[RetryWhen]] = None,
        exit_codes: Optional[List[int]] = None,
    ) -> None:
        self._validate_max(max)

        self._max = max
        self._when = when
        self._exit_codes = exit_codes

    def render(self) -> Dict[str, Union[int, Union[List[int], List[str]]]]:
        """Return a representation of this Retry object as dictionary with static values.

        The rendered representation is used by the gcip to dump it
        in YAML format as part of the .gitlab-ci.yml pipeline.

        Returns:
            Dict[str, Union[str, List[str]]]: A dictionary prepresenting the retry object in Gitlab CI.
        """
        rendered: Dict[str, Union[int, Union[List[int], List[str]]]] = {}

        rendered["max"] = self.max

        if self._when:
            rendered["when"] = [item.value for item in self._when]

        if self._exit_codes:
            rendered["exit_codes"] = deepcopy(self._exit_codes)

        return rendered

    def _equals(self, retry: Optional[Retry]) -> bool:
        """
        Returns:
            bool: True if self equals to `retry`.
        """
        if not retry:
            return False

        return self.render() == retry.render()

    def _validate_max(self, value: int) -> None:
        assert value >= 0, "The maximum number of retries cannot be negative."
        assert (
            value <= 2
        ), "As of the Gitlab CI documentation in 2024 the maximum number of retries is 2."

    @property
    def max(self) -> int:
        return self._max

    @max.setter
    def max(self, value: int) -> None:
        self._validate_max(value)
        self._max = value
