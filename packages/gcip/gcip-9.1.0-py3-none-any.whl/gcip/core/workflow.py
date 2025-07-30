"""This module represents the Gitlab CI [workflow](https://docs.gitlab.com/ee/ci/yaml/#workflow) keyword.

The workflow keyword is used to control when pipelines are created. It supports rules (a list of Rule objects), name (name of the workflow pipeline), and auto_cancel (controls auto-cancel behavior for redundant pipelines).

Example:

    from gcip.core.workflow import Workflow
    from gcip.core.rule import Rule

    workflow = Workflow(
        rules=[Rule(if_statement='$CI_COMMIT_BRANCH == "main"')],
        name="main-workflow",
        auto_cancel="enabled"
    )
"""

from __future__ import annotations

from enum import Enum
from typing import Any, Dict, Optional

__author__ = "Thomas Steinbach"
__copyright__ = "Copyright 2020 DB Systel GmbH"
__credits__ = ["Thomas Steinbach", "Daniel von Eßen"]
# SPDX-License-Identifier: Apache-2.0
__license__ = "Apache-2.0"
__maintainer__ = "Thomas Steinbach"
__email__ = "thomas.t.steinbach@deutschebahn.com"


class AutoCancelOnNewCommit(Enum):
    CONSERVATIVE = "conservative"
    INTERRUPTIBLE = "interruptible"
    NONE = "none"


class AutoCancelOnJobFailure(Enum):
    ALL = "all"
    NONE = "none"


class Workflow:
    """This class represents the Gitlab CI [workflow](https://docs.gitlab.com/ee/ci/yaml/#workflow) keyword.

    Args:
        name (Optional[str]): Name of the workflow pipeline. Defaults to None.
        auto_cancel (Optional[AutoCancel]): Controls auto-cancel behavior for redundant pipelines. Defaults to None.
    """

    def __init__(
        self,
        name: Optional[str] = None,
        auto_cancel_on_new_commit: Optional[AutoCancelOnNewCommit] = None,
        auto_cancel_on_job_failure: Optional[AutoCancelOnJobFailure] = None,
    ) -> None:
        self._name = name
        self._auto_cancel_on_new_commit = auto_cancel_on_new_commit
        self._auto_cancel_on_job_failure = auto_cancel_on_job_failure

    @property
    def name(self) -> Optional[str]:
        return self._name

    @property
    def auto_cancel_on_new_commit(self) -> Optional[AutoCancelOnNewCommit]:
        return self._auto_cancel_on_new_commit

    @property
    def auto_cancel_on_job_failure(self) -> Optional[AutoCancelOnJobFailure]:
        return self._auto_cancel_on_job_failure

    def render(self) -> Dict[str, Any]:
        """Return a representation of this Workflow object as a dictionary for YAML serialization."""
        rendered: Dict[str, Any] = {}
        if self._name is not None:
            rendered["name"] = self._name
        if (
            self._auto_cancel_on_new_commit is not None
            or self._auto_cancel_on_job_failure is not None
        ):
            rendered["auto_cancel"] = {}
        if self._auto_cancel_on_new_commit is not None:
            rendered["auto_cancel"]["on_new_commit"] = (
                self._auto_cancel_on_new_commit.value
            )
        if self._auto_cancel_on_job_failure is not None:
            rendered["auto_cancel"]["on_job_failure"] = (
                self._auto_cancel_on_job_failure.value
            )
        return rendered
